import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora de Lentes", layout="centered", page_icon="👓")

st.title("👓 Calculadora de Espesor de Borde de Lentes")
st.markdown("Introduce los parámetros de la lente para obtener el espesor de borde.")

# Entradas
col1, col2 = st.columns(2)
with col1:
    D = st.number_input("Diámetro (mm)", value=60.0, step=1.0)
    R1 = st.number_input("Radio anterior R1 (mm)", value=100.0, step=1.0)
with col2:
    R2 = st.number_input("Radio posterior R2 (mm)", value=-80.0, step=1.0)
    Tc = st.number_input("Espesor central (mm)", value=2.0, step=0.1)

tipo = st.selectbox("Tipo de lente", ["Biconvexa", "Biconcava", "Plano-convexa", "Plano-cóncava", "Menisco"])
n = st.number_input("Índice de refracción", value=1.5, step=0.01)

# --- Cálculo ---
t_borde = Tc + (D ** 2 / 8.0) * (1.0 / R1 - 1.0 / R2)

st.subheader("📏 Resultado")
st.metric("Espesor de borde (mm)", f"{t_borde:.3f}")

# --- Gráfico del perfil ---
x = np.linspace(-D/2, D/2, 200)
y = Tc + (x**2)/(2*R1) - (x**2)/(2*R2)
plt.figure()
plt.plot(x, y, label="Perfil de la lente")
plt.title("Perfil aproximado de la lente")
plt.xlabel("Ancho (mm)")
plt.ylabel("Espesor (mm)")
plt.legend()
st.pyplot(plt)

st.markdown("---")
st.caption("Desarrollado con Python + Streamlit. Compatible con móviles 📱")
