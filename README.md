# Trade Data Ingest Pipeline (PySpark + Cloud)

This project implements a scalable and cloud-portable data ingestion pipeline using PySpark to load trade event CSVs into Postgres SQL. It supports synthetic data generation, batch metadata tracking, backup organization, and can run across local and cloud environments with minimal reconfiguration.

---

## What It Does

- Reads synthetic trade event data from CSV files
- Ingests enriched rows into Postgres SQL
- Tracks metadata in a batch table for every ingested file
- Moves processed files into timestamped backup directories
- Can run in local Spark or be submitted to cloud platforms
- Designed to support CLI, Airflow, notebooks, or REST API execution

---

## Features

- Generates 2 million rows of synthetic trade events (across 200 CSV files)
- Each `(TradeId, CustomerId)` pair is globally unique to prevent duplicate keys
- Data is typecast to align with the Postgres SQL schema
- Batch ingestion metadata includes file name, row count, status, timestamps, and a random concurrent number
- All processed files are archived for traceability

---

## Code Structure

- `spark_pipeline/`: Core PySpark logic and ingestion routines
- `cli_tool/generate_synthetic_trade_data.py`: Safe generator with composite key uniqueness
- `DevOps/Local-Dev/Containers/`: Docker Compose setup for Postgres SQL and optional Airflow
- `DevOps/Local-Dev/Dataset/`: Dataset examples and volume paths
- `.env`: Spark, cloud, and database environment configuration

---

## Environment Setup

```bash
cp .env.example .env
pip install -r requirements.txt
```

Make sure you have:
- Python 3.11
- Java 11 (run: `export JAVA_HOME=$(/usr/libexec/java_home -v 11)`)
- Spark installed and `spark-submit` available in PATH

---

## Synthetic Data Generation

This script ensures unique `(TradeId, CustomerId)` across all files:

```bash
python cli_tool/generate_synthetic_trade_data.py
```

This generates 200 CSV files (10,000 rows each) into:

```
/tmp/<user>/trade-data-ingest-pipeline-pyspark-cloud/Trade-Events/Local-Dev/Synthetic-Dataset/
```

To clean previous runs:

```bash
npm run clean:synthetic
npm run clean:synthetic:backup
```

---

## Ingesting Data

To run the ingestion pipeline locally:

```bash
npm run ingest:data
```

This will:

- Read all `.csv` files in the synthetic dataset folder
- Drop duplicate `(TradeId, CustomerId)` pairs before insert
- Write enriched records to the event table
- Log file-level metadata into a batch table
- Move completed files to back up folders organized by timestamp and batch ID

---

## Utility Scripts

Available under `package.json`:

```json
"scripts": {
  "ingest:data": "./prepare_ingestion.sh",
  "clean:synthetic": "rm -rf /tmp/$(whoami)/trade-data-ingest-pipeline-pyspark-cloud/Trade-Events/Local-Dev/Synthetic-Dataset/*",
  "clean:synthetic:backup": "rm -rf /tmp/$(whoami)/trade-data-ingest-pipeline-pyspark-cloud/Trade-Events/Local-Dev/Synthetic-Dataset-Backup/*"
}
```

---

## Architectural Overview

This pipeline is built to support a wide range of development and deployment styles, with minimal changes across environments.

**Flexibility**: Built to support multiple execution contexts including CLI tools, Apache Airflow DAGs, notebooks, and REST APIs.

**Portability**: Designed to work seamlessly across local setups, on-premise Spark clusters, and cloud platforms like AWS, Azure, GCP, and Databricks.

### Design Highlights

- **Core Logic Isolation**: PySpark logic is modular and reusable across multiple execution environments
- **Modular Runtimes**:
  - CLI tool for local testing and automation
  - Airflow DAG integration for production pipelines
  - Notebook compatibility for interactive workflows
  - Job submission scripts for EMR, Synapse, Dataproc, and Databricks
- **API Layer**: Flask backend provides endpoints to monitor ingestion state (planned)
- **Frontend Layer**: Angular dashboard for displaying job stats and metrics (planned)
- **DevOps Ready**: Docker Compose configurations for Postgres SQL and Airflow included

---

## Next Steps

- Implement Airflow DAG wrapping the PySpark logic
- Expose job and ingestion metrics via Flask API
- Visualize ingestion progress and metrics with Angular
- Add schema validation layer before ingestion

---

This project is designed for cloud-native ingestion scenarios and fast local iteration, making it suitable for teams working across hybrid or multi-cloud data environments.
