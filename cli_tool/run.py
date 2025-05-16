import os
import sys
import click
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from spark_pipeline import config, ingest


@click.command()
@click.option('--env', default=".env", help='Path to the environment file.')
@click.option('--mode', default="local", help='Execution mode: local | emr | airflow | notebook')
def run(env, mode):
    """Run trade data ingestion job locally (from CSV to PostgreSQL)."""
    load_dotenv(env)
    
    # Only local mode supported in this runner
    if mode != "local":
        print(f"Unsupported mode for this runner: {mode}")
        sys.exit(1)

    print("Starting local ingestion job...")

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("TradeDataIngestLocal") \
        .getOrCreate()

    # Load config from env
    source_csv_path = os.getenv("LOCAL_CSV_PATH")  # e.g., ./DevOps/Local-Dev/Dataset/*.csv
    postgres_url = config.build_postgres_jdbc_url()
    db_table = os.getenv("POSTGRES_TABLE", "Trade_Event")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")

    # Run ingestion
    df = ingest.read_trade_csv(spark, source_csv_path)
    ingest.write_to_postgres(df, postgres_url, db_table, db_user, db_pass)

    print("✅ Ingestion job completed successfully.")
    spark.stop()


if __name__ == '__main__':
    run()
