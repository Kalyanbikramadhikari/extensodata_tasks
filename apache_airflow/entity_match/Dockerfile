FROM apache/airflow:2.9.1

ADD requirements.txt .

# Install apache-airflow and other dependencies
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
