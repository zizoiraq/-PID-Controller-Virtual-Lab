import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# PID-controlled tank simulation function
def simulate_tank(Kp, Ki, Kd, setpoint=5.0, sim_time=100, dt=1.0, A=1.0, max_inflow=5.0):
    time = []
    level = []
    h = 0  # initial level
    integral = 0
    prev_error = setpoint - h

    for t in range(0, int(sim_time)):
        error = setpoint - h
        integral += error * dt
        derivative = (error - prev_error) / dt

        inflow = Kp * error + Ki * integral + Kd * derivative
        inflow = max(0, min(max_inflow, inflow))

        outflow = 0.5 * h  # simple linear outflow
        dh = (inflow - outflow) / A
        h += dh * dt
        h = max(0, h)

        prev_error = error
        time.append(t)
        level.append(h)

    return np.array(time), np.array(level)

# --- Streamlit App ---
st.set_page_config(page_title="Tank PID Lab", layout="wide")
st.title("🚰 Virtual PID-Controlled Tank Level Lab")

st.markdown("""
**Northern Technical University**  
Technical Engineering College  
Chemical and Petroleum Industries Technologies Engineering  
_Designed by: Azam Isam_
""")
st.markdown("---")

# Sidebar Controls
st.sidebar.header("🔧 System Settings")
setpoint = st.sidebar.slider("Setpoint Level (m)", 1.0, 10.0, 5.0, 0.5)
A = st.sidebar.slider("Tank Area (m²)", 0.5, 5.0, 1.0, 0.1)
max_inflow = st.sidebar.slider("Max Inflow Rate (m³/s)", 1.0, 10.0, 5.0, 0.5)

st.sidebar.header("🎛 PID Tuning")
Kp = st.sidebar.slider("Kp", 0.0, 10.0, 2.0)
Ki = st.sidebar.slider("Ki", 0.0, 5.0, 0.5)
Kd = st.sidebar.slider("Kd", 0.0, 2.0, 0.1)

# Simulate system
t, h = simulate_tank(Kp, Ki, Kd, setpoint, A=A, max_inflow=max_inflow)

# Main layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📦 Tank Visualization")
    tank_height = 300
    water_height = int((h[-1] / 10) * tank_height)
    tank_html = f"""
    <div style='
        width: 120px;
        height: {tank_height}px;
        border: 4px solid #333;
        background-color: lightgray;
        position: relative;
    '>
        <div style='
            position: absolute;
            bottom: 0;
            width: 100%;
            height: {water_height}px;
            background-color: deepskyblue;
        '></div>
    </div>
    """
    st.markdown(tank_html, unsafe_allow_html=True)
    st.metric("Final Level", f"{h[-1]:.2f} m")

with col2:
    st.subheader("📈 Tank Level Over Time")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, h, label="Level", color="blue", linewidth=2)
    ax.axhline(setpoint, color="green", linestyle="--", label="Setpoint")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Level (m)")
    ax.set_title("Tank Level vs. Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Educational Section
with st.expander("📘 Equations Used"):
    st.latex(r"h_{t+1} = h_t + \frac{(Q_{in} - Q_{out}) \cdot \Delta t}{A}")
    st.latex(r"Q_{in} = K_p \cdot e + K_i \cdot \int e \, dt + K_d \cdot \frac{de}{dt}")
    st.latex(r"Q_{out} = 0.5 \cdot h_t")
    st.markdown("""
    - \( A \): Tank cross-sectional area  
    - \( Q_{in} \): Inflow controlled by PID  
    - \( Q_{out} \): Outflow is proportional to level  
    """)

with st.expander("🎓 Student Exercise"):
    st.markdown("""
    **Scenario:**  
    Keep the tank level steady at 6.0 m using PID control.  
    - Tank area: 2.0 m²  
    - Inflow limited to 6 m³/s  
    - Tune Kp, Ki, Kd to prevent overshoot and oscillation.

    ✅ Report your PID settings and final level.
    """)
