import numpy as np
import pyvista as pv

# --- EM wave parameters ---
E0 = 0.4
B0 = 0.4
k = 4 * np.pi / 1.0  # doubled frequency → half wavelength

# --- z-axis: propagation direction (0 to 2) ---
z = np.linspace(0, 2, 300)

# --- Field lines: sinusoidal variation along z ---
x_E = E0 * np.cos(k * z)  # E-field in x-direction
y_E = np.zeros_like(z)

x_B = np.zeros_like(z)
y_B = B0 * np.cos(k * z)  # B-field in y-direction

# --- 3D coordinates for field lines ---
points_E = np.column_stack((x_E, y_E, z))
points_B = np.column_stack((x_B, y_B, z))

# --- PyVista lines from points ---
line_E = pv.lines_from_points(points_E)
line_B = pv.lines_from_points(points_B)

# --- Create coordinate system arrows (unit length, same color) ---
arrow_len = 0.6
arrow_radius = 0.01
arrow_color = "gray"

arrow_x = pv.Arrow(start=(0, 0, 0), direction=(-1, 0, 0),  # reversed x-axis
                   tip_length=0.2, tip_radius=0.03,
                   shaft_radius=arrow_radius, scale=arrow_len)
arrow_y = pv.Arrow(start=(0, 0, 0), direction=(0, 1, 0),
                   tip_length=0.2, tip_radius=0.03,
                   shaft_radius=arrow_radius, scale=arrow_len)
arrow_z = pv.Arrow(start=(0, 0, 0), direction=(0, 0, 1),
                   tip_length=0.2, tip_radius=0.03,
                   shaft_radius=arrow_radius, scale=arrow_len)

# --- Plotter setup ---
plotter = pv.Plotter(window_size=(1000, 600))
plotter.set_background("white")
plotter.renderer.SetBackgroundAlpha(0)

# --- Add field lines ---
plotter.add_mesh(line_E, color="orange", line_width=4, label="E-field")
plotter.add_mesh(line_B, color="blue", line_width=4, label="B-field")

# --- Add coordinate system arrows ---
plotter.add_mesh(arrow_x, color=arrow_color)
plotter.add_mesh(arrow_y, color=arrow_color)
plotter.add_mesh(arrow_z, color=arrow_color)

# --- Axis labels near arrow tips (font size larger, offset further, visually centered) ---
label_offset = 0.75
plotter.add_point_labels(
    [(-label_offset, 0, 0),  # ← x-label links raus
     (0, label_offset, 0),   # y-label oben
     (0, 0, label_offset)],  # z-label vorne
    ["x", "y", "z"],
    font_size=36,
    text_color="black",
    point_color="white",
    shape_opacity=0.0,
    always_visible=True
)

# --- Camera setup ---
plotter.view_vector([-4.8, 1.5, 2.5], viewup=[.2, 1, -.15])
plotter.camera.zoom(1.4)
plotter.add_legend()
plotter.hide_axes_all()

# --- Show scene interactively ---
plotter.show(auto_close=False, interactive=False)

# --- Print camera view ---
cpos = plotter.camera_position
print("View vector (camera position):", np.array(cpos[0]))
print("Focal point (looks at):       ", np.array(cpos[1]))
print("View up vector:               ", np.array(cpos[2]))

# --- Save screenshot ---
plotter.screenshot("em_wave.png", transparent_background=True)
plotter.close()
