import pandas as pd
import matplotlib.pyplot as plt

import scienceplots
plt.style.use('science')
plt.style.use('nature')

scale = 1
labelsize=28
titlesize=40
textsize=24
size_marker = 100

labelsize *= scale
titlesize*= scale
textsize*=scale
size_marker*=scale
# Set global font sizes
plt.rcParams['text.usetex'] = True
plt.rcParams['figure.figsize'] = (20,15)
plt.rcParams['font.size'] = textsize  # Sets default font size
plt.rcParams['axes.labelsize'] = labelsize
plt.rcParams['axes.titlesize'] = titlesize
plt.rcParams['xtick.labelsize'] = labelsize
plt.rcParams['ytick.labelsize'] = labelsize
plt.rcParams['legend.fontsize'] = labelsize
plt.rcParams['errorbar.capsize'] = 4
plt.rcParams['lines.markersize'] = 6  # For example, 8 points
plt.rcParams['lines.linewidth'] = 2 # For example, 2 points
# Set global parameters using rcParams
plt.rcParams['axes.titlepad'] = 20  # Padding above the title
plt.rcParams['axes.labelpad'] = 15  # Padding for both x and y axis labels


# Load the CSV data into a DataFrame
file_path = 'scan_data.csv'
data = pd.read_csv(file_path)

# Filter the data by SVOLT values
data_48 = data[data['SVOLT'] == 48.0]
data_55 = data[data['SVOLT'] == 55.0]


# Define the ranges
range_48 = (-1e-7, -1e-8)
range_55 = (-5e-5, -1e-6)

# Count the number of entries within the specified ranges
count_48 = data_48[(data_48['CURRENT'] >= range_48[0]) & (data_48['CURRENT'] <= range_48[1])].shape[0]
count_55 = data_55[(data_55['CURRENT'] >= range_55[0]) & (data_55['CURRENT'] <= range_55[1])].shape[0]

# Print the counts
print(f'Number of entries for 48V in range {range_48}: {count_48}')
print(f'Number of entries for 55V in range {range_55}: {count_55}')

# Plotting the histograms
plt.figure()

binning48 = [i*2e-9 for i in range(1,50)]
binning55 = [i*5e-7 for i in range(1,100)]
plt.hist(-data_48['CURRENT'], bins=binning48, alpha=0.5, label='48V')
plt.hist(-data_55['CURRENT'], bins=binning55, alpha=0.5, label='55V')

# Annotate the plot with the counts
#plt.text(0.7, 0.85, f'48V: {count_48}', transform=plt.gca().transAxes, verticalalignment='top')
#plt.text(0.7, 0.8, f'55V: {count_55}', transform=plt.gca().transAxes, verticalalignment='top')
#plt.text(0.7, 0.75, f'Total SiPM: 19296', transform=plt.gca().transAxes, verticalalignment='top')
plt.xlabel('Current (A)')
plt.ylabel('Number of SiPM')
plt.xlim(2e-8, 1e-4)
plt.xscale('log')
#plt.title('Histogram of Currents for Different SVOLT Values')
plt.legend()
#plt.grid(True)

# Show the plot
#plt.show()
plt.savefig("currents.pdf")

