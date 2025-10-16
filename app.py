import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

st.set_page_config(page_title="Calculadora Interactiva de Lentes", layout="centered", page_icon="👓")

st.title("👓 Calculadora Interactiva de Lentes (ambas caras)")
st.markdown("Visualiza la forma completa de la lente y haz clic para conocer el espesor local 📍")

# --- Entradas ---
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
        R2 = 1e6  # casi plano
        R1 = 1000 * (n - 1) / P
    else:
        R1 = 2000 * (n - 1) / P
        R2 = -R1

# --- Coordenadas ---
x = np.linspace(-D/2, D/2, 400)

# --- Superficies de la lente ---
# Cara anterior (frontal)
y1 = (x**2) / (2 * R1)
# Cara posterior (trasera)
y2 = Tc + (x**2) / (2 * R2)

# Corrige valores si R2 es enorme (plano)
if abs(R2) > 1e5:
    y2 = np.full_like(x, Tc)

# --- Espesor de borde ---
t_borde = (y2 - y1)[0]
st.metric("📏 Espesor de borde (mm)", f"{t_borde:.3f}")

# --- Figura ---
fig = go.Figure()

# Superficie rellena de la lente
fig.add_trace(go.Scatter(
    x=np.concatenate((x, x[::-1])),
    y=np.concatenate((y1, y2[::-1])),
    fill='toself',
    fillcolor='rgba(65,105,225,0.3)',
    line=dict(color='royalblue', width=2),
    name="Lente"
))

fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', line=dict(color='blue', width=2), name="Cara anterior"))
fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', line=dict(color='darkblue', width=2), name="Cara posterior"))

fig.update_layout(
    title="Perfil completo de la lente (vista lateral)",
    xaxis_title="Ancho (mm)",
    yaxis_title="Espesor (mm)",
    height=500,
    hovermode="x unified",
    template="simple_white",
    showlegend=False
)

# --- Captura de clic ---
selected_points = plotly_events(
    fig,
    click_event=True,
    hover_event=False,
    select_event=False,
    override_height=500,
    key="grafico_lente"
)

# --- Mostrar resultado ---
if selected_points and len(selected_points) > 0:
    punto_x = selected_points[0]["x"]

    # Espesor local (diferencia entre ambas caras)
    y1_local = (punto_x**2) / (2 * R1)
    y2_local = Tc + (punto_x**2) / (2 * R2)
    if abs(R2) > 1e5:
        y2_local = Tc
    t_local = y2_local - y1_local

    # Añade marcador en el punto clicado
    fig.add_trace(go.Scatter(
        x=[punto_x, punto_x],
        y=[y1_local, y2_local],
        mode="lines+markers",
        line=dict(color="red", width=3, dash="dot"),
        marker=dict(color="red", size=8),
        name="Punto clicado"
    ))

    st.plotly_chart(fig, use_container_width=True)
    st.success(f"📍 En x = {punto_x:.2f} mm → Espesor local = {t_local:.3f} mm")
else:
    st.plotly_chart(fig, use_container_width=True)
    st.info("Haz clic (o toca) sobre la lente para medir el espesor local.")

st.caption("Versión 2D completa con ambas caras — compatible con móvil 📱")
