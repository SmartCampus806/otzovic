from airflow.operators.python import PythonOperator

def mock_enrich(ti):
    data = ti.xcom_pull(task_ids='parse_data')
    enriched = [item + "_enriched" for item in data]
    print("Enriched data:", enriched)
    return enriched

def enrich_data_task():
    return PythonOperator(
        task_id='enrich_data',
        python_callable=mock_enrich
    )
