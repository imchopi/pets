import streamlit as st
import pandas as pd
import joblib
import json

st.title("ClassiPet")
st.write("Clasificador de mascotas. Introduzca los datos de su mascota y le diremos a que clase pertenece")
st.image("./img/perro.jpg", use_container_width=True)

model = joblib.load("model/model.joblib")
with open("model/category_mapping.json", "r") as f:
    category_mapping = json.load(f)

# Extrae los valores categóricos
eye_color_values = category_mapping["eye_color"]
fur_length_values = category_mapping["fur_length"]

# Pide los datos de la mascota
weight = st.number_input("Peso (kg)", min_value=0.0, max_value=100.0, value=0.0)
height = st.number_input("Altura (cm)", min_value=0.0, max_value=100.0, value=0.0)
eye_color = st.selectbox("Color de ojos", ["Azul", "Marrón", "Gris", "Verde"])
fur_length = st.selectbox("Longitud del pelo", ["Largo", "Mediano", "Corto"])

# Mapea la selección de color de ojos y largo del pelo al español
eye_color_mapping = {"Azul": "blue", "Marrón": "brown", "Gris": "gray", "Verde": "green"}
fur_length_mapping = {"Largo": "long", "Mediano": "medium", "Corto": "short"}
eye_color = eye_color_mapping[eye_color]
fur_length = fur_length_mapping[fur_length]

# Genera las columnas binarias para eye_color y fur_length
eye_color_binary = [(eye_color == selected_color) for selected_color in eye_color_values]
fur_length_binary = [(fur_length == selected_length) for selected_length in fur_length_values]

# Crea un DataFrame con las características de la mascota
input_data = [weight, height] + eye_color_binary + fur_length_binary
columns = ["weight_kg", "height_cm"] + [f"eye_color_{color}" for color in eye_color_values] + [f"fur_length_{length}" for length in fur_length_values]
data = pd.DataFrame([input_data], columns=columns)

prediction_name = {"dog": "Perro", "cat": "Gato", "rabbit": "Conejo"}

# Realiza la predicción
if st.button("Clasificar"):
    prediction = model.predict(data)[0]
    prediction = prediction_name[prediction]
    st.success(f"La mascota es un {prediction}", icon="✅")