from datetime import datetime
from airflow import DAG

from parser.tasks.parse import parse_data_task
from parser.tasks.enrich_data import enrich_data_task
from parser.tasks.send_to_kafka import send_to_kafka_task

with DAG(
    dag_id='data_pipeline',
    start_date=datetime(2025, 5, 20),
    schedule='@daily',
    catchup=False,
    tags=['demo']
) as dag:
    parse = parse_data_task()
    enrich = enrich_data_task()
    send = send_to_kafka_task()

    parse >> enrich >> send
