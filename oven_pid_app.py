import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import base64
from PIL import Image

# PID oven simulation function
def simulate_oven(Kp, Ki, Kd, T_set=200, sim_time=200, dt=1.0):
    T = 25
    T_hist = []
    t_hist = []

    integral = 0
    prev_error = T_set - T

    heat_capacity = 100.0
    heat_loss_coeff = 0.1
    ambient_temp = 25

    for t in range(0, sim_time):
        error = T_set - T
        integral += error * dt
        derivative = (error - prev_error) / dt

        power = Kp * error + Ki * integral + Kd * derivative
        power = max(0, min(100, power))

        heat_gain = power
        heat_loss = heat_loss_coeff * (T - ambient_temp)
        T += (heat_gain - heat_loss) * dt / heat_capacity

        prev_error = error
        T_hist.append(T)
        t_hist.append(t)

    return np.array(t_hist), np.array(T_hist)


# Streamlit setup
st.set_page_config(page_title="PID Oven Visual Lab", layout="wide")
st.title("🔥 Virtual PID-Controlled Oven Lab")

st.markdown("""
**Northern Technical University**  
Technical Engineering College  
Chemical and Petroleum Industries Technologies Engineering  
*Designed by: Azam Isam*
""")

st.markdown("---")

# Sidebar Controls
with st.sidebar:
    st.header("🎛 PID Controller Settings")
    Kp = st.slider("Kp", 0.0, 10.0, 2.0, 0.1)
    Ki = st.slider("Ki", 0.0, 10.0, 0.5, 0.1)
    Kd = st.slider("Kd", 0.0, 5.0, 1.0, 0.1)
    T_set = st.slider("Target Temp (°C)", 50, 300, 200, 5)

    if st.button("🔥 Run Simulation"):
        t, T = simulate_oven(Kp, Ki, Kd, T_set)
        st.session_state["t"] = t
        st.session_state["T"] = T
        st.session_state["T_final"] = T[-1]


# Layout: image + graph
col1, col2 = st.columns([1, 1.5])

# --- Left Column: Oven Visual ---
with col1:
    st.subheader("🧪 Oven Visualization")
    image = Image.open("oven_diagram.png")
    st.image(image, use_container_width=True)


    if "T_final" in st.session_state:
        temp = st.session_state["T_final"]
        display_color = "red" if temp > 250 else "orange" if temp > 150 else "yellow" if temp > 80 else "lightblue"
        st.markdown(
            f"""
            <div style='
                width: 120px;
                height: 50px;
                background-color: {display_color};
                border-radius: 5px;
                font-weight: bold;
                font-size: 22px;
                color: black;
                text-align: center;
                line-height: 50px;
                margin: auto;
                box-shadow: 0 0 12px {display_color};
            '>{temp:.1f} °C</div>
            """,
            unsafe_allow_html=True
        )

# --- Right Column: Graph ---
with col2:
    if "t" in st.session_state:
        t = st.session_state["t"]
        T = st.session_state["T"]

        fig, ax = plt.subplots()
        ax.plot(t, T, color='crimson', linewidth=2, label="Oven Temp")
        ax.axhline(y=T_set, color='green', linestyle='--', label="Setpoint")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Temperature vs. Time")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
