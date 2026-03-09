import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuración de página compacta
st.set_page_config(page_title="Simulador de Cinemática", layout="wide")

# Título de la pagina
st.markdown("### 🎯 Cazadores de Trayectorias: Dominando el Ángulo Perfecto")

# 2. Barra lateral para ingreso numérico escrito
st.sidebar.header("Configuración de Disparo")
v0 = st.sidebar.number_input("Velocidad Inicial (m/s)", min_value=0.0, max_value=200.0, value=70.0, step=0.1)
angulo_deg = st.sidebar.number_input("Ángulo de inclinación (°)", min_value=0.0, max_value=90.0, value=30.0, step=1.0)
g = 9.81

# --- Cálculos ---
angulo_rad = np.radians(angulo_deg)

# Tiempo de vuelo total
t_vuelo = (2 * v0 * np.sin(angulo_rad)) / g
t_puntos = np.linspace(0, t_vuelo, 100)

# Ecuaciones de posición (x, y)
x = v0 * np.cos(angulo_rad) * t_puntos
y = (v0 * np.sin(angulo_rad) * t_puntos) - (0.5 * g * t_puntos**2)

# --- Métricas ---
alcance_max = (v0**2 * np.sin(2 * angulo_rad)) / g
# Aquí está la corrección de la línea 27: potencia **2 en lugar de *2
altura_max = (v0**2 * (np.sin(angulo_rad)**2)) / (2 * g) 
distancia_h_max = alcance_max / 2

# Mostrar métricas en pantalla
col1, col2, col3 = st.columns(3)
col1.metric("Alcance Máximo", f"{alcance_max:.2f} m")
col2.metric("Altura Máxima", f"{altura_max:.2f} m")
col3.metric("Tiempo de Vuelo", f"{t_vuelo:.2f} s")

# --- Gráfica Interactiva y Animada ---

fig = go.Figure(
    data=[
        # 1. La línea de la trayectoria
        go.Scatter(x=x, y=y, mode="lines", name="Trayectoria", line=dict(color='gray', dash='dash')),
        
        # 2. El proyectil (punto rojo móvil)
        go.Scatter(x=[0], y=[0], mode="markers", name="Proyectil", marker=dict(color='red', size=12)),
        
        # 3. Marcador de Altura Máxima (Estrella Verde)
        go.Scatter(
            x=[distancia_h_max],
            y=[altura_max],
            mode="markers+text",
            name="H Máxima",
            text=[f"Punto más alto: {altura_max:.2f}m"],
            textposition="top center",
            marker=dict(color='green', size=15, symbol='star')
        )
    ],
    layout=go.Layout(
        xaxis=dict(range=[0, alcance_max * 1.1], title="Distancia Horizontal (m)"),
        yaxis=dict(range=[0, altura_max * 1.3], title="Altura (m)"),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="🔥 Disparar Cañón", method="animate", args=[None, {"frame": {"duration": 20}}])]
        )],
        # Líneas guía punteadas hacia los ejes
        shapes=[
            dict(type="line", x0=distancia_h_max, y0=0, x1=distancia_h_max, y1=altura_max, line=dict(color="green", width=1, dash="dot")),
            dict(type="line", x0=0, y0=altura_max, x1=distancia_h_max, y1=altura_max, line=dict(color="green", width=1, dash="dot"))
        ],
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    ),
    frames=[go.Frame(data=[
        go.Scatter(x=x, y=y),
        go.Scatter(x=[x[i]], y=[y[i]]) 
    ]) for i in range(len(x))]
)


st.plotly_chart(fig, use_container_width=True)
