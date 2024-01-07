#consumer code
#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from elasticsearch import Elasticsearch
sessions = SparkSession._instantiatedSession
if sessions is not None:
    sessions.stop()
# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Create Spark Session
spark = SparkSession.builder \
    .appName("consumer") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Define schema of data retrieved from the producer velib_stations
schema = StructType([
    StructField("numbers", IntegerType(), True),
    StructField("contract_name", StringType(), True),
    StructField("banking", StringType(), True),
    StructField("bike_stands", IntegerType(), True),
    StructField("available_bike_stands", IntegerType(), True),
    StructField("available_bikes", IntegerType(), True),
    StructField("address", StringType(), True),
    StructField("status", StringType(), True),
    StructField("position", StructType([
        StructField("lat", DoubleType(), True),
        StructField("lng", DoubleType(), True)
    ]), True),
    StructField("last_update", StringType(), True),  
])
print("Reading data from Kafka...")
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "velib-stations") \
    .option("startingOffsets", "latest") \
    .load()
print("Data read from Kafka successfully.")
# Process JSON data
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

# Update your schema if needed
#json_df = json_df.withColumn("position", col("position").alias("position").cast("struct<lat:double, lng:double>"))
json_df = json_df.withColumn("position", struct("position.lat", "position.lng").alias("position").cast("struct<lat:double, lon:double>"))

# Write to Elasticsearch
data = json_df.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .outputMode("append") \
    .option("es.nodes", "127.0.0.1") \
    .option("es.port", "9200") \
    .option("es.index.auto.create", "true") \
    .option("es.resource", "stations") \
    .option("es.nodes.wan.only", "true") \
    .option("checkpointLocation", "/home/chayma/Bureau/checkpoints/new11") \
    .start()
    
data.awaitTermination()


