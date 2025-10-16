import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora de Espesor de Lentes", layout="centered", page_icon="👓")

st.title("👓 Calculadora de Espesor de Lentes con Forma de Aro")

st.markdown("""
Esta aplicación estima el **espesor de borde** de una lente oftálmica rectangular,
teniendo en cuenta el **calibre del aro** y la **distancia nasopupilar (DNP)**.
""")

# --- Parámetros de entrada geométricos ---
col1, col2 = st.columns(2)
with col1:
    A = st.number_input("Calibre horizontal del aro A (mm)", value=52.0, step=0.5)
    B = st.number_input("Calibre vertical del aro B (mm)", value=36.0, step=0.5)
    DNP = st.number_input("Distancia nasopupilar (mm)", value=30.0, step=0.5)
with col2:
    Tc = st.number_input("Espesor central (mm)", value=2.0, step=0.1)
    n = st.number_input("Índice de refracción", value=1.5, step=0.01)
    P = st.number_input("Graduación (dioptrías)", value=-3.00, step=0.25)

# Tipo de lente
tipo = "Cóncava" if P < 0 else "Convexa"

# --- Cálculo de radios aproximados ---
# Suponemos lente plano-cóncava o plano-convexa
if P == 0:
    st.warning("La graduación es 0. La lente será plana (sin espesor de borde significativo).")
R1 = 1e9  # superficie plana
R2 = 1000 * (n - 1) / P if P != 0 else 1e9  # en mm

# --- Geometría del aro ---
# Descentrado del centro óptico respecto al centro del aro
decentrado = (A / 2) - DNP

# Coordenadas del borde más alejado del centro óptico
x_max = (A / 2) + abs(decentrado)
y_max = (B / 2)

# Distancia desde el centro óptico a la esquina exterior
r_ef = np.sqrt(x_max**2 + y_max**2)

# --- Cálculo del espesor en el borde más alejado ---
# Simplificación: potencia en dioptrías → curvatura efectiva
R_ef = abs(R2)
t_borde = Tc + (r_ef**2) / (2 * R_ef) if P > 0 else Tc + (r_ef**2) / (2 * R_ef)

# --- Resultados ---
st.subheader("📏 Resultados")
st.write(f"**Tipo de lente:** {tipo}")
st.write(f"**Descentrado del centro óptico:** {decentrado:.2f} mm")
st.metric("Espesor máximo de borde (mm)"
