import asyncio
from aiokafka import AIOKafkaConsumer
import json

async def consume_messages():
    # Настройки консьюмера
    bootstrap_servers = ['localhost:29092', 'localhost:29093', 'localhost:29094']
    topic = 'test-topic'
    group_id = 'test-group'

    # Инициализация консьюмера
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest'
    )
    await consumer.start()

    try:
        # Чтение сообщений
        async for message in consumer:
            print(f"Получено: {message.value}")
    finally:
        # Закрытие соединения
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_messages())