from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, to_timestamp, hour

spark = SparkSession.builder \
    .appName("Brute Force Detection") \
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

failed_df = df.filter(col("login_status") == "FAILED")

bruteforce_df = failed_df.groupBy("ip_address", "username") \
    .agg(count("*").alias("failed_attempts")) \
    .filter(col("failed_attempts") >= 5) \
    .orderBy(col("failed_attempts").desc())

print("\n=== Possible Brute-Force Attacks ===")
bruteforce_df.show(truncate=False)

bruteforce_df.write.mode("overwrite").csv(
    "/home/ahmed-jallouli/spark-security-project/output/bruteforce_report",
    header=True
)

spark.stop()
