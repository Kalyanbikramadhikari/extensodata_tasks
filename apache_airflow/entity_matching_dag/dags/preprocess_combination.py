
import pandas as pd
import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from read_data import read_datas
from datetime import datetime



def final_entity_matching():

    def create_soup(df, df_, soup, soup_name):
        df[soup_name] = df_[soup].apply(lambda x: ' '.join(x.values.astype(str)).lower(), axis=1)

    soup = ['Name', 'Date of Birth', 'Father_Name']

    layouts,layout_copies = read_datas()
    layout1 = layouts[0]
    layout2 = layouts[1]
    layout3 = layouts[2]
    layout4 = layouts[3]
    layout5 = layouts[4]
    for i, j, k, in zip(layouts, layout_copies, range(len(layouts))):
        create_soup(i, j, soup, f"soup{k+1}")


    def combine(A, B, soup_A, soup_B, threshold=0.3):
        # Initialize the TF-IDF Vectorizer
        tfidf = TfidfVectorizer(stop_words='english')

        # Combine the textual data for fitting the TF-IDF model
        combined_soup = pd.concat([A[soup_A], B[soup_B]], ignore_index=True)
        tfidf.fit(combined_soup)

        # Transform the textual data into TF-IDF matrices
        tfidf_matrix_A = tfidf.transform(A[soup_A])
        tfidf_matrix_B = tfidf.transform(B[soup_B])

        # Compute cosine similarity between the two matrices
        similarity = cosine_similarity(tfidf_matrix_A, tfidf_matrix_B)
        similarity_df = pd.DataFrame(similarity, index=A.index, columns=B.index)

        # Determine the index of the most similar row in B for each row in A
        max_idx_row = similarity_df.idxmax(axis=1)
        similarity_mask = similarity_df.max(axis=1) >= threshold

        # Initialize the combined DataFrame with A, ensuring all columns from both DataFrames
        combined_columns = list(set(A.columns) | set(B.columns))
        combined_data = pd.DataFrame(columns=combined_columns)

        # Merge the similar rows
        for idx_A in A.index:
            if similarity_mask[idx_A]:
                idx_B = max_idx_row[idx_A]
                combined_row = A.loc[idx_A].combine_first(B.loc[idx_B])
                combined_row['source'] = f"{A.loc[idx_A]['source']}, {B.loc[idx_B]['source']}"
                combined_row['modified_date'] = datetime.now()
            else:
                combined_row = A.loc[idx_A]
            combined_data = pd.concat([combined_data, combined_row.to_frame().T], ignore_index=True)

        # Append non-similar rows from B to A
        new_records = B.loc[~B.index.isin(max_idx_row[similarity_mask].values)]
        result = pd.concat([combined_data, new_records], ignore_index=True)
        result.drop(columns=soup_B, inplace=True)
        return result

    result_12 = combine(layout1, layout2, 'soup1', 'soup2')
    result_123 = combine(result_12, layout3, 'soup1', 'soup3')
    result_1234 = combine(result_123, layout4, 'soup1', 'soup4')
    final_result = combine(result_1234, layout5, 'soup1', 'soup5')

    return final_result.to_csv('/usr/local/airflow/dags/final_output/final_result.csv')
