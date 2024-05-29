#FROM apache/airflow:2.3.0-python3.8

FROM puckel/docker-airflow:1.10.9
RUN pip install requests
RUN pip install pandas
RUN pip install numpy scikit-learn


#FROM apache/airflow:latest

#USER root
#RUN apt-get update && \
#
#    apt-get -y install git && \
#
#    apt-get clean
#USER airflow