#!/bin/bash

set -e

JAR_VERSION="42.6.0"
JAR_NAME="postgresql-${JAR_VERSION}.jar"
JAR_PATH="./lib/${JAR_NAME}"
JAR_URL="https://jdbc.postgresql.org/download/${JAR_NAME}"

# Ensure lib folder exists
mkdir -p lib

# Download the jar if it doesn't exist
if [ ! -f "$JAR_PATH" ]; then
  echo "🔽 PostgreSQL JDBC driver not found. Downloading..."
  curl -L -o "$JAR_PATH" "$JAR_URL"
  echo "✅ Downloaded $JAR_NAME to ./lib"
else
  echo "✅ PostgreSQL JDBC driver already exists at $JAR_PATH"
fi

# Set Java version for PySpark
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH="$JAVA_HOME/bin:$PATH"
export PYTHONIOENCODING=utf-8

echo "🚀 Starting PySpark ingestion using JAVA_HOME=$JAVA_HOME"
python -m spark_pipeline.ingest
