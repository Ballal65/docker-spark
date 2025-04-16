from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Initialize Spark Session with Kafka dependencies
spark = SparkSession.builder \
    .appName("KafkaSparkBatch") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

print("Spark Version:", spark.version)

# Read from Kafka
kafka_df = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "AIDHOOSTATION") \
    .option("startingOffsets", "earliest") \
    .option("endingOffsets", "latest") \
    .load()

# Process Kafka data
processed_df = kafka_df.select(
    col("key").cast("string").alias("key"),
    col("value").cast("string").alias("value"),
    col("timestamp"),
    col("partition"),
    col("offset")
)

# Show processed data
processed_df.show(truncate=False)

# Write output to CSV
processed_df.write.mode("overwrite").csv("/opt/spark/output/AIDHOOSTATION_batch_output")

# Stop Spark session
spark.stop()