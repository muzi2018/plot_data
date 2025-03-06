import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.signal import find_peaks

#下降到30%，70%，5min峰值下降

### Color : https://matplotlib.org/stable/users/explain/colors/colormaps.html
###--- Data Processing ---###
# df = pd.read_excel('B0PC-heatup.xlsx', sheet_name='Sheet2')
# df = pd.read_excel('data0206/PBC-0.xlsx', sheet_name='Sheet2') # group 1
df = pd.read_excel('data0206/pbc-b10.xlsx', sheet_name='Sheet2') # group 2

# Number of rows: 55
# Number of columns: 1700

num_rows, num_cols = df.shape
print("Number of rows:", num_rows)
print("Number of columns:", num_cols)

### Wavelength [nm] 1659 rows; Intensity  235 columns ###
### Time = 235 x 5s = 1175 s ---> 121 colums of Intensity = 600 s = 10 min
N_intensity = 121 # 10 min
# N_intensity = 61
N_wavelength = num_rows # 1659
print("Number of N_intensity:", N_intensity)
print("Number of N_wavelength:", N_wavelength)

WaveLength = df.iloc[:, 0].to_numpy() # 1659 rows
# print("the WaveLength = ", WaveLength)
Intensity = np.zeros((num_rows, N_intensity)) # 1659 x 121
for i in range(0, N_intensity):
    Intensity[:, i] = df.iloc[:, i+1].to_numpy()
n_lines = N_intensity

#---- Color ----
colors = [(0, 0.282, 0.510),        # Blue
          (0.608, 0.125, 0.478),    # Green
          (0.773, 0.059, 0.078)]    # Red
cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=n_lines)
line_colors = cmap(np.linspace(0, 1, n_lines))

fig, ax = plt.subplots()
for i, color in enumerate(line_colors):
    alpha = 1 - (i / n_lines)  # Example: Gradual transparency
    rgba_color = list(color[:3]) + [alpha]  # Add the dynamic alpha
    ax.plot(WaveLength, Intensity[:, i], color=color, linewidth=1)

# ---- Step: Find Peak in 60th Curve ----
curve_60 = Intensity[:, 71]  # 60th curve (Python index starts from 0)

peaks_60, _ = find_peaks(curve_60)  # Find peaks

if len(peaks_60) > 0:
    peak_60_idx = peaks_60[np.argmax(curve_60[peaks_60])]  # Highest peak index
    peak_60_wavelength = WaveLength[peak_60_idx]  # Peak wavelength
    peak_60_intensity = curve_60[peak_60_idx]  # Peak intensity

    print(f"60th Curve Peak: {peak_60_intensity:.2f} at {peak_60_wavelength:.2f} nm")

    # Plot peak on graph
    ax.plot(peak_60_wavelength, peak_60_intensity, 'go', markersize=8, label="60th Curve Peak")

    # Add legend
    ax.legend(fontsize=14)

plt.show()



# Create a ScalarMappable for the color bar
lasttime = 10
norm = mpl.colors.Normalize(vmin=0, vmax=lasttime)  # Normalize line indices to colormap
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Required for the color bar

# # Add the color bar to the figure
# cbar = fig.colorbar(sm, ax=ax)
# cbar.set_label('Time(min)',fontsize=14, fontweight='bold')  # Label for the color bar
# # Adjust colorbar tick labels (increase size and make them bold)
# cbar.ax.tick_params(labelsize=14, width=1.5)
# cbar.ax.set_yticks([0, 10])
# for label in cbar.ax.get_yticklabels():
#     label.set_fontweight('bold')

    
#---- axis Label Parameter----
ax.set_xlabel("Wavelength (nm)", fontsize=20, fontweight='bold', labelpad=20)  # Increase labelpad for more distance
ax.set_ylabel("Intensity(Counts)",fontsize=20, fontweight='bold', labelpad=20)
ax.set_xlim(350, 650)

# # Set custom ticks with scientific notation
# ax.set_xticks([0, 3e4, 5e4])  # Define specific x-axis ticks (0, 1e2, 2e2)
ax.set_yticks([0, 1e4, 1.5e4])  # Define specific y-axis ticks (0, 1e3, 2e3, 3e3)

# Format tick labels in scientific notation
# ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0e}'))  # X-axis

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:.0e}'))  # Y-axis
# Add this line after setting up your plot
ax.set_yticklabels([])

# Make sure the ticks are inside the plot too
ax.tick_params(axis='x', direction='in', length=6, labelsize=14, width=1.5)
ax.tick_params(axis='y', direction='in', length=6, labelsize=14, width=1.5)

for label in ax.get_yticklabels():
    label.set_fontweight('bold')
for label in ax.get_xticklabels():
    label.set_fontweight('bold')
    
# Modify plot border thickness 
border_thickness = 2  # 3mm in points
for spine in ax.spines.values():
    spine.set_linewidth(border_thickness)

# Create an inset_axes object for the color bar inside the plot
cax = inset_axes(ax, width="2%", height="50%", loc='upper right', borderpad=10)  # Adjust 'loc' and 'borderpad'
# Add the color bar to the inset_axes
cbar = fig.colorbar(sm, cax=cax)
cbar.set_label('Time(min)', fontsize=20, fontweight='bold', labelpad=1) # Color bar label
cbar.ax.tick_params(labelsize=20, width=1.5)  # Adjust ticks
cbar.ax.set_yticks([0, 2, 4, 6, 8, lasttime])
for label in cbar.ax.get_yticklabels():
    label.set_fontweight('bold')
    
    
    
# **Function to capture only points on the line**
def on_click(event):
    if event.inaxes:  # Check if the click is inside the plot
        x_clicked = event.xdata
        y_clicked = event.ydata

        # Find the closest x index in the dataset
        idx = np.abs(WaveLength - x_clicked).argmin()
        x_nearest = WaveLength[idx]

        # Find the nearest y-value by searching across all plotted lines
        y_nearest_list = [Intensity[idx, i] for i in range(n_lines)]
        y_nearest = min(y_nearest_list, key=lambda y: abs(y - y_clicked))  # Pick the closest intensity value

        # Define a threshold to ignore points far from the line
        threshold = 500  # Adjust this based on data range
        if abs(y_clicked - y_nearest) < threshold:
            print(f'Clicked on line at: x = {x_nearest:.2f}, y = {y_nearest:.2f}')
            ax.plot(x_nearest, y_nearest, 'ro', markersize=8)  # Mark the clicked point
            fig.canvas.draw()  # Update the plot dynamically


fig.canvas.mpl_connect('button_press_event', on_click)


plt.show()
exit()


