import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora de Lentes", layout="centered", page_icon="👓")

st.title("👓 Calculadora de Espesor de Borde de Lentes")

st.markdown("""
Esta herramienta calcula el espesor de borde de una lente óptica a partir de sus parámetros geométricos o su **graduación (dioptrías)**.
""")

# Modo de entrada
modo = st.radio("Selecciona el modo de entrada:", ["Usar radios de curvatura", "Usar graduación (dioptrías)"])

col1, col2 = st.columns(2)
with col1:
    D = st.number_input("Diámetro de la lente (mm)", value=60.0, step=1.0)
    Tc = st.number_input("Espesor central (mm)", value=2.0, step=0.1)
with col2:
    n = st.number_input("Índice de refracción (n)", value=1.5, step=0.01)

tipo = st.selectbox("Tipo de lente", ["Biconvexa (+)", "Biconcava (-)", "Plano-convexa (+)", "Plano-cóncava (-)"])

# Cálculo según el modo
if modo == "Usar radios de curvatura":
    R1 = st.number_input("Radio anterior R1 (mm)", value=100.0)
    R2 = st.number_input("Radio posterior R2 (mm)", value=-80.0)
else:
    # Entrada por graduación
    P = st.number_input("Graduación (dioptrías)", value=+2.00, step=0.25)
    # Convertir D -> radios (en mm)
    # Fórmula: P = (n - 1) * (1/R1 - 1/R2)
    # Asumimos una lente plano-convexa o biconvexa
    if "Plano" in tipo:
        # Cara posterior plana: R2 = infinito
        R2 = 1e9  # radio muy grande ≈ plano
        R1 = 1000 * (n - 1) / P  # en mm
    else:
        # Distribuimos potencia entre ambas caras (biconvexa o biconcava)
        R1 = 2000 * (n - 1) / P  # en mm
        R2 = -R1

# --- Cálculo del espesor de borde ---
t_borde = Tc + (D ** 2 / 8.0) * (1.0 / R1 - 1.0 / R2)

st.subheader("📏 Resultado")
st.metric("Espesor de borde (mm)", f"{t_borde:.3f}")

st.markdown(f"""
**R1:** {R1:.1f} mm  
**R2:** {R2:.1f} mm
""")

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
st.caption("Desarrollado con Python + Streamlit. Compatible con navegador móvil 📱")
