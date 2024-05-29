from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Levenshtein import distance

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'entity_match_dag',
    default_args=default_args,
    description='A simple DAG to perform entity matching',
    schedule_interval='@once',
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define the task to load data
def load_df():
    layout1 = pd.read_csv('/opt/airflow/files/ABC_layout_1.csv')
    layout2 = pd.read_csv('/opt/airflow/files/PQR_layout_2.csv')
    layout3 = pd.read_csv('/opt/airflow/files/layout_3_voters.csv')
    layout4 = pd.read_csv('/opt/airflow/files/KLM_layout_4.csv')
    layout5 = pd.read_csv('/opt/airflow/files/layout_5_license.csv')
    return [layout1, layout2, layout3, layout4, layout5]

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_df,
    dag=dag,
)

# Define the task to preprocess data
def preprocess(ti):
    layouts = ti.xcom_pull(task_ids='load_task')
    layout1, layout2, layout3, layout4, layout5 = layouts
    layout1 = layout1.rename(
        columns={"First Name": "Name", "Father Name": "Father_Name", "Permanent_Adress": "Permanent_Address"})
    layout2 = layout2.rename(columns={"Customer_ID": "Mobile Number"})
    layout3 = layout3.rename(
        columns={"votersName": "Name", "votersFatherName": "Father_Name", "votersMotherName": "Mother Name",
                 " Gender": "Gender", "Permanent_Adress": "Permanent_Address"})
    layout4 = layout4.rename(columns={"Father Name": "Father_Name"})

    layouts = [layout1, layout2, layout3, layout4, layout5]
    layout_sources = ['bank', 'esewa', 'voter', 'electricity', 'license']

    for layout, source in zip(layouts, layout_sources):
        layout['source'] = source
        layout['modified_date'] = datetime.now()

    def sanitize(df):
        return df.applymap(
            lambda x: x.replace(',', '').replace(' ', '').strip() if isinstance(x, str) else '' if pd.isna(x) else x)

    soup = ['Name', 'Date of Birth', 'Father_Name']

    def create_soup(df, soup):
        df['soup'] = df[soup].apply(lambda x: ' '.join(x.values.astype(str)).lower(), axis=1)

    for layout in layouts:
        sanitized_layout = sanitize(layout.copy())
        create_soup(sanitized_layout, soup)
        layout['soup'] = sanitized_layout['soup']

    return [layout1, layout2, layout3, layout4, layout5]


preprocess_task = PythonOperator(
    task_id='preprocess_task',
    python_callable=preprocess,
    dag=dag,
)

# Define the task to perform entity matching
def entity_matching(ti):
    layouts = ti.xcom_pull(task_ids='preprocess_task')
    layout1, layout2, layout3, layout4, layout5 = layouts
    def combine_layouts(A, B, metric='levenshtein', threshold=20):
        def calculate_similarity(A, B, metric):
            if metric == 'cosine':
                tfidf = TfidfVectorizer(stop_words='english')
                combined_soup = pd.concat([A['soup'], B['soup']], ignore_index=True)
                tfidf.fit(combined_soup)
                tfidf_matrix_A = tfidf.transform(A['soup'])
                tfidf_matrix_B = tfidf.transform(B['soup'])
                similarity = cosine_similarity(tfidf_matrix_A, tfidf_matrix_B)
                similarity_df = pd.DataFrame(similarity, index=A.index, columns=B.index)
                idx_row = similarity_df.idxmax(axis=1)
                similarity_mask = similarity_df.max(axis=1) > threshold
            else:
                distance_matrix = pd.DataFrame([[distance(a, b) for b in B['soup']] for a in A['soup']], index=A.index,
                                               columns=B.index)
                idx_row = distance_matrix.idxmin(axis=1)
                similarity_mask = distance_matrix.min(axis=1) <= threshold
            return idx_row, similarity_mask

        def merge_data(A, B, idx_row, similarity_mask):
            combined_columns = list(set(A.columns) | set(B.columns))
            combined_data = pd.DataFrame(columns=combined_columns)
            for idx_A in A.index:
                if similarity_mask[idx_A]:
                    idx_B = idx_row[idx_A]
                    combined_row = A.loc[idx_A].combine_first(B.loc[idx_B])
                    combined_row['source'] = f"{A.loc[idx_A]['source']}, {B.loc[idx_B]['source']}"
                    combined_row['modified_date'] = datetime.now()
                else:
                    combined_row = A.loc[idx_A]
                combined_data = pd.concat([combined_data, combined_row.to_frame().T], ignore_index=True)
            new_records = B.loc[~B.index.isin(idx_row[similarity_mask].values)]
            return pd.concat([combined_data, new_records], ignore_index=True)

        idx_row, similarity_mask = calculate_similarity(A, B, metric)
        return merge_data(A, B, idx_row, similarity_mask)

    result_12 = combine_layouts(layout1, layout2)
    result_123 = combine_layouts(result_12, layout3)
    result_1234 = combine_layouts(result_123, layout4)
    final_result = combine_layouts(result_1234, layout5)
    final_result.to_csv('/opt/airflow/files/final_result.csv', index=False, header=True)

entity_match_task = PythonOperator(
    task_id='entity_match_task',
    python_callable=entity_matching,
    dag=dag,
)

# Set task dependencies
load_task >> preprocess_task >> entity_match_task
