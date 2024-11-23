import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib as mpl
import pandas as pd
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
    # print("Number of rows:",i)
# print("WaveLength:",WaveLength)
# print("Intensity:",Intensity)
n_lines = N_intensity
# cmap = mpl.colormaps['Blues']
# cmap = mpl.colormaps['inferno']
# cmap = mpl.colormaps['Pastel1'] 
# cmap = mpl.colormaps['cividis'] 
# cmap = mpl.colormaps['plasma']
# colors = cmap(np.linspace(0, n_lines/30, n_lines))

# colors = ['blue', 'purple', 'red']  # Define your gradient
colors = [(0, 0.282, 0.510),  # Blue
          (0.608, 0.125, 0.478),  # Green
          (0.773, 0.059, 0.078)]  # Red
cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=n_lines)
# Generate colors for the plot
line_colors = cmap(np.linspace(0, 1, n_lines))
fig, ax = plt.subplots()
for i, color in enumerate(line_colors):
    alpha = 1 - (i / n_lines)  # Example: Gradual transparency
    rgba_color = list(color[:3]) + [alpha]  # Add the dynamic alpha
    ax.plot(WaveLength, Intensity[:, i], color=color, linewidth=0.4)
    # if np.any(Intensity[:, i] > 1000):  # If there are any values > 1000
    #     print(f"Values larger than 1000 in Intensity column {i+1}:")
    #     print(Intensity[Intensity[:, i] > 1000, i])  # Print values larger than 1000
    #     print()  # Print an empty line for clarity
    print("number of i:", i)

# Create a ScalarMappable for the color bar
norm = mpl.colors.Normalize(vmin=0, vmax=10)  # Normalize line indices to colormap
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Required for the color bar

# Add the color bar to the figure
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Time(min)')  # Label for the color bar
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Intensity")

# Move spines (XY axis lines) inside the plot
# ax.spines['top'].set_position('zero')  # Move the top spine to inside
# ax.spines['right'].set_position('zero')  # Move the right spine to inside
# ax.spines['left'].set_position('zero')  # Move the left spine to inside
# ax.spines['bottom'].set_position('zero')  # Move the bottom spine to inside

# # Make sure the ticks are inside the plot too
ax.tick_params(axis='x', direction='in', length=6)
ax.tick_params(axis='y', direction='in', length=6)


plt.show()

exit()

