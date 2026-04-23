from pyspark.sql import SparkSession
from pyspark.sql.functions import col, countDistinct, to_timestamp

spark = SparkSession.builder \
    .appName("Multiple IPs Targeting One Account Detection") \
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

targeted_users_df = df.groupBy("username") \
    .agg(countDistinct("ip_address").alias("distinct_ip_count")) \
    .filter(col("distinct_ip_count") >= 3) \
    .orderBy(col("distinct_ip_count").desc())

print("\n=== Multiple IPs Targeting One Account Detection ===")
targeted_users_df.show(truncate=False)

targeted_users_df.write.mode("overwrite").csv(
    "/home/ahmed-jallouli/spark-security-project/output/multiple_ips_targeting_user_report",
    header=True
)

spark.stop()
