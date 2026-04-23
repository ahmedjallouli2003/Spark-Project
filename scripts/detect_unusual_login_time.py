from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, hour

spark = SparkSession.builder \
    .appName("Unusual Login Time Detection") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv(
    "/home/ahmed-jallouli/spark-security-project/data/auth_logs.csv",
    header=True,
    inferSchema=True
)

df = df.withColumn(
    "timestamp",
    to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
)

df = df.withColumn(
    "login_hour",
    hour(col("timestamp"))
)

unusual_df = df.filter(
    (col("login_hour") >= 1) & (col("login_hour") <= 4)
)

print("\n=== Unusual Login Time Detection ===")
unusual_df.select(
    "timestamp",
    "username",
    "ip_address",
    "login_status",
    "country",
    "device_type",
    "browser",
    "login_hour"
).show(truncate=False)

unusual_df.write.mode("overwrite").csv(
    "/home/ahmed-jallouli/spark-security-project/output/unusual_login_time_report",
    header=True
)

spark.stop()
