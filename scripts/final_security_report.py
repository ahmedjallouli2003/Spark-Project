from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    countDistinct,
    to_timestamp,
    hour,
    lag,
    when
)
from pyspark.sql.window import Window

# Create Spark session
spark = SparkSession.builder \
    .appName("Final Security Analytics Report") \
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

# Extract login hour
df = df.withColumn(
    "login_hour",
    hour(col("timestamp"))
)

print("\n=== Full Dataset Preview ===")
df.show(10, truncate=False)

# =========================================================
# 1. Brute-force detection
# =========================================================
failed_df = df.filter(col("login_status") == "FAILED")

bruteforce_df = failed_df.groupBy("ip_address", "username") \
    .agg(count("*").alias("failed_attempts")) \
    .filter(col("failed_attempts") >= 5) \
    .orderBy(col("failed_attempts").desc())

print("\n=== Brute-Force Detection ===")
bruteforce_df.show(truncate=False)

bruteforce_df.write.mode("overwrite").csv(
    "/home/ahmed-jallouli/spark-security-project/output/bruteforce_report",
    header=True
)

# =========================================================
# 2. Success after repeated failures
# =========================================================
window_spec = Window.partitionBy("ip_address", "username").orderBy("timestamp")

sequence_df = df.withColumn(
    "prev_status",
    lag("login_status").over(window_spec)
)

sequence_df = sequence_df.withColumn(
    "suspicious_flag",
    when(
        (col("prev_status") == "FAILED") & (col("login_status") == "SUCCESS"),
        1
    ).otherwise(0)
)

success_after_failure_df = sequence_df.filter(col("suspicious_flag") == 1) \
    .groupBy("ip_address", "username") \
    .agg(count("*").alias("success_after_failures")) \
    .orderBy(col("success_after_failures").desc())

print("\n=== Success After Failure Detection ===")
success_after_failure_df.show(truncate=False)

success_after_failure_df.write.mode("overwrite").csv(
    "/home/ahmed-jallouli/spark-security-project/output/success_after_failure_report",
    header=True
)

# =========================================================
# 3. Unusual login time detection
# =========================================================
unusual_time_df = df.filter(
    (col("login_hour") >= 1) & (col("login_hour") <= 4)
).select(
    "timestamp",
    "username",
    "ip_address",
    "login_status",
    "country",
    "device_type",
    "browser",
    "login_hour"
)

print("\n=== Unusual Login Time Detection ===")
unusual_time_df.show(truncate=False)

unusual_time_df.write.mode("overwrite").csv(
    "/home/ahmed-jallouli/spark-security-project/output/unusual_login_time_report",
    header=True
)

# =========================================================
# 4. Multiple IPs targeting one account
# =========================================================
multiple_ips_df = df.groupBy("username") \
    .agg(countDistinct("ip_address").alias("distinct_ip_count")) \
    .filter(col("distinct_ip_count") >= 3) \
    .orderBy(col("distinct_ip_count").desc())

print("\n=== Multiple IPs Targeting One Account ===")
multiple_ips_df.show(truncate=False)

multiple_ips_df.write.mode("overwrite").csv(
    "/home/ahmed-jallouli/spark-security-project/output/multiple_ips_targeting_user_report",
    header=True
)

spark.stop()
