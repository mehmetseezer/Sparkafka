from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegressionModel  # LinearRegressionModel'ı içe aktar
import os

# Spark Streaming için Kafka bağlantısını konfigüre et
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 pyspark-shell'

# SparkSession başlatma
spark = SparkSession.builder \
    .appName("KafkaStockPrediction") \
    .getOrCreate()

# Kafka'dan veri okuma
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "tesla-data") \
    .load()

# Kafka'dan gelen veriyi string'e dönüştürme
kafka_df = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Mesaj formatını JSON olarak çözüyoruz (veri şeması)
json_schema = 'struct<date:string, open:double, high:double, low:double, close:double, volume:long>'
processed_df = kafka_df.withColumn("json_value", from_json(kafka_df['value'], json_schema)) \
    .select("json_value.*")

# Veriyi işleme (özellikler)
feature_columns = ['open', 'high', 'low', 'volume']
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
processed_df = assembler.transform(processed_df)

# LinearRegressionModel yükleme (önceden eğitilmiş model)
loaded_model = LinearRegressionModel.load("tesla_stock_lr_model")  # PipelineModel yerine LinearRegressionModel kullanıldı

# Model ile tahmin yapma
predictions = loaded_model.transform(processed_df)

# Tahmin sonuçlarını seçme (gerekirse daha fazla işlem yapılabilir)
predictions = predictions.select("date", "open", "high", "low", "volume", "close", "prediction")

# Tahminleri konsola yazdırma
query = predictions \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .trigger(processingTime='1 seconds') \
    .start()

# Streaming işlemi çalışmaya devam etsin
query.awaitTermination()
