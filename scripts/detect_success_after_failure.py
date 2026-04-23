from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, lag, when, count
from pyspark.sql.window import Window

# Create Spark session
spark = SparkSession.builder \
    .appName("Success After Failure Detection") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Load dataset
df = spark.read.csv(
    "/home/ahmed-jallouli/spark-security-project/data/auth_logs.csv",
    header=True,
    inferSchema=True
)

# Convert timestamp
df = df.withColumn(
    "timestamp",
    to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
)

# Define window partition (group by IP + username ordered by time)
window_spec = Window.partitionBy("ip_address", "username").orderBy("timestamp")

# Get previous login status
df = df.withColumn(
    "prev_status",
    lag("login_status").over(window_spec)
)

# Mark suspicious pattern: FAILED → SUCCESS
df = df.withColumn(
    "suspicious_flag",
    when(
        (col("prev_status") == "FAILED") & (col("login_status") == "SUCCESS"),
        1
    ).otherwise(0)
)

# Filter suspicious cases
suspicious_df = df.filter(col("suspicious_flag") == 1)

# Count occurrences per IP and username
result_df = suspicious_df.groupBy("ip_address", "username") \
    .agg(count("*").alias("success_after_failures")) \
    .orderBy(col("success_after_failures").desc())

print("\n=== Success After Failure Detection ===")
result_df.show(truncate=False)

# Save results
result_df.write.mode("overwrite").csv(
    "/home/ahmed-jallouli/spark-security-project/output/success_after_failure_report",
    header=True
)

spark.stop()
