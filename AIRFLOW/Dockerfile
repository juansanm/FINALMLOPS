FROM apache/airflow:2.7.0-python3.9
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --upgrade pip
RUN pip install \
    mlflow==2.7.1 \
    scikit-learn==1.3.0 \
    pandas==2.0.3 \
    boto3==1.28.17 \
    psycopg2-binary==2.9.7
ENV MLFLOW_S3_ENDPOINT_URL=http://minio:9000
ENV AWS_ACCESS_KEY_ID=mlflow
ENV AWS_SECRET_ACCESS_KEY=mlflow123
ENV AWS_DEFAULT_REGION=us-east-1
ENV MLFLOW_TRACKING_URI=http://mlflow:5000
ENV GIT_PYTHON_REFRESH=quiet