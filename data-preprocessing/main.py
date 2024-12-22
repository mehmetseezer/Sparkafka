import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Veriyi yükle
df = pd.read_csv('dataset/normalized_TSLA.csv', parse_dates=['Date'], index_col='Date')

# Kapanış fiyatını hedef değişken olarak seçiyoruz
data = df[['Close']]

# Veriyi normalize et
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Zaman penceresi için veri oluşturma (10 gün geçmiş veri ile 1 gün sonrası tahmini)
def create_dataset(data, window_size=10):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i, 0])  # Geçmiş 10 günün verisi
        y.append(data[i, 0])  # 10. gün sonrasının kapanış fiyatı
    return np.array(X), np.array(y)

# Veriyi hazırlama
window_size = 10
X, y = create_dataset(scaled_data, window_size)

# Veriyi eğitim ve test setlerine ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Veriyi LSTM modeline uygun hale getirme (3D: [samples, time_steps, features])
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# LSTM modelini oluşturma
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=1))  # Tek bir çıktı değeri (kapanış fiyatı)

# Modeli derleme
model.compile(optimizer='adam', loss='mean_squared_error')

# Modeli eğitme
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Test verisi ile tahmin yapma
y_pred = model.predict(X_test)

# Tahminleri ve gerçek değerleri orijinal ölçeğe geri döndürme
y_pred = scaler.inverse_transform(y_pred)
y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

# Sonuçları görselleştirme
plt.figure(figsize=(10, 6))
plt.plot(y_test, label='Gerçek Değerler')
plt.plot(y_pred, label='Tahmin Edilen Değerler')
plt.title('LSTM Modeli - Kapanış Fiyatı Tahmini')
plt.xlabel('Zaman')
plt.ylabel('Kapanış Fiyatı')
plt.legend()
plt.show()

# Modelin performansını değerlendirme
mae = np.mean(np.abs(y_test - y_pred))
mse = np.mean((y_test - y_pred) ** 2)
print(f"MAE: {mae}")
print(f"MSE: {mse}")
