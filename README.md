# Distributed Authentication Log Analysis with Apache Spark

## Project Overview
This project implements a distributed security analytics system using Apache Spark to detect suspicious login behavior from authentication logs.

## Features
- Brute-force attack detection
- Success-after-failure detection
- Unusual login time detection
- Multiple IPs targeting one account detection

## Technologies
- Apache Spark
- PySpark
- Ubuntu Virtual Machines
- Spark Standalone Cluster

## Architecture
- 1 Master Node
- 2 Worker Nodes
- Distributed data processing

## How to Run
```bash
spark-submit --master spark://<MASTER_IP>:7077 scripts/final_security_report.py

##Author

Ahmed Jallouli
