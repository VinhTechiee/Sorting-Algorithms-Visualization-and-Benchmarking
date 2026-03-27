import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file
df = pd.read_csv('benchmark_results.csv')

# Convert the necessary columns to numeric and handle errors by coercing invalid data to NaN
df['ExecutionTime(ms)'] = pd.to_numeric(df['ExecutionTime(ms)'], errors='coerce')
df['InputSize'] = pd.to_numeric(df['InputSize'], errors='coerce')

# Drop rows with NaN values in 'ExecutionTime(ms)' or 'InputSize' columns
df = df.dropna(subset=['ExecutionTime(ms)', 'InputSize'])

# Check the data types of the columns
print("Data types after conversion:")
print(df.dtypes)

# Group by Algorithm and InputSize, then calculate the average execution time
# Only calculate the mean for numeric columns
df_grouped = df.groupby(['Algorithm', 'InputSize'], as_index=False)['ExecutionTime(ms)'].mean()

# Display grouped data to verify
print("\nGrouped data:")
print(df_grouped.head())

# Plot the results with a log scale for the y-axis
plt.figure(figsize=(10, 6))

# Plot data for each algorithm
for algorithm in df_grouped['Algorithm'].unique():
    data = df_grouped[df_grouped['Algorithm'] == algorithm]
    plt.plot(data['InputSize'], data['ExecutionTime(ms)'], label=algorithm)

# Set labels and title for the plot
plt.xlabel('Input Size')
plt.ylabel('Execution Time (ms)')
plt.title('Benchmark of Sorting Algorithms')
plt.legend()
plt.grid(True)

# Apply log scale for y-axis to better visualize large differences
plt.yscale('log')

# Save the plot as an image
plt.savefig('benchmark_plot.png')  # Saves the plot to a PNG file


# Show the plot
plt.show()