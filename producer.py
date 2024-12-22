import pandas as pd
from confluent_kafka import Producer
import json
import time

# Kafka producer konfigürasyonu
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker adresi
    'client.id': 'python-producer'  # Client ID
}

# Kafka producer'ı oluştur
producer = Producer(conf)

# Hedef Kafka topic adı
topic = 'tesla-data'

# CSV dosyasını pandas ile oku
csv_file = 'send-data.csv'  # Buraya send-data.csv dosyanızın yolunu yazın
data = pd.read_csv(csv_file)

# Veriyi Kafka'ya gönderme fonksiyonu
def send_to_kafka(row):
    """Verilen satırı Kafka'ya gönderir."""
    message = {
        "date": row['Date'],
        "open": row['Open'],
        "high": row['High'],
        "low": row['Low'],
        "close": row['Close'],
        "volume": row['Volume']
    }
    
    # Mesajı Kafka'ya gönder
    producer.produce(topic, key=row['Date'], value=json.dumps(message))
    print(f"Sent message: {message}")

# Verileri sırayla Kafka'ya gönder
for index, row in data.iterrows():
    send_to_kafka(row)
    time.sleep(1)  # Her mesajdan sonra 1 saniye bekle (kendi ihtiyacınıza göre ayarlayabilirsiniz)

# Producer'ı bekle ve kapat
producer.flush()
producer.close()
