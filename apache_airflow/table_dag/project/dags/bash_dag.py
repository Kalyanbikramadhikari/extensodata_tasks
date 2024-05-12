from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

bash_dag = DAG(
    'bash',
    default_args=default_args,
    description='A DAG to dump a MySQL table',
    schedule_interval='@once',
    catchup=False,
)

curl_command = 'curl -o /opt/airflow/dags/xrate.csv "https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata"'
run_this = BashOperator(
    task_id="bash_curl",
    bash_command=curl_command,
    dag=bash_dag
)
