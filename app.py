import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

st.set_page_config(page_title="Calculadora Interactiva de Lentes", layout="centered", page_icon="👓")

st.title("👓 Calculadora Interactiva de Lentes")
st.markdown("Haz clic en el perfil para ver el espesor local en ese punto 📍")

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
        R2 = 1e6  # no infinito, para mantener forma visible
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

# Normalización del perfil (para asegurar que se vea)
y_min, y_max = y.min(), y.max()
if abs(y_max - y_min) < 0.001:
    y = (y - y.min()) * 1000  # amplifica si el perfil es muy plano

# --- Crear figura Plotly ---
fig = go.Figure()

# Relleno de la lente
fig.add_trace(go.Scatter(
    x=np.concatenate(([x[0]], x, [x[-1]])),
    y=np.concatenate(([0], y, [0])),
    fill='toself',
    fillcolor='rgba(65,105,225,0.3)',
    line=dict(color='royalblue', width=2),
    name="Lente"
))

fig.update_layout(
    title="Perfil de la lente (vista lateral)",
    xaxis_title="Ancho (mm)",
    yaxis_title="Espesor (mm)",
    hovermode="x unified",
    height=500,
    template="simple_white",
    showlegend=False
)

# --- Mostrar el gráfico y capturar clics ---
selected_points = plotly_events(
    fig,
    click_event=True,
    hover_event=False,
    select_event=False,
    override_height=500,
    key="grafico_lente"
)

# --- Mostrar resultado del clic ---
if selected_points and len(selected_points) > 0:
    punto_x = selected_points[0]["x"]
    # cálculo del espesor local
    t_local = Tc + (punto_x**2)/(2*R1) - (punto_x**2)/(2*R2)

    # Añadimos marcador rojo en el punto clicado
    fig.add_trace(go.Scatter(
        x=[punto_x],
        y=[t_local],
        mode="markers",
        marker=dict(color="red", size=10),
        name="Punto clicado"
    ))

    st.plotly_chart(fig, use_container_width=True)
    st.success(f"📍 En x = {punto_x:.2f} mm → Espesor = {t_local:.3f} mm")
else:
    st.plotly_chart(fig, use_container_width=True)
    st.info("Haz clic (o toca) sobre el perfil para ver el espesor en ese punto.")

st.caption("Visualización interactiva compatible con móvil 📱")
