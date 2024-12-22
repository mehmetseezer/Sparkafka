import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV dosyasını yükleme
df = pd.read_csv('normalized_dataset.csv')  # Verinizin dosya adı

# Sayısal sütunları belirleyelim
numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# Her bir sayısal sütun için histogram çizme
for column in numerical_columns:
    plt.figure(figsize=(10, 6))  # Grafik boyutunu ayarlama
    df[column].hist(bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title(f'{column} Distribution')  # Başlık
    plt.xlabel(column)  # X ekseni etiketi
    plt.ylabel('Frequency')  # Y ekseni etiketi
    plt.grid(True)  # Izgara çizgileri
    plt.show()  # Grafiği gösterme
