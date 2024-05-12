#datetime
from datetime import timedelta, datetime

# DAG object
from airflow import DAG

# Operators
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

# Initializing default arguments for DAG
default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2024, 3, 14),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

# Instantiate a DAG
first_dag = DAG(
    dag_id='first_dag',
    default_args=default_args,
    description='This is my first DAG',
    schedule_interval='@once',
    catchup=False
)

# Creating a callable function
def print_hello():
    return 'Hello, World!'

# Creating tasks
start_task = DummyOperator(
    task_id = 'start_task',
    dag = first_dag
)

hello_world_task = PythonOperator(
    task_id = 'hello_world_task',
    python_callable = print_hello,
    dag = first_dag
)

end_task = DummyOperator(
    task_id = 'end_task',
    dag = first_dag
)

# Setting up dependencies

start_task >> hello_world_task >> end_task




