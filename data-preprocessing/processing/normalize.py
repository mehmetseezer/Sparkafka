import pandas as pd
from sklearn.preprocessing import MinMaxScaler
# CSV dosyasını yükleme
df = pd.read_csv('dataset/TSLA.csv')  # Burada 'veri_seti.csv' yerine kendi dosyanızın adını yazmalısınız

# Sayısal sütunları seçme
numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# MinMaxScaler nesnesini oluşturma
scaler = MinMaxScaler()

# Veriyi normalize etme
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
# Normalize edilmiş veriyi yeni bir CSV dosyasına kaydetme
df.to_csv('normalized_dataset.csv', index=False)


# Normalizasyon sonrası veriyi kontrol etme
print(df.head())
