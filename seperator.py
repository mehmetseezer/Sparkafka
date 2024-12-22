import pandas as pd
from sklearn.model_selection import train_test_split

# TSLA dosyasını oku (dosya yolunu buraya yazın)
file_path = 'TSLA.csv'  # Buraya CSV dosyanızın yolunu girin

# CSV dosyasını okuma
data = pd.read_csv(file_path)

# Veriyi 75% eğitim (learn), 25% test (send) olarak ayıralım
learn_data, send_data = train_test_split(data, test_size=0.25, random_state=42)

# Eğitim verisini (learn-data.csv) dosyasına kaydet
learn_data.to_csv('learn-data.csv', index=False)

# Test verisini (send-data.csv) dosyasına kaydet
send_data.to_csv('send-data.csv', index=False)

print("Dosya başarıyla bölündü: 'learn-data.csv' ve 'send-data.csv'.")
