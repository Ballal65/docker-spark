from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkBatch") \
    .master("spark://spark-master:7077") \
    .config("spark.jars", "/opt/spark/jars/spark-sql-kafka-0-10_2.12-3.2.1.jar,/opt/spark/jars/kafka-clients-3.2.1.jar") \
    .config("spark.driver.extraClassPath", "/opt/spark/jars/spark-sql-kafka-0-10_2.12-3.2.1.jar:/opt/spark/jars/kafka-clients-3.2.1.jar") \
    .config("spark.executor.extraClassPath", "/opt/spark/jars/spark-sql-kafka-0-10_2.12-3.2.1.jar:/opt/spark/jars/kafka-clients-3.2.1.jar") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

# Verify configuration
print("Spark Version:", spark.version)
print("Driver Extra Classpath:", spark.conf.get("spark.driver.extraClassPath"))
print("Executor Extra Classpath:", spark.conf.get("spark.executor.extraClassPath"))

# Read from Kafka
kafka_df = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "AIDHOOSTATION") \
    .option("startingOffsets", "earliest") \
    .option("endingOffsets", "latest") \
    .load()

# Process data
processed_df = kafka_df.select(
    col("key").cast("string").alias("key"),
    col("value").cast("string").alias("value"),
    col("timestamp"),
    col("partition"),
    col("offset")
)

# Show results
processed_df.show(truncate=False)

# Optional: Save to CSV
processed_df.write \
    .mode("overwrite") \
    .csv("/opt/spark/output/AIDHOOSTATION_batch_output")

spark.stop()