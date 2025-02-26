# ==============================================================
# Spectral Intensity Plot with Interactive Point Selection
# ==============================================================
# This script reads spectral data from an Excel file and visualizes 
# intensity variations over time using a custom colormap. It includes:
#  - Gradual color transition for better time representation
#  - Dynamic alpha blending for aesthetic clarity
#  - Click interaction to capture the nearest spectral point
#  - A well-integrated color bar to indicate time progression
#
# Written for precise wavelength analysis in scientific visualization.
# ==============================================================

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# ==============================================================
# 1. Data Processing - Load and Structure the Spectral Data
# ==============================================================

# Load spectral data from an Excel file (Ensure the path is correct)
df = pd.read_excel('data0206/PBC-0.xlsx', sheet_name='Sheet2')

# Print dataset dimensions for reference
num_rows, num_cols = df.shape
print(f"Loaded Data: {num_rows} rows × {num_cols} columns")

# Define intensity matrix dimensions
N_intensity = 121  # Corresponds to 10 minutes (600s)
N_wavelength = num_rows  # Number of wavelength points

# Extract Wavelength data (1st column)
WaveLength = df.iloc[:, 0].to_numpy()

# Extract Intensity data (Remaining columns)
# num_rows: different wavelength, N_intensity: actually represent the timing
Intensity = np.zeros((num_rows, N_intensity)) 
for i in range(N_intensity):
    Intensity[:, i] = df.iloc[:, i + 1].to_numpy() 

n_lines = N_intensity  # Number of time steps

# ==============================================================
# 2. Visualization Setup - Define Colormap and Aesthetic Elements
# ==============================================================

colors = [(0, 0.282, 0.510),  
          (0.608, 0.125, 0.478),  
          (0.773, 0.059, 0.078)]  

cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=n_lines)
line_colors = cmap(np.linspace(0, 1, n_lines))

# Create Figure and Axis
fig, ax = plt.subplots()

# Plot each time step with fading transparency for depth perception
for i, color in enumerate(line_colors):
    alpha = 1 - (i / n_lines)  # Gradual transparency effect
    ax.plot(WaveLength, Intensity[:, i], color=color, linewidth=1, alpha=alpha)

# ==============================================================
# 3. Formatting - Labels, Ticks, and Borders for Clarity
# ==============================================================

# X-axis Label
ax.set_xlabel("Wavelength (nm)", fontsize=20, fontweight='bold', labelpad=20)
ax.set_ylabel("Intensity(Counts)",fontsize=20, fontweight='bold', labelpad=20)

# Remove Y-axis labels and ticks for a cleaner look
ax.set_yticks([])

# Adjust X and Y axis ticks for readability
ax.tick_params(axis='x', direction='in', length=6, labelsize=14, width=1.5)
ax.tick_params(axis='y', direction='in', length=6, width=1.5)

# Bold formatting for X-axis tick labels
for label in ax.get_xticklabels():
    label.set_fontweight('bold')

# Set border thickness for a defined plot frame
for spine in ax.spines.values():
    spine.set_linewidth(2)  # Thicker frame

# ==============================================================
# 4. Time-Based Color Bar - Integrated for Easy Interpretation
# ==============================================================

# Normalize time scale for the colormap
lasttime = 10  # Last time step in minutes
norm = mpl.colors.Normalize(vmin=0, vmax=lasttime)
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Needed for color bar creation

# Add inset color bar for a refined appearance
cax = inset_axes(ax, width="2%", height="50%", loc='upper right', borderpad=10)
cbar = fig.colorbar(sm, cax=cax)
cbar.set_label('Time (min)', fontsize=20, fontweight='bold', labelpad=1)

# Customize color bar tick labels
cbar.ax.tick_params(labelsize=20, width=1.5)
cbar.ax.set_yticks([0, 2, 4, 6, 8, lasttime])
for label in cbar.ax.get_yticklabels():
    label.set_fontweight('bold')

# ==============================================================
# 5. Interactive Click Event - Capture Spectral Points
# ==============================================================

def on_click(event):
    """Capture nearest wavelength-intensity point on mouse click."""
    if event.inaxes:
        x_clicked = event.xdata
        y_clicked = event.ydata

        # Find the closest wavelength index
        idx = np.abs(WaveLength - x_clicked).argmin()
        x_nearest = WaveLength[idx]

        # Find the closest intensity value across time
        y_nearest_list = [Intensity[idx, i] for i in range(n_lines)]
        y_nearest = min(y_nearest_list, key=lambda y: abs(y - y_clicked))

        # Define threshold to filter out irrelevant clicks
        threshold = 500  # Adjust based on dataset range
        if abs(y_clicked - y_nearest) < threshold:
            print(f'Clicked on: Wavelength = {x_nearest:.2f} nm, Intensity = {y_nearest:.2f}')
            ax.plot(x_nearest, y_nearest, 'ro', markersize=8)  # Mark the clicked point
            fig.canvas.draw()

# Bind click event to function
fig.canvas.mpl_connect('button_press_event', on_click)

# ==============================================================
# 6. Display Plot - Ready for Analysis
# ==============================================================

plt.show()
exit()
