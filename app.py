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
    P = st.number_input("Graduación (dioptrías)", value=+2.00, step=0.25)
    if "Plano" in tipo:
        R2 = 1e9  # Cara plana
        R1 = 1000 * (n - 1) / P
    else:
        R1 = 2000 * (n - 1) / P
        R2 = -R1

# --- Cálculo del espesor de borde ---
t_borde = Tc + (D**2 / 8.0) * (1.0 / R1 - 1.0 / R2)
st.metric("📏 Espesor de borde (mm)", f"{t_borde:.3f}")

# --- Perfil de la lente ---
x = np.linspace(-D/2, D/2, 400)
y = Tc + (x**2)/(2*R1) - (x**2)/(2*R2)

# --- Gráfico interactivo con Plotly ---
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode="lines",
    name="Perfil de la lente",
    line=dict(color="royalblue", width=3)
))

fig.update_layout(
    title="Perfil interactivo de la lente",
    xaxis_title="Ancho (mm)",
    yaxis_title="Espesor (mm)",
    hovermode="x unified",
    height=500
)

# --- Interacción con clic ---
click_data = st.plotly_chart(fig, use_container_width=True, on_click=True)

if click_data and click_data["points"]:
    punto_x = click_data["points"][0]["x"]
    # Cálculo del espesor en el punto clicado
    t_local = Tc + (punto_x**2)/(2*R1) - (punto_x**2)/(2*R2)
    st.success(f"📍 En x = {punto_x:.2f} mm → Espesor = {t_local:.3f} mm")

st.caption("Haz clic (o toca) sobre el perfil para ver el espesor en ese punto. Compatible con móvil 📱")
