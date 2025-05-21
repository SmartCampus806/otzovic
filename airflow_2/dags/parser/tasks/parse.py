from airflow.operators.python import PythonOperator

def mock_parse():
    data = ["item1", "item2", "item3"]
    print("Parsed data:", data)
    return data

def parse_data_task():
    return PythonOperator(
        task_id='parse_data',
        python_callable=mock_parse
    )