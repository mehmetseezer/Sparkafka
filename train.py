from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

# SparkSession başlatma
spark = SparkSession.builder.appName("StockPricePrediction").getOrCreate()

# CSV dosyasını okuma
file_path = "learn-data.csv"  # CSV dosyasının yolu
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Veriyi görüntüleyelim
df.show(5)

# Veriyi hazırlamak için gerekli işlemleri yapalım (Özellik çıkarımı)
# Kullanacağımız özellikler: Open, High, Low, Volume
# Tahmin edeceğimiz hedef değişken: Close

df = df.select("Date", "Open", "High", "Low", "Close", "Volume")

# Tarih bilgisini uygun formata dönüştürme (Zaman serisi için, tarihi kullanmamız gerekebilir)
# Ancak bu örnekte, basit regresyon yapılacak, bu yüzden tarihi kullanmayacağız
df = df.withColumn("Date", col("Date").cast("string"))

# Veriyi eğitime hazırlamak için özellikleri birleştirelim
feature_columns = ['Open', 'High', 'Low', 'Volume']
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
df = assembler.transform(df)

# Hedef değişken (Close) ve özellikler
train_data = df.select("features", "Close")

# Veriyi eğitim ve test olarak ayıralım (80-20 oranında)
train, test = train_data.randomSplit([0.8, 0.2], seed=1234)

# Model oluşturma ve eğitme (LinearRegression)
lr = LinearRegression(featuresCol='features', labelCol='Close')

# Modeli eğitme
lr_model = lr.fit(train)

# Modelin performansını test verisi üzerinde değerlendirme
test_results = lr_model.evaluate(test)
print(f"Root Mean Squared Error (RMSE) : {test_results.rootMeanSquaredError}")
print(f"R2: {test_results.r2}")

# Modeli kaydetme
lr_model.save("tesla_stock_lr_model")

