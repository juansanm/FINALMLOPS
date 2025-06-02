Este proyecto implementa un pipeline completo de MLOps en Kubernetes con entrenamiento, registro, despliegue, monitoreo y CI/CD utilizando Argo CD.

## 🚀 Arquitectura

- **Airflow**: Orquesta el ETL y el entrenamiento de modelos
- **MLflow**: Registra modelos y gestiona la versión en producción
- **FastAPI**: Sirve el modelo en producción como API REST
- **Streamlit**: Frontend para predicciones interactivas
- **Locust** – Herramienta para pruebas de carga y estrés de la API.
- **Prometheus + Grafana**: Monitoreo de métricas de la API
- **MinIO**: Backend S3 compatible para almacenar artefactos
- **Argo CD**: Sincronización GitOps desde GitHub al clúster de Kubernetes


##  Flujo de Trabajo

1. **ETL con Airflow**: Orquesta el flujo desde la descarga de datos hasta el entrenamiento.
2. **MLflow**: Registra múltiples modelos y promueve automáticamente el mejor modelo.
3. **FastAPI**: Sirve el modelo promovido con un endpoint `/predict`.
4. **Streamlit**: Permite a los usuarios realizar predicciones vía frontend.
5. **Prometheus & Grafana**: Visualizan métricas como latencia, peticiones y errores.
6. **Locust**: Permite simular múltiples usuarios accediendo al endpoint `/predict` para evaluar el rendimiento.
7. **Argo CD**: Automatiza el despliegue de recursos declarativos desde GitHub.

---

├── AIRFLOW/ # DAGs de ingestión, procesamiento y entrenamiento
├── FASTAPI/ # Código de la API
├── STREAMLIT/ # Aplicación de Streamlit para inferencia
├── MLFLOW/ # Configuración de MLflow y artefactos
├── postgres-init/ # Inicialización de base de datos PostgreSQL
├── k8s/ # Manifiestos de Kubernetes
├── docker-compose.yaml # Infraestructura local con Docker
├── prometheus.yml # Configuración Prometheus (Docker)
├── README.md # Este archivo


CI/CD con Argo CD
El directorio k8s/ está sincronizado con Argo CD para despliegue GitOps. Cualquier cambio que usted haga en este folder será reflejado en el clúster con solo hacer push.

✍️ Autor Juan Felipe Gonzalez Sanmiguel 

