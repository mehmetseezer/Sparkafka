import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi yükleme
df = pd.read_csv('dataset/TSLA.csv')  # Verinizin dosya adı

# Scatter plot ile görselleştirme
plt.figure(figsize=(10, 6))  # Grafik boyutunu ayarlama
sns.scatterplot(data=df, x='Open', y='Close', color='blue', alpha=0.6)
plt.title('Open vs Close Price')  # Başlık
plt.xlabel('Open Price')  # X ekseni etiketi
plt.ylabel('Close Price')  # Y ekseni etiketi
plt.grid(True)  # Izgara çizgileri
plt.show()  # Grafiği gösterme
