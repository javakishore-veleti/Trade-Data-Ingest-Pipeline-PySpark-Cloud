#!/bin/bash

# Use Java 11 explicitly
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH="$JAVA_HOME/bin:$PATH"

# Ensure UTF-8 output for Python
export PYTHONIOENCODING=utf-8

echo "Using JAVA_HOME: $JAVA_HOME"
echo "Starting PySpark ingestion..."

# Run ingestion module
python -m spark_pipeline.ingest
