import asyncio
from aiokafka import AIOKafkaProducer
import json

async def send_messages():
    # Настройки продюсера
    bootstrap_servers = ['localhost:29092', 'localhost:29093']
    topic = 'test-topic'

    # Инициализация продюсера
    producer = AIOKafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()

    try:
        # Отправка сообщений
        for i in range(3):
            message = {'async_number': i}
            await producer.send_and_wait(topic, value=message)
            print(f"Отправлено: {message}")
            await asyncio.sleep(1)  # Задержка для наглядности
    finally:
        # Закрытие соединения
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(send_messages())