from kafka import KafkaProducer
import json
import time

# Настройки
bootstrap_servers = ['localhost:29092', 'localhost:29093']
topic = 'test-topic'

# Создание продюсера
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Отправка сообщений
for i in range(10):
    message = {'number': i}
    producer.send(topic, value=message)
    print(f"Отправлено: {message}")
    time.sleep(1)

producer.flush()
producer.close()