import streamlit as st
import requests
st.set_page_config(page_title="Predicción Inmobiliaria", page_icon="🏠")
st.title("🏠 Predicción del Precio de una Propiedad")
st.write("Ingrese las características de la propiedad:")
bed = st.number_input("Número de habitaciones", min_value=0, value=3)
bath = st.number_input("Número de baños", min_value=0, value=2)
house_size = st.number_input("Tamaño en pies cuadrados", min_value=0, value=120)
if st.button("Predecir Precio"):
    payload = {
        "bed": bed,
        "bath": bath,
        "house_size": house_size
    }
    try:
        response = requests.post("http://mlops-fastapi:8000/predict", json=payload)
        if response.status_code == 200:
            predicted_price = response.json()["predicted_price"]
            st.success(f"💰 Precio estimado: ${predicted_price:,.2f}")
        else:
            st.error("❌ Error al realizar la predicción.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
