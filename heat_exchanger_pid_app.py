import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="PID Heat Exchanger Lab", layout="wide")
st.title("🌬️ Virtual PID-Controlled Heat Exchanger Lab")

st.markdown("""
**Northern Technical University**  
Technical Engineering College  
Chemical and Petroleum Industries Technologies Engineering  
_Designed by: Azam Isam_
""")
st.markdown("---")

# Sidebar inputs
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

# Diagram and annotations
left, right = st.columns([1, 2])

with left:
    st.subheader("🖼 Heat Exchanger Diagram")
    st.image("heat_exchanger.png", caption="Labeled schematic")

    with st.expander("📌 Diagram Annotations"):
        st.markdown("""
        - 🔴 **T_in:** Hot fluid inlet  
        - 🔵 **T_cool:** Coolant inlet  
        - 🟢 **T_out:** Controlled outlet temperature  
        - ⚫ **Coolant outlet**  
        - 🧮 **UA, Cp, ṁ:** System parameters  
        """)

# Simulation
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
    UA_eff = max(100, min(2000, UA + control))  # Clamp
    T_next = T_out[-1] + (UA_eff * (T_in - T_out[-1]) * dt) / (m_dot * Cp * 1000)
    T_out.append(T_next)
    error_prev = error

final_T = T_out[-1]
Q = UA * (final_T - T_cool)
delta_T = T_in - final_T

with right:
    st.subheader("📊 Real-Time Results with Formulas")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Final Outlet Temp (°C)", f"{final_T:.2f}")
        st.latex(r"T_{\text{out,next}} = T_{\text{out}} + \frac{UA \cdot (T_{\text{in}} - T_{\text{out}}) \cdot \Delta t}{\dot{m} \cdot C_p \cdot 1000}")

    with col2:
        st.metric("Heat Transferred (Q)", f"{Q:.2f} kJ/s")
        st.latex(r"Q = UA \cdot (T_{\text{out}} - T_{\text{cool}})")

    with col3:
        st.metric("Temperature Drop (ΔT)", f"{delta_T:.2f} °C")
        st.latex(r"\Delta T = T_{\text{in}} - T_{\text{out}}")

    # Plot
    fig, ax = plt.subplots()
    ax.plot(time, T_out, label="T_out", color="crimson", linewidth=2)
    ax.axhline(y=T_set, color="green", linestyle="--", label="Setpoint")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Outlet Temperature vs. Time")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# Formulas summary
with st.expander("📘 Full Equations Summary"):
    st.latex(r"Q = UA \cdot (T_{\text{out}} - T_{\text{cool}})")
    st.latex(r"T_{\text{out,next}} = T_{\text{out}} + \frac{Q \cdot \Delta t}{\dot{m} \cdot C_p \cdot 1000}")
    st.latex(r"U = K_p \cdot e + K_i \cdot \int e \, dt + K_d \cdot \frac{de}{dt}")

# Student task
st.markdown("---")
with st.expander("🎓 Student Exercise"):
    st.markdown("""
    **Scenario:**  
    A hot fluid enters at 200°C and must exit at 100°C using coolant at 40°C.  
    UA = 600, Cp = 4.18, ṁ = 2.5 kg/s.  

    👉 Your task:  
    - Tune PID to reach and maintain 100°C  
    - Keep T_out within ±2°C of the setpoint  
    - Report your control values and explain why they work  
    """)

with st.expander("✅ Checklist"):
    st.checkbox("PID reaches steady state")
    st.checkbox("T_out stable within ±2°C of T_set")
    st.checkbox("Student explains control strategy")
