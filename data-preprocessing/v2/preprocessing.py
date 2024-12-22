import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report

# Veri setini yükleyelim
dataset_path = '../dataset/TSLA.csv'  # Burada veri setinin yolunu güncellemeniz gerekebilir
df = pd.read_csv(dataset_path)

# 'Date' sütununu datetime formatına dönüştürme
df['Date'] = pd.to_datetime(df['Date'])

# Eksik verileri kontrol edelim
print(df.isnull().sum())  # Eksik verileri kontrol etme

# Veri setine göz atalım
print(df.head())  # İlk birkaç satırı gösterme

# Veri görselleştirmeleri
plt.figure(figsize=(10, 6))

# Fiyatların zaman içindeki değişimini gösteren çizgi grafiği
plt.subplot(2, 1, 1)
plt.plot(df['Date'], df['Close'], label='Close Price')
plt.title('Close Price Over Time')
plt.xlabel('Date')
plt.ylabel('Close Price')

# Korelasyon matrisini görselleştirelim
plt.subplot(2, 1, 2)
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')

plt.tight_layout()
plt.show()

# Veriyi normalize etme ve standartlaştırma
scaler_minmax = MinMaxScaler()
scaler_standard = StandardScaler()

# 'Close' sütununu normalize etme ve standartlaştırma
df['Close_normalized'] = scaler_minmax.fit_transform(df[['Close']])
df['Close_standardized'] = scaler_standard.fit_transform(df[['Close']])

# Gözden geçirelim
print(df[['Close', 'Close_normalized', 'Close_standardized']].head())

# Anomali tespiti yapalım
X = df[['Close_normalized']]  # 'Close_normalized' sütunu üzerinde çalışacağız

# Isolation Forest modelini kuruyoruz
model = IsolationForest(contamination=0.05)  # contamination parametresi, anomalilerin oranını belirtir
df['anomaly'] = model.fit_predict(X)

# Anomali tespit edilen verileri işaretleyelim (-1 = anomali, 1 = normal)
anomalies = df[df['anomaly'] == -1]

# Sonuçları görselleştirelim
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], label='Close Price')
plt.scatter(anomalies['Date'], anomalies['Close'], color='red', label='Anomalies')
plt.title('Anomaly Detection in Stock Prices')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()

# Gerçek etiketleri oluşturmak (örneğin, %5'lik oran ile)
df['actual_anomaly'] = np.where(df['anomaly'] == -1, 1, 0)

# Modelin başarı metriklerini değerlendirelim
print("Model Başarım Metrikleri:")
print(classification_report(df['actual_anomaly'], df['anomaly']))

# Anomali tespiti sonucu başarı metriklerini yazdırma
print("Model Başarım Metrikleri:")
print(f"Accuracy: {df['anomaly'].mean()}")
print(f"Anomalilerin Oranı: {df['actual_anomaly'].mean()}")

# Sonuçları görselleştirelim
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], label='Close Price')
plt.scatter(anomalies['Date'], anomalies['Close'], color='red', label='Anomalies')
plt.title('Anomaly Detection in Stock Prices with Performance Metrics')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()

from sklearn.metrics import classification_report, accuracy_score

# Gerçek etiketler (Anomali: 1, Normal: 0) ve tahminler (modelin tespit ettiği anomaliler) üzerinde karşılaştırma
# Gerçek anomaliler
df['actual_anomaly'] = np.where(df['anomaly'] == -1, 1, 0)  # -1 anomali, 1 normal (gerçek etiketler)

# Modelin tahminleri (anomaly column)
df['predicted_anomaly'] = np.where(df['anomaly'] == -1, 1, 0)  # -1 anomali, 1 normal (tahminler)

# Başarım metriklerini raporlama
accuracy = accuracy_score(df['actual_anomaly'], df['predicted_anomaly'])
print(f"Accuracy: {accuracy}")

# Precision, Recall ve F1 Skoru hesaplama
print("Classification Report:")
print(classification_report(df['actual_anomaly'], df['predicted_anomaly']))

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_recall_fscore_support

# Precision, Recall ve F1 skorlarını hesaplama
precision, recall, f1, _ = precision_recall_fscore_support(df['actual_anomaly'], df['predicted_anomaly'], average='binary')

# Başarım metriklerinin görselleştirilmesi
metrics = ['Precision', 'Recall', 'F1 Score']
scores = [precision, recall, f1]

plt.figure(figsize=(8, 5))
sns.barplot(x=metrics, y=scores, palette='viridis')
plt.title('Model Performance Metrics')
plt.ylim(0, 1)  # Y-ekseni aralığını 0-1 arasında ayarlıyoruz
plt.ylabel('Score')
plt.show()
