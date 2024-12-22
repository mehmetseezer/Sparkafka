import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.ml.feature import VectorAssembler
import tensorflow as tf
import numpy as np
import pandas as pd
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
import json

# Kafka ve Spark yapılandırması
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 pyspark-shell'

# Spark oturumunu başlat
spark = SparkSession.builder \
    .appName("KafkaSparkIntegrationWithML") \
    .config("spark.executor.instances", "4") \
    .config("spark.executor.cores", "2") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

# Modeli yükle (Keras modelini .h5 dosyasından)
model = tf.keras.models.load_model('tesla_stock_model.h5')

# Kafka'dan veri okuma
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "tesla-data") \
    .option("maxOffsetsPerTrigger", 1000).load()

# 'value' kolonundaki veriyi string'e dönüştürme
kafka_df = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Mesaj formatını JSON olarak çözüyoruz (veri tipini belirlemek için)
json_schema = 'struct<date:string, open:double, high:double, low:double, close:double, volume:long>'
processed_df = kafka_df.withColumn("json_value", from_json(kafka_df['value'], json_schema)) \
    .select("json_value.*")

# Özelliklerin belirlenmesi
feature_columns = ['open', 'high', 'low', 'volume']

# Özellikleri vektöre dönüştürmek için VectorAssembler kullanıyoruz
assembler = VectorAssembler(inputCols=feature_columns, outputCol="assembled_features")

def process_batch(batch_df, batch_id):
    if batch_df.count() == 0:
        return

    # Özellikleri vektöre dönüştürme
    assembled_df = assembler.transform(batch_df)
    
    # Pandas DataFrame'e dönüştürme (TensorFlow'a input formatı için)
    pandas_df = assembled_df.select('open', 'high', 'low', 'volume').toPandas()

    # Model için uygun input formatına dönüştürme
    features = pandas_df.values
    
    # Modeli kullanarak tahmin yapma
    predictions = model.predict(features)

    # Gerçek 'close' değerini alıyoruz
    real_close = pandas_df['close'].values
    
    # Karşılaştırma yapalım
    for i in range(len(predictions)):
        print(f"Date: {batch_df.collect()[i]['date']}")
        print(f"Real Close: {real_close[i]}")
        print(f"Predicted Close: {predictions[i]}")
        print(f"Difference: {abs(real_close[i] - predictions[i])}\n")
    
    # Başarı metriklerini hesaplayalım (RMSE, MSE, MAE, R2)
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    mse = mean_squared_error(real_close, predictions)
    mae = mean_absolute_error(real_close, predictions)
    r2 = r2_score(real_close, predictions)
    rmse = np.sqrt(mse)

    # Sonuçları yazdırma
    print(f"Batch ID: {batch_id}")
    print(f"RMSE: {rmse}")
    print(f"MSE: {mse}")
    print(f"MAE: {mae}")
    print(f"R2: {r2}")

# Veriyi streaming olarak işleyip sonuçları konsola yazdırıyoruz
query = processed_df \
    .writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .trigger(processingTime='10 seconds') \
    .start()

# Streaming işlemi çalışmaya devam etsin
query.awaitTermination()
