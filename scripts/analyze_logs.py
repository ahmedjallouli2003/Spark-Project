from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, hour, to_timestamp

# Create Spark session
spark = SparkSession.builder \
    .appName("Authentication Log Analysis") \
    .getOrCreate()

# Load CSV file
df = spark.read.csv("data/auth_logs.csv", header=True, inferSchema=True)

# Convert timestamp column to proper timestamp type
df = df.withColumn("timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss"))

# Extract login hour
df = df.withColumn("login_hour", hour(col("timestamp")))

print("\n=== Schema ===")
df.printSchema()

print("\n=== First 10 Rows ===")
df.show(10, truncate=False)

# Total number of records
total_records = df.count()
print(f"\nTotal log records: {total_records}")

# Count by login status
print("\n=== Login Status Counts ===")
df.groupBy("login_status").count().show()

# Top IPs with failed attempts
print("\n=== Top Failed Login IPs ===")
df.filter(col("login_status") == "FAILED") \
  .groupBy("ip_address") \
  .count() \
  .orderBy(col("count").desc()) \
  .show(10, truncate=False)

# Most targeted usernames
print("\n=== Most Targeted Usernames ===")
df.groupBy("username") \
  .count() \
  .orderBy(col("count").desc()) \
  .show(10, truncate=False)

# Failed attempts by username
print("\n=== Failed Attempts by Username ===")
df.filter(col("login_status") == "FAILED") \
  .groupBy("username") \
  .count() \
  .orderBy(col("count").desc()) \
  .show(10, truncate=False)

# Login activity by hour
print("\n=== Login Activity by Hour ===")
df.groupBy("login_hour") \
  .count() \
  .orderBy("login_hour") \
  .show(24, truncate=False)

spark.stop()
