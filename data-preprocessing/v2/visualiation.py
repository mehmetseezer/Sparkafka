import matplotlib.pyplot as plt
import seaborn as sns

# Verinin genel özelliklerini görselleştirelim (Dağılım Grafiği ve Korelasyon)
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
