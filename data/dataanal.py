import pandas as pd

# Load the data from CSV file
file_path = r'C:\AmazonStreamlit\data\RawAmazonData.csv'
data = pd.read_csv(file_path)

# Fields to analyze for unique values
fields = ['ChannelName', 'AgentShift', 'ProductCategory']

# Path for the output text file
output_path = r'C:\AmazonStreamlit\data\unique_values.txt'

# Open the file in write mode
with open(output_path, 'w') as file:
    for field in fields:
        # Get unique values, consider NaN as a unique value
        unique_values = data[field].unique()
        # Replace nan with a string to indicate blanks explicitly
        unique_values = [str(val) if pd.notna(val) else 'BLANK' for val in unique_values]
        
        # Write to file
        file.write(f"Unique values in {field}:\n")
        file.writelines(f"{value}\n" for value in unique_values)
        file.write("\n")

print(f"Unique values have been written to {output_path}")
