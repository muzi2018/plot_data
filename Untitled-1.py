import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl


import pandas as pd

###--- Data Processing ---###
df = pd.read_excel('B0PC-heatup.xlsx', sheet_name='Sheet2')
num_rows, num_cols = df.shape
print("Number of rows:", num_rows)
print("Number of columns:", num_cols)

### Wavelength [nm] 857 rows; Intensity  138 columns ###
### Time = 137 x 5s = 685 s ---> 121 colums of Intensity
delt_T = 5 # m
N_intensity = 121
N_wavelength = 857
time = (N_intensity - 1) * delt_T

WaveLength = df.iloc[:, 0].to_numpy() 
Intensity = np.zeros((num_rows, num_cols-1))

for i in range(0, num_cols - 1):
    Intensity[:, i] = df.iloc[:, i+1].to_numpy()
    # print("Number of rows:",i)

n_lines = 3
cmap = mpl.colormaps['plasma']
colors = cmap(np.linspace(0, 1, n_lines))
fig, ax = plt.subplots()
for i, color in enumerate(colors):
    ax.plot(WaveLength, Intensity[:, i], color=color)



# ### Plotting data ###
# arr1 = np.array([1, 2, 3, 4, 5])
# # From a tuple
# arr2 = np.array((1, 3, 1, 2, 1))
# ax.plot(arr1, arr2)
# plt.show()
# exit()


# Create a ScalarMappable for the color bar
norm = mpl.colors.Normalize(vmin=0, vmax=n_lines - 1)  # Normalize line indices to colormap
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Required for the color bar

# Add the color bar to the figure
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Line Index')  # Label for the color bar

plt.show()







    
# print("Intensity = ", Intensity)
    # for j in range()
    # column_array = df.iloc[i, 0].to_numpy() 
    # print("column_array = ", column_array)
    # Intensity[i, :, 0] = column_array.flatten()


# print("Wave Length:", WaveLength)
# print("--------------------")

### (wave_length[0, :], intensity[0, 0, :]) - (wave_length[0, :], intensity[0, 1, :]) -...-
### (wave_length[0, :], intensity[0, 856, :])

exit()


### Plotting parameter###
n_lines = N
cmap = mpl.colormaps['plasma']
colors = cmap(np.linspace(0, 1, n_lines))
fig, ax = plt.subplots()



# ### Plotting data ###
# arr1 = np.array([1, 2, 3, 4, 5])
# # From a tuple
# arr2 = np.array((1, 3, 1, 2, 1))
# ax.plot(arr1, arr2)




for i, color in enumerate(colors):
    ax.plot([arr1, arr2], color=color)

# print("Row Array:", row_array)  # Output: [1 2 3 4]
# print("Column Array:", col_array)  # Output: [5 6 7 8]





n_lines = 21
cmap = mpl.colormaps['plasma']

# Take colors at regular intervals spanning the colormap.
colors = cmap(np.linspace(0, 1, n_lines))

fig, ax = plt.subplots()

arr1 = np.array([1, 2, 3, 4, 5])
# From a tuple
arr2 = np.array((1, 3, 1, 2, 1))
ax.plot(arr1, arr2)

# Plot the lines

## 

# for i, color in enumerate(colors):
#     ax.plot([arr1, arr2], color=color)




# Create a ScalarMappable for the color bar
norm = mpl.colors.Normalize(vmin=0, vmax=n_lines - 1)  # Normalize line indices to colormap
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Required for the color bar

# Add the color bar to the figure
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Line Index')  # Label for the color bar

plt.show()