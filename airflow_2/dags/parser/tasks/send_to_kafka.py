from kafka import KafkaProducer
import json
import time

# Настройки
bootstrap_servers = ['kafka1:9092', 'kafka2:9093']
topic = 'test-topic'

# Создание продюсера
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

from airflow.operators.python import PythonOperator

def mock_send(ti):
    enriched = ti.xcom_pull(task_ids='enrich_data')
    message = {'enriched': enriched}
    producer.send(topic, value=message)

def send_to_kafka_task():
    return PythonOperator(
        task_id='send_to_kafka',
        python_callable=mock_send
    )