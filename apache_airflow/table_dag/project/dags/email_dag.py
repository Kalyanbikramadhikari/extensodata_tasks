from datetime import datetime, timedelta
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 14),
    'email': ['ngawanggurung@outlook.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def start_task():
    print("task started")

email_dag = DAG(
    dag_id='emaildag',
    description='Use case of email operator in Airflow',
    default_args=default_args,
    # schedule_interval='@once',
    schedule_interval='30 1 * * *',
    dagrun_timeout=timedelta(minutes=60),
    catchup=False)

start_task = PythonOperator(
    task_id='executetask',
    python_callable=start_task,
    dag=email_dag
)

send_email = EmailOperator(
    task_id='send_email',
    to='tseringnc707@gmail.com',
    # to='susma.pant@extensodata.com',
    # to = ['tseringnc707@gmail.com','susma.pant@extensodata.com','neupanebishal039@gmail.com', 'anuragkarkikarki79@gmail.com', 'bisheshkafle18@gmail.com', 'kalyanad100@gmail.com'],
    subject='Airflow Message',
    html_content="""<h2>Good Morning, Ngawang Gurung</h2>""",
    dag=email_dag
)

start_task >> send_email
