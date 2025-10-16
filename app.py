import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Calculadora de Lentes Interactiva", layout="centered", page_icon="👓")

st.title("👓 Calculadora Interactiva de Lentes")

st.markdown("""
Esta herramienta calcula el espesor de borde de una lente y permite explorar su forma haciendo clic sobre el perfil.
""")

# --- Entradas básicas ---
col1, col2 = st.columns(2)
with col1:
    D = st.number_input("Diámetro (mm)", value=60.0, step=1.0)
    Tc = st.number_input("Espesor central (mm)", value=2.0, step=0.1)
    n = st.number_input("Índice de refracción (n)", value=1.5, step=0.01)
with col2:
    modo = st.radio("Modo de entrada", ["Usar radios", "Usar graduación (D)"])
    tipo = st.selectbox("Tipo de lente", ["Biconvexa (+)", "Biconcava (-)", "Plano-convexa (+)", "Plano-cóncava (-)"])

# --- Cálculo de radios ---
if modo == "Usar radios":
    R1 = st.number_input("Radio anterior R1 (mm)", value=100.0)
    R2 = st.number_input("Radio posterior R2 (mm)", value=-80.0)
else:
    P = st.numb
