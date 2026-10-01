import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Seiten-Konfiguration
st.set_page_config(
    page_title="Interaktive System-Simulation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Interaktive System-Simulation")
st.markdown("Passen Sie die Parameter in der Seitenleiste an, um das Verhalten des Systems dynamisch zu simulieren.")

# ---------------------------------------------------------
# SEITENLEISTE: Steuerlemente & Regler
# ---------------------------------------------------------
st.sidebar.header("⚙️ Simulationsparameter")

# Regler (Slider)
param_a = st.sidebar.slider(
    "Startwert / Baseline (A)", 
    min_value=1.0, max_value=100.0, value=50.0, step=1.0
)

param_b = st.sidebar.slider(
    "Wachstumsfaktor (B)", 
    min_value=0.01, max_value=0.50, value=0.10, step=0.01
)

noise_level = st.sidebar.slider(
    "Schwankung / Rauschen", 
    min_value=0.0, max_value=10.0, value=2.0, step=0.5
)

time_steps = st.sidebar.slider(
    "Zeithorizont (Schritte)", 
    min_value=10, max_value=200, value=100, step=10
)

# Auswahlfeld & Checkboxen
model_type = st.sidebar.selectbox(
    "Modelltyp wählen", 
    ["Logistisch", "Exponentiell", "Linear"]
)

show_raw_data = st.sidebar.checkbox("Rohdaten-Tabelle anzeigen", value=False)

# ---------------------------------------------------------
# SIMULATION & BERECHNUNG
# ---------------------------------------------------------
t = np.arange(0, time_steps)

if model_type == "Exponentiell":
    y_ideal = param_a * np.exp(param_b * t / 10)
elif model_type == "Logistisch":
    y_ideal = param_a / (1 + np.exp(-param_b * (t - time_steps / 2)))
else:
    y_ideal = param_a + param_b * t * 10

# Zufälliges Rauschen hinzufügen
np.random.seed(42)
noise = np.random.normal(0, noise_level, size=len(t))
y_sim = np.maximum(0, y_ideal + noise)

df = pd.DataFrame({
    "Zeitschritt": t,
    "Simulierter Wert": y_sim,
    "Theoretischer Trend": y_ideal
})

# ---------------------------------------------------------
# DASHBOARD DISPLAY
# ---------------------------------------------------------
# Kennzahlen anzeigen
col1, col2, col3 = st.columns(3)
col1.metric("Maximalwert", f"{y_sim.max():.2f}")
col2.metric("Durchschnittswert", f"{y_sim.mean():.2f}")
col3.metric("Endwert", f"{y_sim[-1]:.2f}")

st.markdown("---")

# Interaktives Diagramm zeichnen
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(t, y_sim, label="Simulierte Daten (mit Schwankung)", color="#1f77b4", alpha=0.8, linewidth=1.5)
ax.plot(t, y_ideal, label="Theoretische Kurve", color="#ff7f0e", linestyle="--", linewidth=2)
ax.set_xlabel("Zeit / Schritte")
ax.set_ylabel("Wert")
ax.set_title(f"Simulationsergebnis: {model_type}es Modell")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()

st.pyplot(fig)

# Rohdaten anzeigen, falls gewünscht
if show_raw_data:
    st.subheader("📋 Datenübersicht")
    st.dataframe(df, use_container_width=True)
