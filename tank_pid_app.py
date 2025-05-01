import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(layout="wide", page_title="Tank Level PID Lab")

# Title
st.title("🧪 Virtual PID-Controlled Tank Level Lab")
st.markdown("Designed by: *Azam Isam*")

# Sidebar settings
with st.sidebar:
    st.header("🛠 System Settings")
    setpoint = st.slider("Setpoint Level (m)", 1.0, 10.0, 2.0, 0.1)
    area = st.slider("Tank Area (m²)", 0.5, 5.0, 2.0, 0.1)
    max_flow = st.slider("Max Inflow Rate (m³/s)", 1.0, 10.0, 2.5, 0.1)

    st.header("🎛 PID Tuning")
    Kp = st.slider("Kp", 0.0, 10.0, 1.0, 0.1)
    Ki = st.slider("Ki", 0.0, 5.0, 0.0, 0.1)
    Kd = st.slider("Kd", 0.0, 2.0, 0.0, 0.1)

# Simulation parameters
dt = 0.1
t = np.arange(0, 100, dt)
h = np.zeros_like(t)
Q_in = np.zeros_like(t)
Q_out = 1.0

integral = 0
prev_error = 0

for i in range(1, len(t)):
    error = setpoint - h[i-1]
    integral += error * dt
    derivative = (error - prev_error) / dt
    u = Kp * error + Ki * integral + Kd * derivative
    prev_error = error

    Q_in[i] = max(0, min(max_flow, u))
    dh = (Q_in[i] - Q_out) * dt / area
    h[i] = h[i-1] + dh
    h[i] = max(0, h[i])  # prevent negative level

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📦 Tank Visualization")

    fig, ax = plt.subplots(figsize=(2.5, 5))
    tank_max = 10
    tank_width = 1.0

    ax.barh(y=0.5, width=tank_width, height=h[-1], left=0, color='deepskyblue', edgecolor='black')
    ax.set_ylim(0, tank_max)
    ax.set_xlim(0, tank_width)
    ax.set_yticks(np.arange(0, tank_max+1, 1))
    ax.set_xticks([])
    ax.set_title("Tank Level", fontsize=10)
    ax.tick_params(axis='y', labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    for lvl in np.arange(0, tank_max + 1, 2):
        ax.text(tank_width / 2, lvl + 0.1, f"{lvl:.0f} m", ha='center', va='bottom', fontsize=7, color='black')

    st.pyplot(fig)
    st.metric("Final Level", f"{h[-1]:.2f} m")

with col2:
    st.subheader("📈 Tank Level Over Time")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(t, h, label="Level", color='blue')
    ax2.axhline(setpoint, color='green', linestyle='--', label='Setpoint')
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Level (m)")
    ax2.set_title("Tank Level vs. Time")
    ax2.legend()
    st.pyplot(fig2)
