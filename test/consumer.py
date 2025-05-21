from kafka import KafkaConsumer
import json

# Настройки
bootstrap_servers = ['localhost:29092', 'localhost:29093']
topic = 'test-topic'
group_id = 'test-group'

# Создание консьюмера
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    group_id=group_id,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

try:
    for message in consumer:
        print(f"Получено: {message.value}")
except KeyboardInterrupt:
    print("Прерывание...")
finally:
    consumer.close()