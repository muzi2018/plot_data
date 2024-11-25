import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

### Color : https://matplotlib.org/stable/users/explain/colors/colormaps.html
###--- Data Processing ---###
df = pd.read_excel('B0PC-heatup.xlsx', sheet_name='Sheet2')
num_rows, num_cols = df.shape
print("Number of rows:", num_rows)
print("Number of columns:", num_cols)

### Wavelength [nm] 857 rows; Intensity  138 columns ###
### Time = 137 x 5s = 685 s ---> 121 colums of Intensity
N_intensity = 121
N_wavelength = num_rows

WaveLength = df.iloc[:, 0].to_numpy() 
Intensity = np.zeros((num_rows, N_intensity))
for i in range(0, N_intensity):
    Intensity[:, i] = df.iloc[:, i+1].to_numpy()
n_lines = N_intensity

#---- Color ----
colors = [(0, 0.282, 0.510),  # Blue
          (0.608, 0.125, 0.478),  # Green
          (0.773, 0.059, 0.078)]  # Red
cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=n_lines)
line_colors = cmap(np.linspace(0, 1, n_lines))
fig, ax = plt.subplots()
for i, color in enumerate(line_colors):
    alpha = 1 - (i / n_lines)  # Example: Gradual transparency
    rgba_color = list(color[:3]) + [alpha]  # Add the dynamic alpha
    ax.plot(WaveLength, Intensity[:, i], color=color, linewidth=1)

# Create a ScalarMappable for the color bar
norm = mpl.colors.Normalize(vmin=0, vmax=10)  # Normalize line indices to colormap
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
ax.set_xlabel("Wavelength (nm)", fontsize=14, fontweight='bold', labelpad=20)  # Increase labelpad for more distance
ax.set_ylabel("Intensity(Counts)",fontsize=14, fontweight='bold', labelpad=20)
ax.set_xlim(350, 600)

# # Set custom ticks with scientific notation
# ax.set_xticks([0, 3e4, 5e4])  # Define specific x-axis ticks (0, 1e2, 2e2)
ax.set_yticks([0, 3e4, 6e4])  # Define specific y-axis ticks (0, 1e3, 2e3, 3e3)

# Format tick labels in scientific notation
# ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0e}'))  # X-axis
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:.0e}'))  # Y-axis


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
cax = inset_axes(ax, width="2%", height="50%", loc='upper right', borderpad=4)  # Adjust 'loc' and 'borderpad'
# Add the color bar to the inset_axes
cbar = fig.colorbar(sm, cax=cax)
cbar.set_label('Time(min)', fontsize=14, fontweight='bold', labelpad=1) # Color bar label
cbar.ax.tick_params(labelsize=12, width=1.5)  # Adjust ticks
cbar.ax.set_yticks([0, 10])
for label in cbar.ax.get_yticklabels():
    label.set_fontweight('bold')
    
plt.show()
exit()

