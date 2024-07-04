import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read results from CSV and create a heatmap
def create_heatmap(csv_file, title, output_image):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Map "yes" to 1 and "no" to 0
    df['Correct Measurement'] = df['Correct Measurement'].map({'yes': 1, 'no': 0})
    
    # Pivot the DataFrame to get positions as rows and mean distances as columns
    df_pivot = df.pivot(index="Position", columns="Mean Distance (cm)", values="Correct Measurement")
    
    # Create a heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_pivot, annot=True, cmap="YlGnBu", cbar=False, fmt='g')
    plt.title(title)
    plt.xlabel('Mean Distance (cm)')
    plt.ylabel('Position')
    plt.savefig(output_image)
    plt.show()

# Create heatmaps for each scenario
create_heatmap('round_object_results.csv', 'Correct Measurements for Round Object', 'round_object_heatmap.png')
create_heatmap('square_object_results.csv', 'Correct Measurements for Square Object (0°)', 'square_object_heatmap.png')
create_heatmap('square_object_45_results.csv', 'Correct Measurements for Square Object (45°)', 'square_object_45_heatmap.png')
