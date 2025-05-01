import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plant_model(y, y_dot, u, dt):
    y_ddot = u - 3 * y_dot - 2 * y
    y_dot += y_ddot * dt
    y += y_dot * dt
    return y, y_dot

def pid_controller(error, prev_error, integral, dt, Kp, Ki, Kd):
    integral += error * dt
    derivative = (error - prev_error) / dt
    output = Kp * error + Ki * integral + Kd * derivative
    return output, integral

def run_simulation(Kp, Ki, Kd):
    setpoint = 1.0
    dt = 0.01
    time = 5.0
    y = 0
    y_dot = 0
    integral = 0
    prev_error = setpoint - y
    times, outputs = [], []

    for i in range(int(time / dt)):
        t = i * dt
        error = setpoint - y
        u, integral = pid_controller(error, prev_error, integral, dt, Kp, Ki, Kd)
        y, y_dot = plant_model(y, y_dot, u, dt)
        prev_error = error
        times.append(t)
        outputs.append(y)

    return times, outputs

root = tk.Tk()
root.title("PID Controller Virtual Lab")
root.geometry("750x700")
root.configure(bg="#f4f4f4")

default_font = ("Arial", 12)
header_font = ("Arial", 14, "bold")
title_font = ("Arial", 16, "bold")

# ----- Header -----
tk.Label(root, text="Northern Technical University", font=title_font, bg="#f4f4f4").pack(pady=(5, 0))
tk.Label(root, text="Technical Engineering College", font=header_font, bg="#f4f4f4").pack()
tk.Label(root, text="Chemical and Petroleum Industries Technologies Engineering", font=default_font, bg="#f4f4f4").pack()
tk.Label(root, text="Designed by: Azam Isam", font=("Arial", 10), anchor="w", bg="#f4f4f4").pack(anchor="w", padx=10, pady=(2, 5))
ttk.Separator(root, orient='horizontal').pack(fill='x', padx=10, pady=5)
tk.Label(root, text="PID Controller Response Calculator", font=title_font, bg="#f4f4f4").pack(pady=(5, 10))

# ----- Sliders -----
def add_slider(label_text, var, default):
    frame = tk.Frame(root, bg="#f4f4f4")
    frame.pack(pady=3)
    tk.Label(frame, text=label_text, font=default_font, bg="#f4f4f4").pack()
    ttk.Scale(frame, from_=0, to=10, orient='horizontal', variable=var, length=300).pack()
    tk.Label(frame, textvariable=var, font=default_font, bg="#f4f4f4").pack()
    var.set(default)

kp_var = tk.DoubleVar()
ki_var = tk.DoubleVar()
kd_var = tk.DoubleVar()

add_slider("Kp", kp_var, 2.0)
add_slider("Ki", ki_var, 1.0)
add_slider("Kd", kd_var, 0.5)

# ----- Button -----
def update_plot():
    Kp = kp_var.get()
    Ki = ki_var.get()
    Kd = kd_var.get()
    t, y = run_simulation(Kp, Ki, Kd)

    ax.clear()
    ax.plot(t, y, linewidth=2, color="blue")
    ax.set_title("System Output vs Time", fontsize=14)
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("Output", fontsize=12)
    ax.tick_params(axis='both', labelsize=10)
    ax.grid(True)
    canvas.draw()

button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=10)

simulate_button = tk.Button(
    button_frame,
    text="Run Simulation",
    command=update_plot,
    font=("Arial", 12, "bold"),
    bg="#007bff",
    fg="white",
    activebackground="#0056b3",
    padx=16,
    pady=6
)
simulate_button.pack()

# ----- Graph -----
fig, ax = plt.subplots(figsize=(6, 3.5))  # smaller graph
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

root.mainloop()
