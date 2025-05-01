import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -----------------------
# Heat exchanger PID simulation
# -----------------------
def simulate_heat_exchanger(Kp, Ki, Kd, T_in, T_cool, UA_base, Cp, m_dot, T_set, sim_time=200, dt=1.0):
    T_out = T_in
    T_hist = []
    t_hist = []

    integral = 0
    prev_error = T_set - T_out

    for t in range(0, int(sim_time)):
        error = T_set - T_out
        integral += error * dt
        derivative = (error - prev_error) / dt

        # PID affects effective UA (or flow control valve effect)
        UA_effective = UA_base + (Kp * error + Ki * integral + Kd * derivative)
        UA_effective = max(100, min(2000, UA_effective))  # clamp UA

        Q = UA_effective * (T_out - T_cool)
        delta_T = Q / (m_dot * Cp + 1e-6)  # prevent div by zero
        T_out = T_in - delta_T

        prev_error = error
        T_hist.append(T_out)
        t_hist.append(t)

    return np.array(t_hist), np.array(T_hist)

# -----------------------
# Streamlit App Layout
# -----------------------
st.set_page_config(page_title="Heat Exchanger PID Lab", layout="wide")
st.title("🌬️ Virtual PID-Controlled Heat Exchanger Lab")

st.markdown("""
**Northern Technical University**  
Technical Engineering College  
Chemical and Petroleum Industries Technologies Engineering  
*Designed by: Azam Isam*
""")

st.markdown("---")

# Sidebar Controls
st.sidebar.header("🔧 System Inputs")
T_in = st.sidebar.slider("Hot Inlet Temp (°C)", 80, 300, 150, 5)
T_cool = st.sidebar.slider("Coolant Temp (°C)", 10, 100, 30, 5)
UA_base = st.sidebar.slider("Base UA Value", 100, 1500, 500, 50)
Cp = st.sidebar.slider("Specific Heat Cp (kJ/kg°C)", 1.0, 5.0, 4.18, 0.1)
m_dot = st.sidebar.slider("Flow Rate (kg/s)", 0.5, 10.0, 2.0, 0.1)
T_set = st.sidebar.slider("Target Outlet Temp (°C)", 50, 300, 100, 5)

st.sidebar.header("🎛 PID Controller")
Kp = st.sidebar.slider("Kp", 0.0, 10.0, 2.0, 0.1)
Ki = st.sidebar.slider("Ki", 0.0, 5.0, 0.5, 0.1)
Kd = st.sidebar.slider("Kd", 0.0, 2.0, 0.1, 0.05)

simulate = st.sidebar.button("Run Simulation")

# Main layout
left, right = st.columns([1, 2])

with left:
    st.subheader("🖼 Heat Exchanger Diagram")
    st.image("heat_exchanger.png", use_container_width=True)  # <-- Provide this image
    st.markdown("""
    **Equation Model:**
    - Q = UA · (T_out - T_cool)  
    - ΔT = Q / (m · Cp)  
    - T_out = T_in - ΔT
    """)

with right:
    if simulate:
        t, T_out = simulate_heat_exchanger(Kp, Ki, Kd, T_in, T_cool, UA_base, Cp, m_dot, T_set)

        st.subheader("📈 Outlet Temperature Response")
        fig, ax = plt.subplots()
        ax.plot(t, T_out, label="T_out", color="crimson", linewidth=2)
        ax.axhline(y=T_set, color="green", linestyle="--", label="Setpoint")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Outlet Temperature vs. Time")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
