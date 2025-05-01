import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(page_title="PID Heat Exchanger Lab", layout="wide")

# --- Title and Header ---
st.title("🌬️ Virtual PID-Controlled Heat Exchanger Lab")
st.markdown("""
**Northern Technical University**  
Technical Engineering College  
Chemical and Petroleum Industries Technologies Engineering  
_Designed by: Azam Isam_
""")
st.markdown("---")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 System Inputs")
T_in = st.sidebar.slider("Hot Inlet Temp (°C)", 80, 300, 150)
T_cool = st.sidebar.slider("Coolant Temp (°C)", 10, 100, 30)
UA = st.sidebar.slider("Base UA (W/°C)", 100, 1500, 500)
Cp = st.sidebar.slider("Specific Heat Cp (kJ/kg·°C)", 1.0, 5.0, 4.18)
m_dot = st.sidebar.slider("Mass Flow Rate (kg/s)", 0.5, 10.0, 2.0)
T_set = st.sidebar.slider("Target Outlet Temp (°C)", 50, 300, 100)

st.sidebar.header("🎛 PID Controller")
Kp = st.sidebar.slider("Kp", 0.0, 10.0, 2.0)
Ki = st.sidebar.slider("Ki", 0.0, 5.0, 0.5)
Kd = st.sidebar.slider("Kd", 0.0, 2.0, 0.1)

with st.sidebar.expander("ℹ️ Parameter Help"):
    st.markdown("""
    - **T_in:** Hot fluid inlet temperature  
    - **T_cool:** Coolant inlet temperature  
    - **UA:** Overall heat transfer coefficient × area  
    - **Cp:** Specific heat capacity  
    - **ṁ:** Mass flow rate  
    - **T_set:** Target outlet temperature  
    """)

# --- Layout Columns ---
left, right = st.columns([1, 2])

# --- Heat Exchanger Diagram ---
with left:
    st.subheader("📉 Diagram")
    st.image("heat_exchanger.png", caption="Labeled schematic")

    with st.expander("📌 Diagram Annotations"):
        st.markdown("""
        - 🔴 **T_in:** Hot fluid inlet  
        - 🔵 **T_cool:** Coolant inlet  
        - 🟢 **T_out:** Controlled outlet temperature  
        - ⚫ **Coolant outlet**  
        - 🧮 **UA, Cp, ṁ:** System parameters  
        """)

# --- PID Simulation ---
dt = 1
time = np.arange(0, 200, dt)
T_out = [T_cool]
error_prev = T_set - T_cool
integral = 0

for t in time[1:]:
    error = T_set - T_out[-1]
    integral += error * dt
    derivative = (error - error_prev) / dt
    control = Kp * error + Ki * integral + Kd * derivative
    UA_eff = max(100, min(2000, UA + control))  # Clamp UA
    T_next = T_out[-1] + (UA_eff * (T_in - T_out[-1]) * dt) / (m_dot * Cp * 1000)
    T_out.append(T_next)
    error_prev = error

# --- Calculated Results ---
final_T = T_out[-1]
Q = UA * (final_T - T_cool)
delta_T = T_in - final_T

# --- Metrics and Chart ---
with right:
    st.subheader("📊 Real-Time Output")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Outlet Temp (°C)", f"{final_T:.2f}")
    with col2:
        st.metric("Heat Transferred (Q)", f"{Q:.2f} kJ/s")
    with col3:
        st.metric("Temperature Drop (ΔT)", f"{delta_T:.2f} °C")

    # --- Chart ---
    st.subheader("📈 Outlet Temperature vs. Time")
    fig, ax = plt.subplots(figsize=(8, 4.5))  # Wider, balanced aspect
    ax.plot(time, T_out, label="T_out", color="crimson", linewidth=2)
    ax.axhline(y=T_set, color="green", linestyle="--", label="Setpoint")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("PID-Controlled Outlet Temp")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# --- Equations ---
with st.expander("📘 Full Equations Summary"):
    st.latex(r"Q = UA \cdot (T_{\text{out}} - T_{\text{cool}})")
    st.latex(r"T_{\text{out,next}} = T_{\text{out}} + \frac{Q \cdot \Delta t}{\dot{m} \cdot C_p \cdot 1000}")
    st.latex(r"U = K_p \cdot e + K_i \cdot \int e \, dt + K_d \cdot \frac{de}{dt}")
    st.markdown("All values are updated every second (1s timestep).")

# --- Student Activity ---
st.markdown("---")
with st.expander("🎓 Student Exercise"):
    st.markdown("""
    **Scenario:**  
    A hot fluid enters at 200°C and must exit at 100°C using coolant at 40°C.  
    UA = 600, Cp = 4.18, ṁ = 2.5 kg/s.  

    👉 Your task:  
    - Tune the PID to maintain T_out near 100°C  
    - Keep T_out within ±2°C of the setpoint  
    - Report your PID values and explain your reasoning  
    """)

# --- Optional Checklist ---
with st.expander("✅ Experiment Checklist"):
    st.checkbox("PID reaches steady state")
    st.checkbox("T_out stays within ±2°C of target")
    st.checkbox("Control strategy documented")
