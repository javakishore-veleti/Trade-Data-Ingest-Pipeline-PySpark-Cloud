import os
from pyspark.sql import SparkSession

def build_postgres_jdbc_url():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db   = os.getenv("POSTGRES_DB", "tradedb")
    return f"jdbc:postgresql://{host}:{port}/{db}"

def get_spark_session(app_name="TradeDataIngest"):
    cloud = os.getenv("CLOUD_PROVIDER", "local").lower()
    master = os.getenv("SPARK_MASTER_URL", "local[*]")
    print(f"CLOUD_PROVIDER = {cloud}")
    print(f"SPARK_MASTER = {master}")

    builder = SparkSession.builder.appName(app_name).master(master)

    # Optional: Add external JARs (e.g. JDBC driver)
    jar_path = os.getenv("SPARK_EXTRA_JARS")
    if jar_path:
        print(f"Including JAR: {jar_path}")
        builder = builder.config("spark.jars", jar_path)

    # AWS EMR Configuration
    if cloud == "emr":
        print("Configuring for AWS EMR")
        os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID", "")
        os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY", "")
        os.environ["AWS_REGION"] = os.getenv("AWS_REGION", "us-east-1")

    # Azure Configuration
    elif cloud == "azure":
        print("Configuring Azure credentials...")
        storage_account = os.getenv("AZURE_STORAGE_ACCOUNT")
        storage_key = os.getenv("AZURE_STORAGE_KEY")
        if storage_account and storage_key:
            builder = builder.config(
                f"fs.azure.account.key.{storage_account}.blob.core.windows.net", storage_key
            )

    # GCP Configuration
    elif cloud == "gcp":
        print("Configuring GCP access — ensure gcloud auth and Hadoop connector are in place.")
        # Add gcloud-specific configs here if needed

    # Databricks (no extra config usually needed)
    elif cloud == "databricks":
        print("Running on Databricks")

    # Local
    else:
        print("Using local Spark context")

    return builder.getOrCreate()