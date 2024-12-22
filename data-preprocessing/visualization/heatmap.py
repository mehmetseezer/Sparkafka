import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# CSV dosyasını yükleme
df = pd.read_csv('normalized_dataset.csv')  # Verinizin dosya adı

# Sayısal sütunları seçme
numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# Korelasyon matrisini hesaplama
corr_matrix = df[numerical_columns].corr()

# Korelasyon matrisini yazdırma
print(corr_matrix)

# Korelasyon matrisini görselleştirme
plt.figure(figsize=(10, 6))  # Grafik boyutunu ayarlama
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap')  # Başlık
plt.show()  # Görselleştirmeyi gösterme
