#!/bin/bash

echo "Creating project directories..."

# Core pipeline logic
mkdir -p spark_pipeline
mkdir -p cli_tool
mkdir -p airflow_dags
mkdir -p cloud_jobs/aws_emr cloud_jobs/azure_synapse cloud_jobs/gcp_dataproc cloud_jobs/databricks

# Backend & Frontend
mkdir -p backend
mkdir -p frontend/trade-monitor-ui

# DevOps
mkdir -p DevOps/Local-Dev/Dataset
mkdir -p DevOps/Local-Dev/Containers

# Docs and metadata
mkdir -p docs

# Root-level files
touch .env.example
touch README.md
touch requirements.txt
touch docker-compose.yml
touch package.json

# Backend stubs
touch backend/app.py backend/routes.py backend/models.py backend/db.py

# CLI and pipeline
touch cli_tool/run.py
touch spark_pipeline/config.py spark_pipeline/schema.py spark_pipeline/ingest.py

# Airflow DAG
touch airflow_dags/trade_ingest_dag.py

echo "Folder structure created!"
