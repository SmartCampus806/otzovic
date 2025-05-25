# etl_mongo_to_clickhouse.py

from datetime import datetime
from pymongo import MongoClient
from clickhouse_driver import Client as ClickHouseClient
from pymongo.errors import PyMongoError
import time

MONGO_URI = "mongodb://localhost:27017"
CLICKHOUSE_HOST = "localhost"
MONGO_DB = "your_db"
MONGO_COLLECTION = "your_collection"
CLICKHOUSE_DB = "default"
CLICKHOUSE_TABLE = "mongo_data"

mongo_client = MongoClient(MONGO_URI)
mongo_collection = mongo_client[MONGO_DB][MONGO_COLLECTION]
clickhouse_client = ClickHouseClient(host=CLICKHOUSE_HOST)

clickhouse_client.execute(f"""
CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE} (
    date DateTime,
    rating Int32,
    city String,
    comments Int32,
    id Int32,
    class Int32,
    mood Int32,
    status Enum('inprogress' = 0, 'done' = 1)
) ENGINE = MergeTree()
ORDER BY id
""")

print("Watching MongoDB for changes...")

with mongo_collection.watch(full_document='updateLookup') as stream:
    for change in stream:
        try:
            doc = change.get("fullDocument")
            if not doc:
                continue

            date = doc.get("date", datetime.utcnow())
            rating = doc.get("rating", 0)
            city = doc.get("city", "")
            comments = doc.get("comments", 0)
            _id = doc.get("id", 0)
            clazz = doc.get("class")
            mood = doc.get("mood")

            has_class = clazz is not None
            has_mood = mood is not None
            status = "done" if has_class and has_mood else "inprogress"

            row = [
                date,
                rating,
                city,
                comments,
                _id,
                clazz if clazz is not None else 0,
                mood if mood is not None else 0,
                status
            ]

            clickhouse_client.execute(
                f"INSERT INTO {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE} VALUES",
                [row]
            )

            print(f"Synced change for id={_id}, status={status}")

        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        except Exception as ex:
            print(f"Processing error: {ex}")
