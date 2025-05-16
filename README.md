# Trade Data Ingest Pipeline (PySpark + Cloud)
A cloud-agnostic data ingestion pipeline built using Apache PySpark. It is designed to ingest historical trade event data from distributed CSV files stored in various cloud object storage platforms (e.g., Azure Blob Storage, AWS S3, Google Cloud Storage) and persist them into a structured PostgreSQL database for downstream analytics and reporting

# Introduction

A modular, enterprise-grade data ingestion pipeline that ingests historical trade event data from CSV files and stores it into a PostgreSQL database. The system supports PySpark ingestion from local or cloud sources (Azure Blob, AWS S3, GCP GCS, Databricks), provides a Flask backend API, Angular frontend for monitoring, and can run as a CLI, Apache Airflow DAG, or on cloud-native Spark platforms.

---

## Architectural Overview

**Flexibility**: Built to support multiple execution contexts such as CLI, Airflow, notebooks, and REST APIs with minimal code changes.

**Portability**: Designed to run seamlessly across local setups, on-premise clusters, and major cloud platforms including AWS, Azure, GCP, and Databricks.

- **Core Logic Isolation**: The core PySpark code is encapsulated in a reusable module so it can be triggered by different execution engines: CLI, Apache Airflow, Jupyter Notebooks, or native cloud Spark jobs.
- **Modular Runtimes**:
  - CLI Tool for local development
  - Apache Airflow DAG for production orchestration
  - Notebook compatibility for interactive debugging in Jupyter or Databricks
  - Cloud Integration with job specs/scripts for EMR, Synapse, Dataproc, and Databricks
- **API Layer**: A Flask backend serves REST APIs for monitoring and integration.
- **Frontend Layer**: An Angular app visualizes ingestion metrics such as record counts, last load status, and timestamps.
- **DevOps Ready**: Docker Compose configurations for PostgreSQL and Airflow are included for local simulation of cloud services.

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
