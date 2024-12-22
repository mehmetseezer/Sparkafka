import tkinter as tk
from tkinter import messagebox
from confluent_kafka import Consumer, KafkaException, KafkaError, Producer
import json
import csv
import threading
import time

# Kafka Consumer Konfigürasyonu
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'python-consumer',
    'auto.offset.reset': 'earliest'
}

# Kafka Producer Konfigürasyonu
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}

# Kafka Producer'ı oluştur
producer = Producer(producer_conf)

# Kafka Consumer'ı oluştur
consumer = Consumer(consumer_conf)
consumer.subscribe(['tesla-data'])  # Kafka topic'ine abone ol


# Producer: CSV dosyasından veri gönderme
def send_message_to_kafka():
    try:
        # CSV dosyasını oku ve her satırı Kafka'ya gönder
        csv_file_path = "TSLA.csv"  # CSV dosyasının yolu
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)  # CSV'yi dict formatında okuyacağız
            
            # Her satırdaki veriyi Kafka'ya gönder
            for row in csvreader:
                message = {
                    "date": row['Date'],
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": int(row['Volume'])
                }

                # Mesajı Kafka'ya gönder
                producer.produce('tesla-data', key=row['Date'], value=json.dumps(message))
                print(f"Sent message: {message}")
                producer.flush()
                time.sleep(1)

        messagebox.showinfo("Producer", "All messages sent successfully!")
    except Exception as e:
        messagebox.showerror("Producer Error", f"Error sending message: {e}")


# Consumer İşlevi
def consume_messages():
    def run_consumer():
        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print(f"End of partition reached {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")
                    else:
                        raise KafkaException(msg.error())
                else:
                    message = json.loads(msg.value().decode('utf-8'))
                    messages_list.insert(tk.END, f"Received message: {message}")
                    messages_list.yview(tk.END)  # Scroll to the bottom
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    # Yeni bir thread başlatarak consumer'ı çalıştırıyoruz
    threading.Thread(target=run_consumer, daemon=True).start()
    messagebox.showinfo("Consumer", "Consumer is running and listening for messages.")


# GUI Ayarları
root = tk.Tk()
root.title("Kafka Producer and Consumer")
root.geometry("500x400")

# Kafka Consumer Butonu
consumer_button = tk.Button(root, text="Start Kafka Consumer", command=consume_messages, width=20, height=2)
consumer_button.pack(pady=10)

# Kafka Producer Butonu
producer_button = tk.Button(root, text="Send Messages to Kafka", command=lambda: threading.Thread(target=send_message_to_kafka, daemon=True).start(), width=20, height=2)
producer_button.pack(pady=10)

# Mesajları göstermek için bir liste kutusu
messages_list = tk.Listbox(root, width=60, height=10)
messages_list.pack(pady=10)

# Uygulamayı başlat
root.mainloop()
