import os
import csv
import uuid
import random
from faker import Faker
from getpass import getuser

fake = Faker()
total_rows = 2_000_000
rows_per_file = 10_000
total_files = total_rows // rows_per_file

user = getuser()
repo = "trade-data-ingest-pipeline-pyspark-cloud"
output_dir = os.getenv("LOCAL_CSV_PATH", f"/tmp/{user}/{repo}/Trade-Events/Local-Dev/Synthetic-Dataset")

os.makedirs(output_dir, exist_ok=True)

existing_keys = set()


def generate_row():
    while True:
        trade_id = str(uuid.uuid4())
        customer_id = str(uuid.uuid4())[:8]
        if (trade_id, customer_id) not in existing_keys:
            existing_keys.add((trade_id, customer_id))
            break

    return {
        "TradeId": trade_id,
        "CustomerId": customer_id,
        "From_Currency": random.choice(["USD", "EUR", "GBP", "JPY", "CAD"]),
        "To_Currency": random.choice(["INR", "CHF", "AUD", "NZD", "ZAR"]),
        "From_Cost": round(random.uniform(10000, 60000), 2),
        "To_Cost": round(random.uniform(10000, 60000), 2),
        "From_Pip": round(random.uniform(40.0, 100.0), 2),
        "To_Pip": round(random.uniform(40.0, 100.0), 2),
        "Transaction_Date": fake.date_time_this_decade().isoformat(),
        "Transaction_Status": random.choice(["COMPLETED", "FAILED", "PENDING"]),
        "Created_By": fake.user_name(),
        "Created_On": fake.date_time_this_decade().isoformat(),
        "Updated_By": fake.user_name(),
        "Updated_on": fake.date_time_this_decade().isoformat(),
        "From_Deposited_Account": fake.iban(),
        "To_Debited_Account": fake.iban()
    }


header = list(generate_row().keys())

for i in range(total_files):
    file_path = os.path.join(output_dir, f"trades_part_{i + 1}.csv")
    with open(file_path, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for _ in range(rows_per_file):
            writer.writerow(generate_row())
    print(f"✅ Done Creating CSV File Trade Event Data file_path {file_path}")

print(f"✅ Generated {total_files} files at {output_dir}")
