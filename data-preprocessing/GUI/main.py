import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Veriyi standardize etme fonksiyonu
def standardize_data(input_file, output_file):
    df = pd.read_csv(input_file)
    numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    scaler = StandardScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    df.to_csv(output_file, index=False)
    messagebox.showinfo("Başarı", f"Veri başarıyla standardize edildi ve {output_file} dosyasına kaydedildi.")
    print(df.head())

# Veriyi normalize etme fonksiyonu
def normalize_data(input_file, output_file):
    df = pd.read_csv(input_file)
    numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    scaler = MinMaxScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    df.to_csv(output_file, index=False)
    messagebox.showinfo("Başarı", f"Veri başarıyla normalize edildi ve {output_file} dosyasına kaydedildi.")
    print(df.head())

# Histogram fonksiyonu
def plot_histogram(input_file):
    df = pd.read_csv(input_file)
    numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    df[numerical_columns].hist(bins=15, figsize=(10, 6), color='#4CAF50', edgecolor='black')
    plt.suptitle('Numerical Columns Histogram', fontsize=16)
    plt.tight_layout()
    plt.show()

# Korelasyon heatmap fonksiyonu
def plot_correlation_heatmap(input_file):
    df = pd.read_csv(input_file)
    numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    corr_matrix = df[numerical_columns].corr()
    print("Korelasyon Matrisi:")
    print(corr_matrix)
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Korelasyon Heatmap', fontsize=16)
    plt.tight_layout()
    plt.show()

# Scatter plot fonksiyonu
def plot_scatter(input_file):
    df = pd.read_csv(input_file)
    numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Open', y='Close', hue='Volume', palette='coolwarm', s=100)
    plt.title('Scatter Plot: Open vs Close', fontsize=16)
    plt.tight_layout()
    plt.show()

# Dosya seçimi fonksiyonu
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV dosyaları", "*.csv")])
    return file_path

# GUI penceresi
def create_gui():
    root = tk.Tk()
    root.title("Veri Dönüşümü ve Görselleştirme")
    root.geometry("900x600")  # Daha geniş pencere
    root.config(bg="#F0F0F0")  # Arka plan rengini açık gri yapalım

    # Başlık etiketini ekleyelim
    header_label = tk.Label(root, text="Veri Dönüşümü & Görselleştirme", font=("Helvetica", 20, 'bold'), bg="#4CAF50", fg="white", height=2)
    header_label.pack(fill='x', pady=10)

    # Butonların yerleştirileceği alan
    button_frame = tk.Frame(root, bg="#F0F0F0")
    button_frame.pack(pady=30)

    # Dosya yükleme ve işlem yapma
    def load_and_process_file():
        input_file = load_file()
        if input_file:
            messagebox.showinfo("Dosya Seçildi", f"Dosya seçildi: {input_file}")
            return input_file

    # Histogram butonu
    def display_histogram():
        input_file = load_and_process_file()
        if input_file:
            plot_histogram(input_file)

    # Korelasyon heatmap butonu
    def display_correlation_heatmap():
        input_file = load_and_process_file()
        if input_file:
            plot_correlation_heatmap(input_file)

    # Scatter plot butonu
    def display_scatter_plot():
        input_file = load_and_process_file()
        if input_file:
            plot_scatter(input_file)

    # Standardize butonu
    def standardize_button():
        input_file = load_and_process_file()
        if input_file:
            output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV dosyaları", "*.csv")])
            if output_file:
                standardize_data(input_file, output_file)

    # Normalize butonu
    def normalize_button():
        input_file = load_and_process_file()
        if input_file:
            output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV dosyaları", "*.csv")])
            if output_file:
                normalize_data(input_file, output_file)

    # Butonların düzenlenmesi
    load_button = ttk.Button(button_frame, text="Dosya Yükle", command=load_and_process_file, width=20, style="TButton")
    load_button.grid(row=0, column=0, padx=20, pady=10)

    hist_button = ttk.Button(button_frame, text="Histogram Göster", command=display_histogram, width=20, style="TButton")
    hist_button.grid(row=0, column=1, padx=20, pady=10)

    heatmap_button = ttk.Button(button_frame, text="Heatmap Göster", command=display_correlation_heatmap, width=20, style="TButton")
    heatmap_button.grid(row=1, column=0, padx=20, pady=10)

    scatter_button = ttk.Button(button_frame, text="Scatter Plot Göster", command=display_scatter_plot, width=20, style="TButton")
    scatter_button.grid(row=1, column=1, padx=20, pady=10)

    standardize_button = ttk.Button(button_frame, text="Veriyi Standardize Et", command=standardize_button, width=20, style="TButton")
    standardize_button.grid(row=2, column=0, padx=20, pady=10)

    normalize_button = ttk.Button(button_frame, text="Veriyi Normalize Et", command=normalize_button, width=20, style="TButton")
    normalize_button.grid(row=2, column=1, padx=20, pady=10)

    # Stil oluşturma
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat", background="#4CAF50", foreground="black")  # Yazı rengini siyah yaptık
    style.map("TButton", background=[('active', '#45a049')])

    # Pencereyi başlatma
    root.mainloop()

# Arayüzü başlatma
create_gui()
