# Spark Security Log Analytics

A PySpark-based security analytics project for detecting suspicious authentication behavior from login logs.

## Project Purpose
This repository demonstrates how to use Apache Spark to process authentication logs at scale and produce actionable security detections, including:

- Brute-force login attempts
- Successful logins immediately following failures
- Logins at unusual hours (01:00–04:59)
- User accounts targeted from multiple distinct IP addresses

## Repository Structure

```text
.
├── data/
│   └── auth_logs.csv
├── scripts/
│   ├── generate_logs.py
│   ├── analyze_logs.py
│   ├── detect_bruteforce.py
│   ├── detect_success_after_failure.py
│   ├── detect_unusual_login_time.py
│   ├── detect_multiple_ips_targeting_user.py
│   └── final_security_report.py
└── README.md
```

## Dataset
The project uses a CSV file at `data/auth_logs.csv` with the following schema:

- `timestamp` (string/timestamp)
- `username` (string)
- `ip_address` (string)
- `login_status` (`SUCCESS` or `FAILED`)
- `device_type` (string)
- `browser` (string)
- `country` (string)
- `response_time` (integer, milliseconds)

### Generate Sample Data
You can regenerate a synthetic dataset (8,900 records) using:

```bash
python3 scripts/generate_logs.py
```

## Detection Scripts

### 1) Baseline analysis
`analyze_logs.py` prints:
- schema and sample rows
- login status distribution
- top failed-login IPs
- most targeted usernames
- failed attempts by username
- hourly login activity

Run:

```bash
spark-submit scripts/analyze_logs.py
```

### 2) Brute-force detection
`detect_bruteforce.py` flags `(ip_address, username)` pairs with **5 or more failed attempts**.

Run:

```bash
spark-submit scripts/detect_bruteforce.py
```

### 3) Success-after-failure detection
`detect_success_after_failure.py` uses a window over `(ip_address, username)` ordered by timestamp and flags `FAILED -> SUCCESS` transitions.

Run:

```bash
spark-submit scripts/detect_success_after_failure.py
```

### 4) Unusual login time detection
`detect_unusual_login_time.py` filters events where login hour is between **1 and 4**.

Run:

```bash
spark-submit scripts/detect_unusual_login_time.py
```

### 5) Multiple IPs targeting one user
`detect_multiple_ips_targeting_user.py` flags usernames accessed from **3+ distinct IPs**.

Run:

```bash
spark-submit scripts/detect_multiple_ips_targeting_user.py
```

### 6) Consolidated report
`final_security_report.py` executes all four detections in one run.

Run:

```bash
spark-submit scripts/final_security_report.py
```

## Output Reports
Each detection writes a CSV output folder (Spark format with part files) under `output/`:

- `output/bruteforce_report/`
- `output/success_after_failure_report/`
- `output/unusual_login_time_report/`
- `output/multiple_ips_targeting_user_report/`

> Note: some scripts currently use absolute paths (e.g., `/home/ahmed-jallouli/spark-security-project/...`). If your environment differs, update these paths to your local repository location.

## Requirements
- Python 3.8+
- Apache Spark 3.x
- PySpark

Install PySpark (if needed):

```bash
pip install pyspark
```

## Quick Start

```bash
# 1) Optional: regenerate sample logs
python3 scripts/generate_logs.py

# 2) Run the consolidated detection pipeline
spark-submit scripts/final_security_report.py
```

## Author
Ahmed Jallouli
