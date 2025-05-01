import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Header ---
st.set_page_config(page_title="Heat Exchanger PID Lab", layout="wide")
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
UA = st.sidebar.slider("Base UA Value", 100, 1500, 500)
Cp = st.sidebar.slider("Specific Heat Cp (kJ/kg·°C)", 1.0, 5.0, 4.18)
m_dot = st.sidebar.slider("Flow Rate (kg/s)", 0.5, 10.0, 2.0)
T_set = st.sidebar.slider("Target Outlet Temp (°C)", 50, 300, 100)

st.sidebar.header("🎛 PID Controller")
Kp = st.sidebar.slider("Kp", 0.0, 10.0, 2.0)
Ki = st.sidebar.slider("Ki", 0.0, 5.0, 0.5)
Kd = st.sidebar.slider("Kd", 0.0, 2.0, 0.1)

with st.sidebar.expander("ℹ️ Parameter Help"):
    st.markdown("""
    - **T_in**: Temp of incoming hot fluid  
    - **T_cool**: Temp of coolant  
    - **UA**: Overall heat transfer coefficient × area  
    - **Cp**: Specific heat capacity of the process fluid  
    - **ṁ**: Mass flow rate of the fluid  
    - **T_set**: Desired outlet temperature  
    """)
st.subheader("📊 Real-Time Results with Formulas")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Final Outlet Temp (°C)", f"{final_T:.2f}")
    st.caption("**T_out_next = T_out + (UA × (T_in - T_out) × dt) / (m · Cp × 1000)**")

with col2:
    st.metric("Heat Transferred (Q)", f"{Q:.2f} kJ/s")
    st.caption("**Q = UA × (T_out - T_cool)**")

with col3:
    st.metric("Temperature Drop (ΔT)", f"{delta_T:.2f} °C")
    st.caption("**ΔT = T_in - T_out**")

# --- Main Layout ---
left, right = st.columns([1, 2])

with left:
    st.subheader("🖼 Heat Exchanger Diagram")
    st.image("heat_exchanger.png", caption="Shell & Tube Heat Exchanger")

    with st.expander("🧾 Diagram Annotations"):
        st.markdown("""
        - 🔴 **T_in:** Hot fluid inlet  
        - 🔵 **T_cool:** Coolant inlet  
        - 🟢 **T_out:** Outlet temperature (controlled)  
        - ⚫ **Coolant outlet**  
        - 🧮 **UA, Cp, ṁ**: Influence how heat is transferred
        """)

# --- Simulation ---
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

final_T = T_out[-1]
Q = UA * (final_T - T_cool)
delta_T = T_in - final_T

with right:
    st.subheader("📈 Outlet Temperature Response")

    # Real-time Feedback
    st.metric("Final Outlet Temp (°C)", f"{final_T:.2f}")
    st.metric("Heat Transferred (Q)", f"{Q:.2f} kJ/s")
    st.metric("Temperature Drop (ΔT)", f"{delta_T:.2f} °C")

    # Plot
    fig, ax = plt.subplots()
    ax.plot(time, T_out, label="T_out", color="crimson", linewidth=2)
    ax.axhline(y=T_set, color="green", linestyle="--", label="Setpoint")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Outlet Temperature vs Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# --- Student Exercise ---
st.markdown("---")
with st.expander("🎓 Student Exercise"):
    st.markdown("""
    **Scenario:**  
    A hot fluid enters at 200°C and must exit at 100°C using a coolant at 40°C.  
    UA = 600, Cp = 4.18, ṁ = 2.5 kg/s.  

    Your Task:  
    - Tune the PID controller to reach and hold 100°C  
    - Keep T_out within ±2°C of the setpoint  
    - Explain how each parameter affects your result  
    """)

with st.expander("✅ Checklist"):
    st.checkbox("PID reaches steady state")
    st.checkbox("T_out stable within ±2°C of T_set")
    st.checkbox("Student explains reasoning in report")

st.success("✅ Lab ready for student use!")



st.subheader("📊 Real-Time Results with Formulas")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Final Outlet Temp (°C)", f"{final_T:.2f}")
    st.caption("**T_out_next = T_out + (UA × (T_in - T_out) × dt) / (m · Cp × 1000)**")

with col2:
    st.metric("Heat Transferred (Q)", f"{Q:.2f} kJ/s")
    st.caption("**Q = UA × (T_out - T_cool)**")

with col3:
    st.metric("Temperature Drop (ΔT)", f"{delta_T:.2f} °C")
    st.caption("**ΔT = T_in - T_out**")
