from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from spark_pipeline.config import get_spark_session
import os
import uuid
import random
from datetime import datetime
from getpass import getuser
import shutil
from pyspark.sql.functions import lit, col
from pyspark.sql.types import DoubleType, TimestampType

from dotenv import load_dotenv
load_dotenv()

def get_default_synthetic_path():
    user = getuser()
    repo = "trade-data-ingest-pipeline-pyspark-cloud"
    return f"/tmp/{user}/{repo}/Trade-Events/Local-Dev/Synthetic-Dataset"

def get_backup_path(batch_id):
    user = getuser()
    repo = "trade-data-ingest-pipeline-pyspark-cloud"
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    return f"/tmp/{user}/{repo}/Trade-Events/Local-Dev/Synthetic-Dataset-Backup/{timestamp}/{batch_id}"

def read_trade_csv(spark: SparkSession, path: str) -> DataFrame:
    print(f"Reading trade data from: {path}")
    return spark.read.option("header", "true").csv(path)

def write_to_postgres(df: DataFrame, jdbc_url: str, table: str, user: str, password: str):
    print("Writing to PostgreSQL with:")
    print(f"  URL     : {jdbc_url}")
    print(f"  Table   : {table}")
    print(f"  User    : {user}")
    print(f"  Password: {'***' if password else 'None'}")

    if not all([jdbc_url, table, user, password]):
        raise ValueError("❌ One or more required JDBC parameters are missing!")

    df.write \
      .format("jdbc") \
      .option("url", jdbc_url) \
      .option("dbtable", table) \
      .option("user", user) \
      .option("password", password) \
      .option("driver", "org.postgresql.Driver") \
      .mode("append") \
      .save()

def log_ingest_metadata(spark: SparkSession, file_path: str, row_count: int, jdbc_url: str, db_user: str, db_pass: str) -> (str, int, datetime):
    ingest_id = str(uuid.uuid4())
    now = datetime.now()
    concurrent_number = random.randint(1, 20)

    metadata = [(ingest_id, os.path.basename(file_path), row_count, now, "COMPLETED", now, now, now, concurrent_number)]
    columns = [
        "id", "file_name", "row_count", "created_dt", "ingest_status",
        "ingest_start_date_time", "ingest_end_date_time", "updated_dt", "concurrent_number"
    ]

    meta_df = spark.createDataFrame(metadata, columns)
    write_to_postgres(meta_df, jdbc_url, "TRADE_EVENT_INGEST_BATCH", db_user, db_pass)
    return ingest_id, concurrent_number, now

def enrich_and_store_trade_events(df: DataFrame, batch_id: str, batch_cc: int, ingest_time: datetime, jdbc_url: str, db_user: str, db_pass: str):
    event_cc = random.randint(1, 20)

    enriched_df = df \
        .withColumn("From_Cost", col("From_Cost").cast(DoubleType())) \
        .withColumn("To_Cost", col("To_Cost").cast(DoubleType())) \
        .withColumn("From_Pip", col("From_Pip").cast(DoubleType())) \
        .withColumn("To_Pip", col("To_Pip").cast(DoubleType())) \
        .withColumn("Transaction_Date", col("Transaction_Date").cast(TimestampType())) \
        .withColumn("Created_On", col("Created_On").cast(TimestampType())) \
        .withColumn("Updated_on", col("Updated_on").cast(TimestampType())) \
        .withColumn("batch_id", lit(batch_id)) \
        .withColumn("batch_concurrent_number", lit(batch_cc)) \
        .withColumn("ingest_date", lit(ingest_time)) \
        .withColumn("concurrent_number", lit(event_cc)) \
        .withColumn("TradeId", col("TradeId")) \
        .withColumn("CustomerId", col("CustomerId"))

    enriched_df = enriched_df.dropDuplicates(["TradeId", "CustomerId"])

    write_to_postgres(enriched_df, jdbc_url, "TRADE_EVENT", db_user, db_pass)

def move_to_backup(file_path: str, batch_id: str):
    backup_dir = get_backup_path(batch_id)
    os.makedirs(backup_dir, exist_ok=True)
    shutil.move(file_path, os.path.join(backup_dir, os.path.basename(file_path)))
    print(f"Moved {file_path} to {backup_dir}")

if __name__ == '__main__':
    spark = get_spark_session("TradeIngestJob")

    input_path = os.getenv("LOCAL_CSV_PATH", get_default_synthetic_path())
    jdbc_url = os.getenv("POSTGRES_JDBC_URL")
    db_table = os.getenv("POSTGRES_TABLE", "Trade_Event")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")

    if not jdbc_url:
        from spark_pipeline.config import build_postgres_jdbc_url
        jdbc_url = build_postgres_jdbc_url()

    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith(".csv"):
                full_path = os.path.join(input_path, filename)
                df = read_trade_csv(spark, full_path)

                if df.rdd.isEmpty():
                    print(f"Skipping empty file: {filename}")
                    continue

                df = df \
                    .withColumn("From_Cost", col("From_Cost").cast(DoubleType())) \
                    .withColumn("To_Cost", col("To_Cost").cast(DoubleType())) \
                    .withColumn("From_Pip", col("From_Pip").cast(DoubleType())) \
                    .withColumn("To_Pip", col("To_Pip").cast(DoubleType())) \
                    .withColumn("Transaction_Date", col("Transaction_Date").cast(TimestampType())) \
                    .withColumn("Created_On", col("Created_On").cast(TimestampType())) \
                    .withColumn("Updated_on", col("Updated_on").cast(TimestampType()))

                df = df.dropDuplicates(["TradeId", "CustomerId"])

                write_to_postgres(df, jdbc_url, db_table, db_user, db_pass)
                batch_id, batch_cc, ingest_time = log_ingest_metadata(spark, full_path, df.count(), jdbc_url, db_user, db_pass)
                enrich_and_store_trade_events(df, batch_id, batch_cc, ingest_time, jdbc_url, db_user, db_pass)
                move_to_backup(full_path, batch_id)
    else:
        print(f"Provided input path does not exist or is not a directory: {input_path}")

    print("Ingestion complete.")
    spark.stop()