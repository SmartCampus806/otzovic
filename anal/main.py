# app/main.py

from fastapi import FastAPI, Response
from clickhouse_connect import get_client
from typing import Dict
import pandas as pd
from io import BytesIO

app = FastAPI(title="Bank Review Analytics API")

# Настройка ClickHouse клиента
client = get_client(host='localhost', username='default', password='', database='default')
TABLE = 'bank_reviews'

@app.get("/average_rating_by_city")
def average_rating_by_city() -> Dict:
    """
    Метрика: Средний рейтинг по городам
    Расчёт: AVG(rating) GROUP BY city
    Назначение: Анализирует удовлетворенность клиентов по регионам.
    """
    result = client.query(f"""
        SELECT city, AVG(rating) as avg_rating
        FROM {TABLE}
        GROUP BY city
        ORDER BY avg_rating DESC
    """).result_rows
    return {"description": "Средний рейтинг по городам", "data": result}


@app.get("/mood_distribution")
def mood_distribution() -> Dict:
    """
    Метрика: Распределение по тональности
    Расчёт: COUNT(*) GROUP BY mood
    Назначение: Отслеживание эмоционального фона клиентов.
    """
    result = client.query(f"""
        SELECT mood, COUNT(*) as count
        FROM {TABLE}
        GROUP BY mood
        ORDER BY count DESC
    """).result_rows
    return {"description": "Распределение отзывов по тональности", "data": result}


@app.get("/review_status_count")
def review_status_count() -> Dict:
    """
    Метрика: Количество отзывов по статусам
    Расчёт: COUNT(*) GROUP BY status
    Назначение: Показывает объём необработанных и завершённых отзывов.
    """
    result = client.query(f"""
        SELECT status, COUNT(*) as count
        FROM {TABLE}
        GROUP BY status
    """).result_rows
    return {"description": "Количество отзывов по статусам", "data": result}


@app.get("/top_negative_cities")
def top_negative_cities() -> Dict:
    """
    Метрика: ТОП-5 городов по количеству негативных отзывов
    Расчёт: WHERE mood = -1 GROUP BY city LIMIT 5
    Назначение: Выявление регионов с наибольшим числом проблем.
    """
    result = client.query(f"""
        SELECT city, COUNT(*) as negative_count
        FROM {TABLE}
        WHERE mood = -1
        GROUP BY city
        ORDER BY negative_count DESC
        LIMIT 5
    """).result_rows
    return {"description": "ТОП-5 городов по негативу", "data": result}


@app.get("/category_distribution")
def category_distribution() -> Dict:
    """
    Метрика: Распределение отзывов по категориям (class)
    Расчёт: COUNT(*) GROUP BY class
    Назначение: Понимание, какие темы вызывают отклики.
    """
    result = client.query(f"""
        SELECT class, COUNT(*) as count
        FROM {TABLE}
        GROUP BY class
        ORDER BY count DESC
    """).result_rows
    return {"description": "Распределение по категориям отзывов", "data": result}


@app.get("/average_rating_over_time")
def average_rating_over_time() -> Dict:
    """
    Метрика: Средний рейтинг по неделям
    Расчёт: AVG(rating) по неделям
    Назначение: Отслеживание трендов удовлетворенности клиентов.
    """
    result = client.query(f"""
        SELECT toStartOfWeek(date) as week, AVG(rating) as avg_rating
        FROM {TABLE}
        GROUP BY week
        ORDER BY week
    """).result_rows
    return {"description": "Средний рейтинг по неделям", "data": result}


@app.get("/review_volume_trend")
def review_volume_trend() -> Dict:
    """
    Метрика: Динамика количества отзывов по неделям
    Расчёт: COUNT(*) по неделям
    Назначение: Анализирует активность пользователей и сезонность.
    """
    result = client.query(f"""
        SELECT toStartOfWeek(date) as week, COUNT(*) as reviews
        FROM {TABLE}
        GROUP BY week
        ORDER BY week
    """).result_rows
    return {"description": "Динамика отзывов по неделям", "data": result}


@app.get("/export/excel")
def export_all_metrics_to_excel():
    """
    Экспорт всех метрик в Excel файл.
    Удобно для менеджеров для анализа оффлайн.
    """
    queries = {
        "average_rating_by_city": f"SELECT city, AVG(rating) as avg_rating FROM {TABLE} GROUP BY city ORDER BY avg_rating DESC",
        "mood_distribution": f"SELECT mood, COUNT(*) as count FROM {TABLE} GROUP BY mood ORDER BY count DESC",
        "review_status_count": f"SELECT status, COUNT(*) as count FROM {TABLE} GROUP BY status",
        "top_negative_cities": f"SELECT city, COUNT(*) as negative_count FROM {TABLE} WHERE mood = -1 GROUP BY city ORDER BY negative_count DESC LIMIT 5",
        "category_distribution": f"SELECT class, COUNT(*) as count FROM {TABLE} GROUP BY class ORDER BY count DESC",
        "average_rating_over_time": f"SELECT toStartOfWeek(date) as week, AVG(rating) as avg_rating FROM {TABLE} GROUP BY week ORDER BY week",
        "review_volume_trend": f"SELECT toStartOfWeek(date) as week, COUNT(*) as reviews FROM {TABLE} GROUP BY week ORDER BY week",
    }
    
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        for name, sql in queries.items():
            df = client.query_df(sql)
            df.to_excel(writer, sheet_name=name[:31], index=False)
    excel_buffer.seek(0)
    return Response(content=excel_buffer.read(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=bank_review_metrics.xlsx"})
