from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.python_operator import PythonOperator
from read_data import read_datas
from preprocess_combination import final_entity_matching
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 14),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'extenso_assignment',
    default_args=default_args,
    description='A DAG for entity matching',
    schedule_interval='@once',
    catchup=False,
)

preparing_preprocessing = PythonOperator(
    task_id = "reader",
    python_callable = read_datas,
    dag = dag
)
final_df = PythonOperator(
    task_id = "output",
    python_callable = final_entity_matching,
    dag = dag
)
preparing_preprocessing >> final_df




