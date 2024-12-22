from confluent_kafka import Consumer, KafkaException, KafkaError
import json

# Kafka consumer konfigürasyonu
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker adresi
    'group.id': 'python-consumer',  # Consumer group ID
    'auto.offset.reset': 'earliest'  # İlk baştan verileri almak için
}

# Kafka consumer'ı oluştur
consumer = Consumer(conf)

# Kafka topic'ine abone ol
consumer.subscribe(['tesla-data'])

# Mesajları oku
try:
    while True:
        msg = consumer.poll(timeout=1.0)  # 1 saniye bekle

        if msg is None:
            # Veri yoksa bekle
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Partition sonu
                print(f"End of partition reached {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")
            else:
                raise KafkaException(msg.error())
        else:
            # Kafka mesajını JSON formatında işleme
            message = json.loads(msg.value().decode('utf-8'))
            print(f"Received message: {message}")

except KeyboardInterrupt:
    print("Consuming interrupted")

finally:
    # Consumer'ı kapat
    consumer.close()
