FROM python:3.10

RUN pip install mlflow psycopg2-binary

EXPOSE 5000

CMD ["mlflow", "server", "--backend-store-uri", "postgresql://mlflow:mlflow@postgres:5432/mlflow_db", "--default-artifact-root", "/mlflow/mlruns", "--host", "0.0.0.0", "--port", "5000"]