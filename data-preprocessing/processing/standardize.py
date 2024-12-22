import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

df = pd.read_csv('dataset/TSLA.csv')

# Sayısal sütunları seçme
numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# StandardScaler ile standardize etme
scaler = StandardScaler()

# Veriyi standardize etme
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# Sonuçları kontrol etme
print(df.head())

# Standardize edilmiş veriyi yeni bir CSV dosyasına kaydetme
df.to_csv('standardize_veri.csv', index=False)

