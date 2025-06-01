from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import mlflow
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'catchup': False
}

with DAG(
    'Gran_Proceso_Pal_5',
    schedule_interval=None,
    default_args=default_args,
    description='Pipeline completo de ETL y ML con promoción automática'
) as dag:

    def ingesta():
        df = pd.read_csv('/opt/airflow/properties_batch.csv')
        print("✅ Ingesta completada")
        print(df.head())

    def procesamiento():
        df = pd.read_csv('/opt/airflow/properties_batch.csv')
        df['price_m2'] = df['price'] / df['house_size']
        df.to_csv('/opt/airflow/processed_properties.csv', index=False)
        print("✅ Procesamiento completado")

    def entrenamiento():
        df = pd.read_csv('/opt/airflow/processed_properties.csv')
        X = df[['bed', 'bath', 'house_size']]
        y = df['price']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = LinearRegression()
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        
        # SOLUCIÓN: Configurar variables de entorno ANTES de cualquier operación MLflow
        os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://minio:9000"
        os.environ["AWS_ACCESS_KEY_ID"] = "mlflow"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "mlflow123"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        
        # Configurar tracking URI
        mlflow.set_tracking_uri("http://mlflow:5000")
        
        print("🔧 Configuración MLflow completada")

        # Crear o verificar experimento con configuración S3 correcta
        client = MlflowClient(tracking_uri="http://mlflow:5000")
        
        try:
            experiments = client.search_experiments()
            experiment_exists = any(exp.name == "real_estate_exp" for exp in experiments)
            
            if not experiment_exists:
                experiment_id = client.create_experiment(
                    name="real_estate_exp",
                    artifact_location="s3://mlflow-artifacts/experiments/"
                )
                print(f"✅ Experimento 'real_estate_exp' creado con ID: {experiment_id}")
            else:
                print("✅ Experimento 'real_estate_exp' ya existe")
        except Exception as e:
            print(f"⚠️ Error al manejar experimentos: {e}")
            print("Continuando con experimento por defecto...")

        # Configurar experimento
        try:
            mlflow.set_experiment("real_estate_exp")
            print("✅ Experimento configurado")
        except Exception as e:
            print(f"⚠️ Error al configurar experimento: {e}")

        # Registrar modelo
        with mlflow.start_run() as run:
            try:
                mlflow.log_param("features", ['bed', 'bath', 'house_size'])
                mlflow.log_metric("r2_score", score)
                
                # Log model con configuración explícita de S3
                mlflow.sklearn.log_model(
                    model,
                    artifact_path="model",
                    registered_model_name="real_estate_model"
                )

                run_id = run.info.run_id
                print(f"✅ Modelo entrenado y registrado. Run ID: {run_id}, Score: {score:.4f}")
                
            except Exception as e:
                print(f"❌ Error durante el logging del modelo: {e}")
                # Fallback: solo log de métricas sin registro del modelo
                try:
                    mlflow.log_param("features", ['bed', 'bath', 'house_size'])
                    mlflow.log_metric("r2_score", score)
                    print(f"✅ Métricas registradas (sin modelo). Score: {score:.4f}")
                except Exception as e2:
                    print(f"❌ Error crítico en MLflow: {e2}")
                    raise

    def promocionar_mejor_modelo():
        client = MlflowClient(tracking_uri="http://mlflow:5000")
        model_name = "real_estate_model"
        best_version = None
        best_score = float('-inf')

        try:
            # SOLUCIÓN: Usar get_registered_model para obtener versiones
            registered_model = client.get_registered_model(model_name)
            
            for mv in client.search_model_versions(f"name='{model_name}'"):
                try:
                    run = client.get_run(mv.run_id)
                    r2_score = run.data.metrics.get("r2_score")
                    
                    if r2_score is not None and r2_score > best_score:
                        best_score = r2_score
                        best_version = mv.version
                except Exception as e:
                    print(f"⚠️ Error al obtener métricas para versión {mv.version}: {e}")
                    continue

            if best_version:
                client.transition_model_version_stage(
                    name=model_name,
                    version=best_version,
                    stage="Production",
                    archive_existing_versions=True
                )
                print(f"✅ Versión {best_version} promovida a Production con r2_score={best_score:.4f}")
            else:
                print("⚠️ No se encontró ningún modelo para promover.")
                
        except Exception as e:
            print(f"⚠️ Error en promoción de modelo: {e}")
            print("Esto puede ser normal si es la primera ejecución.")

    # Definir tareas
    ingesta_task = PythonOperator(task_id='ingesta_csv', python_callable=ingesta)
    procesamiento_task = PythonOperator(task_id='procesamiento_csv', python_callable=procesamiento)
    entrenamiento_task = PythonOperator(task_id='entrenamiento_modelo', python_callable=entrenamiento)
    promocion_task = PythonOperator(task_id='promocionar_mejor_modelo', python_callable=promocionar_mejor_modelo)

    # Definir dependencias
    ingesta_task >> procesamiento_task >> entrenamiento_task >> promocion_task