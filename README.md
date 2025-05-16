# Trade Data Ingest Pipeline (PySpark + Cloud)
A cloud-agnostic data ingestion pipeline built using Apache PySpark. It is designed to ingest historical trade event data from distributed CSV files stored in various cloud object storage platforms (e.g., Azure Blob Storage, AWS S3, Google Cloud Storage) and persist them into a structured PostgreSQL database for downstream analytics and reporting

# Introduction

A modular, enterprise-grade data ingestion pipeline that ingests historical trade event data from CSV files and stores it into a PostgreSQL database. The system supports PySpark ingestion from local or cloud sources (Azure Blob, AWS S3, GCP GCS, Databricks), provides a Flask backend API, Angular frontend for monitoring, and can run as a CLI, Apache Airflow DAG, or on cloud-native Spark platforms.

---

## Architectural Overview

This pipeline is structured to support a wide range of environments, development styles, and orchestration layers, making it adaptable for both exploratory and production-scale workloads.

**Flexibility**: Built to support multiple execution contexts including CLI tools, Apache Airflow DAGs, interactive notebooks, and REST APIs with minimal changes to the core logic.

**Portability**: Designed for seamless operation across local setups, on-premise clusters, and major cloud platforms such as AWS, Azure, GCP, and Databricks.

### Design Highlights

- **Core Logic Isolation**  
  The PySpark ingestion logic is encapsulated in reusable modules, allowing you to plug it into:
  - CLI scripts for local testing
  - Airflow DAGs for production
  - Notebooks for experimentation
  - Cloud job definitions for Spark-native environments

- **Modular Runtime Support**
  - **CLI Tool**: Easily trigger ingestion locally via `npm run ingest:data`
  - **Airflow DAG**: Integrate the same logic for production pipelines
  - **Jupyter / Databricks**: Run the pipeline inside interactive notebooks
  - **Cloud Spark Engines**: Submit as jobs to EMR, Synapse, Dataproc, or Databricks clusters

- **API Layer (Flask)**  
  A Flask-based backend provides REST endpoints to expose ingestion metrics, pipeline status, and historical logs (planned extension).

- **Frontend Layer (Angular)**  
  An Angular frontend (optional) will be added to visualize ingestion progress, per-file metrics, and errors in real-time.

- **DevOps-Ready Setup**  
  Includes Docker Compose configurations for:
  - PostgreSQL database (for trade and batch tables)
  - Apache Airflow (for future orchestration flows)
  - Volume mounts and local dataset emulation

This architecture ensures consistent behavior regardless of the environment you're running in—local or cloud, batch or interactive, manual or automated.

---

## Value Proposition

This repository is ideal for teams looking to:

- Backfill or batch-ingest large-scale financial trade data.
- Standardize ingestion pipelines across multiple cloud platforms.
- Monitor and audit ingestion through a web dashboard.
- Experiment interactively with trade data via notebooks.
- Integrate ingestion into a broader enterprise data lake or warehouse architecture.

With its highly modular and pluggable design, this codebase can adapt to a variety of data platform setups and is ready for enterprise-scale deployment.

---

## Tech Stack

- **PySpark** for high-performance distributed data processing
- **PostgreSQL** as the landing zone for structured trade events
- **Flask** for backend API services
- **Angular** for the frontend dashboard
- **Apache Airflow** for orchestration
- **Docker Compose** for local infrastructure emulation

---

## Development Modes

- Run locally via CLI: `python cli_tool/run.py`
- Run interactively in a Jupyter or Databricks notebook
- Schedule with Airflow: use the `airflow_dags/trade_ingest_dag.py`
- Submit to cloud platforms using job templates in `cloud_jobs/`

---
