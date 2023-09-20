import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

# Global variables
plot_lines = {}  # Store lines for each trajectory with corresponding labels
show_grid = True  # Initial grid state
x_range = 20  # Initial x-axis range
y_range = 20  # Initial y-axis range
canvas = None  # Initialize the canvas variable

# Function to simulate projectile motion and update the plot
def simulate():
    global plot_lines, show_grid, x_range, y_range, canvas
    
    # Get the values from input fields
    angle_str = angle_entry.get()
    velocity_str = velocity_entry.get()
    air_resistance_str = air_resistance_entry.get()
    
    # Validate input
    if not angle_str or not velocity_str:
        # Handle case where angle or velocity is empty
        # You can display an error message or handle it as you prefer
        return
    
    try:
        angle = float(angle_str)
        velocity = float(velocity_str)
        if air_resistance_str:
            air_resistance = float(air_resistance_str)
        else:
            air_resistance = 0.0  # Default to zero if air resistance is not provided
        
        # Calculate the physics simulation results
        time_of_flight = (2 * velocity * np.sin(np.radians(angle))) / (9.8 + air_resistance)
        max_height = (velocity ** 2) * (np.sin(np.radians(angle)) ** 2) / (2 * (9.8 + air_resistance))
        range_val = (velocity ** 2) * np.sin(np.radians(2 * angle)) / (9.8 + air_resistance)
        
        # Create time values for trajectory calculation
        t = np.linspace(0, time_of_flight, 100)
        x_values = velocity * np.cos(np.radians(angle)) * t
        y_values = velocity * np.sin(np.radians(angle)) * t - (0.5 * (9.8 + air_resistance) * t ** 2)
        
        # Update information labels with calculated values
        max_height_label.config(text=f"Max Height: {max_height:.2f} m")
        range_label.config(text=f"Range: {range_val:.2f} m")
        time_of_flight_label.config(text=f"Time of Flight: {time_of_flight:.2f} s")
        
        # Plot the trajectory
        line, = ax.plot(x_values, y_values, linestyle='-', marker='o', markersize=5)
        plot_lines[line] = f'Trajectory {len(plot_lines) + 1}'  # Store line with label
        update_legend_dropdown()
        
        # Show/hide grid based on the checkbox
        ax.grid(show_grid)

        # Set x-axis and y-axis limits based on the slider values
        ax.set_xlim(0, x_range)
        ax.set_ylim(0, y_range)

        # Redraw the canvas
        canvas.draw()
    
    except ValueError:
        # Handle the case where the input cannot be converted to floats
        # You can display an error message or handle it as you prefer
        pass

# Function to toggle grid marks
def toggle_grid():
    global show_grid
    show_grid = not show_grid
    ax.grid(show_grid)
    canvas.draw()

# Function to update x-axis range
def update_x_range():
    global x_range
    x_range_start = float(x_range_start_entry.get())
    x_range_end = float(x_range_end_entry.get())
    
    # Check if the range is valid
    if x_range_start >= x_range_end:
        # Set default values if the range is invalid
        x_range_start = 0
        x_range_end = 20
    
    x_range = x_range_end
    ax.set_xlim(x_range_start, x_range_end)
    canvas.draw()

# Function to update y-axis range
def update_y_range():
    global y_range
    y_range_start = float(y_range_start_entry.get())
    y_range_end = float(y_range_end_entry.get())
    
    # Check if the range is valid
    if y_range_start >= y_range_end:
        # Set default values if the range is invalid
        y_range_start = 0
        y_range_end = 20
    
    y_range = y_range_end
    ax.set_ylim(y_range_start, y_range_end)
    canvas.draw()

# Function to clear the plot
def clear_plot():
    global plot_lines
    for line in plot_lines.keys():
        line.remove()
    plot_lines.clear()
    update_legend_dropdown()  # Clear the legend dropdown
    canvas.draw()

# Function to handle mouse wheel event for zooming
def on_mousewheel(event):
    global x_range, y_range
    x_range_start, x_range_end = ax.get_xlim()
    y_range_start, y_range_end = ax.get_ylim()

    x_scale_factor = 0.1  # Adjust the scaling factor as needed (smaller value for slower zoom)
    y_scale_factor = 0.1

    if event.delta > 0:
        # Zoom in
        x_range_start += (x_range_end - x_range_start) * x_scale_factor
        x_range_end -= (x_range_end - x_range_start) * x_scale_factor
        y_range_start += (y_range_end - y_range_start) * y_scale_factor
        y_range_end -= (y_range_end - y_range_start) * y_scale_factor
    else:
        # Zoom out
        x_range_start -= (x_range_end - x_range_start) * x_scale_factor
        x_range_end += (x_range_end - x_range_start) * x_scale_factor
        y_range_start -= (y_range_end - y_range_start) * y_scale_factor
        y_range_end += (y_range_end - y_range_start) * y_scale_factor
    
    ax.set_xlim(max(0, x_range_start), max(0, x_range_end))
    ax.set_ylim(max(0, y_range_start), max(0, y_range_end))
    canvas.draw()

# Function to update the legend dropdown
def update_legend_dropdown():
    trajectory_names = list(plot_lines.values())
    trajectory_dropdown['values'] = trajectory_names

# Function to handle legend selection in the dropdown
def select_trajectory(event):
    selected_trajectory_name = trajectory_dropdown.get()
    selected_line = None

    # Find the line associated with the selected trajectory name
    for line, label in plot_lines.items():
        if label == selected_trajectory_name:
            selected_line = line
            break

    if selected_line:
        # Highlight the selected line
        for line in plot_lines.keys():
            line.set_alpha(0.2)  # Dim all lines
        selected_line.set_alpha(1.0)  # Highlight selected line
        canvas.draw()

# Create the main window
root = tk.Tk()
root.title("2D Projectile Motion Simulator")

# Add a window close event handler
root.protocol("WM_DELETE_WINDOW", root.quit)

# Create a frame for the input widgets
input_frame = ttk.Frame(root)
input_frame.pack(fill=tk.BOTH, expand=True)

# First Row: Launch Angle, Initial Velocity, Air Resistance
angle_frame = ttk.Frame(input_frame)
angle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

angle_label = ttk.Label(angle_frame, text="Launch Angle (degrees):")
angle_label.pack(side=tk.TOP, padx=5, pady=5)
angle_entry = ttk.Entry(angle_frame)
angle_entry.pack(side=tk.TOP, padx=5, pady=5)

velocity_label = ttk.Label(angle_frame, text="Initial Velocity (m/s):")
velocity_label.pack(side=tk.TOP, padx=5, pady=5)
velocity_entry = ttk.Entry(angle_frame)
velocity_entry.pack(side=tk.TOP, padx=5, pady=5)

air_resistance_label = ttk.Label(angle_frame, text="Air Resistance (optional):")
air_resistance_label.pack(side=tk.TOP, padx=5, pady=5)
air_resistance_entry = ttk.Entry(angle_frame)
air_resistance_entry.pack(side=tk.TOP, padx=5, pady=5)

# Second Row: X-Axis Range, Y-Axis Range, Clear Button
range_frame = ttk.Frame(input_frame)
range_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

x_range_label = ttk.Label(range_frame, text="X-Axis Range:")
x_range_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

x_range_start_label = ttk.Label(range_frame, text="Start:")
x_range_start_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
x_range_start_entry = ttk.Entry(range_frame)
x_range_start_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

x_range_end_label = ttk.Label(range_frame, text="End:")
x_range_end_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
x_range_end_entry = ttk.Entry(range_frame)
x_range_end_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

x_range_apply_button = ttk.Button(range_frame, text="Apply", command=update_x_range)
x_range_apply_button.grid(row=1, column=4, padx=5, pady=5, sticky="w")

y_range_label = ttk.Label(range_frame, text="Y-Axis Range:")
y_range_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

y_range_start_label = ttk.Label(range_frame, text="Start:")
y_range_start_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
y_range_start_entry = ttk.Entry(range_frame)
y_range_start_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

y_range_end_label = ttk.Label(range_frame, text="End:")
y_range_end_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")
y_range_end_entry = ttk.Entry(range_frame)
y_range_end_entry.grid(row=3, column=3, padx=5, pady=5, sticky="w")

y_range_apply_button = ttk.Button(range_frame, text="Apply", command=update_y_range)
y_range_apply_button.grid(row=3, column=4, padx=5, pady=5, sticky="w")

# Clear Button (Same row as the range entries)
clear_button = ttk.Button(range_frame, text="Clear Plot", command=clear_plot)
clear_button.grid(row=1, column=5, rowspan=3, padx=5, pady=5, sticky="w")

# Third Row: Max Height, Range, Time of Flight
metrics_frame = ttk.Frame(input_frame)
metrics_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

max_height_label = ttk.Label(metrics_frame, text="Max Height:")
max_height_label.pack(side=tk.TOP, padx=5, pady=5)
range_label = ttk.Label(metrics_frame, text="Range:")
range_label.pack(side=tk.TOP, padx=5, pady=5)
time_of_flight_label = ttk.Label(metrics_frame, text="Time of Flight:")
time_of_flight_label.pack(side=tk.TOP, padx=5, pady=5)

# Generate Button (Spanning all columns)
generate_button = ttk.Button(root, text="Generate", command=simulate)
generate_button.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a Matplotlib figure for the trajectory plot
fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111)
ax.set_xlabel('Horizontal Distance (m)')
ax.set_ylabel('Vertical Distance (m)')
ax.set_title('Projectile Motion')
ax.grid(show_grid)

# Create the FigureCanvasTkAgg object
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Add navigation tools to the Matplotlib figure
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Bind mousewheel event to the canvas for zooming
canvas.get_tk_widget().bind("<MouseWheel>", on_mousewheel)

# Legend Dropdown
trajectory_dropdown = ttk.Combobox(root, values=[], state="readonly")
trajectory_dropdown.bind("<<ComboboxSelected>>", select_trajectory)
trajectory_dropdown.pack(pady=5)

# Start the GUI event loop
root.mainloop()
