from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Instrumentador Prometheus
instrumentator = Instrumentator().instrument(app).expose(app)

# Modelo global
model = None

# Entrada de predicción
class PropertyFeatures(BaseModel):
    bed: float
    bath: float
    house_size: float

# Cargar modelo en inicio
@app.on_event("startup")
def load_model():
    global model
    model_uri = "models:/real_estate_model/Production"
    try:
        model = mlflow.pyfunc.load_model(model_uri)
        print("✅ Modelo cargado exitosamente.")
    except Exception as e:
        print(f"❌ Error al cargar modelo: {e}")
        model = None

@app.get("/")
def root():
    return {"message": "API de predicción de propiedades en funcionamiento"}

@app.post("/predict")
def predict_price(features: PropertyFeatures):
    if model is None:
        return {"error": "Modelo no disponible. Intenta más tarde."}
    input_data = [[features.bed, features.bath, features.house_size]]
    prediction = model.predict(input_data)
    return {"predicted_price": prediction[0]}
