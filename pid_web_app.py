import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import control

# ----------------------------
# PID simulation logic
# ----------------------------

def simulate_pid(Kp, Ki, Kd, plant_type):
    # Define plant transfer function
    if plant_type == "First Order":
        plant = control.tf([1], [1, 2])
    elif plant_type == "Second Order":
        plant = control.tf([1], [1, 3, 2])
    elif plant_type == "Integrator":
        plant = control.tf([1], [1, 0])
    else:
        plant = control.tf([1], [1, 2])  # default fallback

    # PID Controller: Kp + Ki/s + Kd*s
    pid = control.tf([Kd, Kp, Ki], [1, 0])

    # Closed-loop transfer function
    system = control.feedback(pid * plant, 1)

    # Simulate step response
    t, y = control.step_response(system, T=np.linspace(0, 5, 500))
    return t, y

# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(page_title="PID Virtual Lab", layout="centered")
st.title("🎛️ PID Controller Virtual Lab")
st.markdown("**Northern Technical University**  \nTechnical Engineering College  \nChemical and Petroleum Industries Technologies Engineering  \n*Designed by: Azam Isam*")
st.markdown("---")

# PID sliders with rounded display
col1, col2, col3 = st.columns(3)

with col1:
    Kp = st.slider("Kp", 0.0, 10.0, 2.0, 0.1)
    st.write(f"**Kp = {Kp:.2f}**")

with col2:
    Ki = st.slider("Ki", 0.0, 10.0, 1.0, 0.1)
    st.write(f"**Ki = {Ki:.2f}**")

with col3:
    Kd = st.slider("Kd", 0.0, 10.0, 0.5, 0.1)
    st.write(f"**Kd = {Kd:.2f}**")

# Dropdown to select plant model
plant_type = st.selectbox("Choose Plant Model", ["First Order", "Second Order", "Integrator"])

# Simulate
if st.button("Run Simulation"):
    t, y = simulate_pid(Kp, Ki, Kd, plant_type)

    # Plot result
    fig, ax = plt.subplots()
    ax.plot(t, y, label="Output", color="blue")
    ax.set_title("System Output vs Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Output")
    ax.grid(True)
    st.pyplot(fig)
