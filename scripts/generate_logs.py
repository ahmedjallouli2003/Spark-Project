import csv
import random
from datetime import datetime, timedelta

users = ["ahmed", "sarah", "admin", "yassine", "amine", "guest"]
devices = ["Laptop", "Mobile", "Desktop", "Tablet"]
browsers = ["Chrome", "Firefox", "Edge", "Safari"]
normal_ips = ["192.168.1.10", "192.168.1.15", "192.168.1.20", "10.0.0.5", "10.0.0.8"]
suspicious_ips = ["203.0.113.50", "198.51.100.23", "45.67.89.10"]

start_time = datetime(2026, 4, 1, 0, 0, 0)
rows = []

# 1. Normal activity
for _ in range(8000):
    ts = start_time + timedelta(minutes=random.randint(0, 60 * 24 * 20))
    username = random.choice(users)
    ip = random.choice(normal_ips)
    status = random.choices(["SUCCESS", "FAILED"], weights=[85, 15])[0]
    device = random.choice(devices)
    browser = random.choice(browsers)
    country = random.choice(["Tunisia", "Tunisia", "Tunisia", "France"])
    response_time = random.randint(50, 300)

    rows.append([
        ts.strftime("%Y-%m-%d %H:%M:%S"),
        username,
        ip,
        status,
        device,
        browser,
        country,
        response_time
    ])

# 2. Brute-force failed attempts
for _ in range(300):
    ts = start_time + timedelta(minutes=random.randint(0, 60 * 24 * 20))
    username = random.choice(["admin", "ahmed", "sarah"])
    ip = random.choice(suspicious_ips)
    status = "FAILED"
    device = "Desktop"
    browser = random.choice(browsers)
    country = random.choice(["Germany", "USA"])
    response_time = random.randint(80, 250)

    rows.append([
        ts.strftime("%Y-%m-%d %H:%M:%S"),
        username,
        ip,
        status,
        device,
        browser,
        country,
        response_time
    ])

# 3. Success after repeated failures
for _ in range(100):
    base_ts = start_time + timedelta(minutes=random.randint(0, 60 * 24 * 20))
    username = random.choice(["admin", "ahmed"])
    ip = random.choice(suspicious_ips)

    for i in range(3):
        rows.append([
            (base_ts + timedelta(seconds=i * 20)).strftime("%Y-%m-%d %H:%M:%S"),
            username,
            ip,
            "FAILED",
            "Desktop",
            "Chrome",
            "Germany",
            random.randint(70, 200)
        ])

    rows.append([
        (base_ts + timedelta(seconds=70)).strftime("%Y-%m-%d %H:%M:%S"),
        username,
        ip,
        "SUCCESS",
        "Desktop",
        "Chrome",
        "Germany",
        random.randint(70, 200)
    ])

# 4. Unusual-hour events
for _ in range(200):
    day = random.randint(1, 20)
    hour = random.choice([1, 2, 3, 4])
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    ts = datetime(2026, 4, day, hour, minute, second)

    rows.append([
        ts.strftime("%Y-%m-%d %H:%M:%S"),
        random.choice(users),
        random.choice(suspicious_ips),
        random.choice(["SUCCESS", "FAILED"]),
        random.choice(devices),
        random.choice(browsers),
        random.choice(["USA", "Germany"]),
        random.randint(60, 280)
    ])

with open("data/auth_logs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "timestamp", "username", "ip_address", "login_status",
        "device_type", "browser", "country", "response_time"
    ])
    writer.writerows(rows)

print(f"Generated {len(rows)} log records into data/auth_logs.csv")
