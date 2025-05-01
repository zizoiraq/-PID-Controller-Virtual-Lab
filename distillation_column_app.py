import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- Simulation Function ----------
def distillation_column(alpha, zF, R, N, feed_stage):
    x = np.zeros(N+1)
    y = np.zeros(N+1)
    x[feed_stage] = zF

    # Rectifying section (above feed)
    for i in range(feed_stage, 0, -1):
        y[i] = alpha * x[i] / (1 + (alpha - 1) * x[i])
        x[i-1] = y[i] / (R + 1)

    # Stripping section (below feed)
    for i in range(feed_stage, N):
        y[i] = alpha * x[i] / (1 + (alpha - 1) * x[i])
        x[i+1] = (R + 1) * x[i] - R * y[i]
        x[i+1] = max(0, min(1, x[i+1]))  # keep x in [0,1]

    return x, y

# ---------- Streamlit App ----------
st.set_page_config(page_title="Distillation Tower Lab", layout="wide")
st.title("🧪 Virtual Distillation Column Lab")

st.markdown("""
**Northern Technical University**  
Technical Engineering College – Chemical and Petroleum Engineering  
_Designed by: Azam Isam_
""")

st.markdown("---")

# ---------- Sidebar Controls ----------
st.sidebar.header("🔧 Input Parameters")
alpha = st.sidebar.slider("Relative Volatility (α)", 1.1, 5.0, 2.5, 0.1)
zF = st.sidebar.slider("Feed Composition (zF)", 0.01, 0.99, 0.5, 0.01)
R = st.sidebar.slider("Reflux Ratio (R)", 0.5, 10.0, 2.5, 0.1)
N = st.sidebar.slider("Number of Trays", 5, 25, 10, 1)
feed_stage = st.sidebar.slider("Feed Stage Location", 1, 24, 5, 1)

# ---------- Run Simulation ----------
x, y = distillation_column(alpha, zF, R, N, feed_stage)

# ---------- Plot ----------
st.subheader("📈 Composition Profile Along Trays")

fig, ax = plt.subplots(figsize=(6, 6))
trays = np.arange(0, N+1)
ax.plot(x, trays, 'bo-', label='Liquid (x)')
ax.plot(y, trays, 'rx--', label='Vapor (y)')
ax.axhline(feed_stage, color='gray', linestyle=':', label=f"Feed at Tray {feed_stage}")
ax.invert_yaxis()
ax.set_xlabel("Mole Fraction of More Volatile Component")
ax.set_ylabel("Tray Number (Top → Bottom)")
ax.set_title("Composition Profile in Distillation Column")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ---------- Educational Section ----------
with st.expander("📘 Explanation"):
    st.markdown("""
    - **Feed tray** divides the column into:
        - Rectifying section (above)
        - Stripping section (below)
    - **Liquid (x)** flows down, **vapor (y)** rises.
    - **Reflux ratio** controls purity at the top.
    - Composition is calculated using ideal tray assumptions and constant molar overflow.
    """)

with st.expander("🎓 Student Challenge"):
    st.markdown("""
    **Your Task:**  
    Set the parameters to achieve a top product (Tray 0) composition of at least **0.95**.

    - Try changing α, R, and N.
    - Report the number of trays needed.
    """)
