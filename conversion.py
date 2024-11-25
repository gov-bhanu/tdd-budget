import pandas as pd

# Function to read and transform the Excel file
def transform_excel(file_path, output_path):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name=None, header=None)  # Read all sheets, no header

    # Create an empty list to store the transformed data
    transformed_data = []

    # Process each sheet
    for sheet_name, sheet_df in df.items():
        # Initialize variables for the department, scheme ID, and scheme name
        department = None
        scheme_id = None
        scheme_name = None

        # Iterate through each row in the sheet
        for index, row in sheet_df.iterrows():
            # Check for Department (non-empty in the first column and not "TOTAL")
            if pd.notna(row.iloc[0]) and "TOTAL" not in str(row.iloc[0]):
                department = row.iloc[0]
            
            # Check for Scheme ID and Name (second and third columns)
            elif pd.notna(row.iloc[1]) and pd.notna(row.iloc[2]):
                scheme_id = row.iloc[1]
                scheme_name = row.iloc[2]
            
            # If there's an Expense Category in the fourth column, process it
            elif pd.notna(row.iloc[3]) and "Total" not in str(row.iloc[3]):
                expense_category = row.iloc[3]
                # Add the record to the transformed data
                transformed_data.append([department, scheme_id, scheme_name, expense_category])

    # Convert the transformed data to a DataFrame
    transformed_df = pd.DataFrame(transformed_data, columns=['Department', 'Scheme ID', 'Scheme Name', 'Expense Category'])

    # Save the transformed data to a new Excel file
    transformed_df.to_excel(output_path, index=False)

# Example usage with raw string format for file paths
file_path = r'C:\Users\govbh\Downloads\conversion.xlsx'  # Provide the path to your input Excel file
output_path = r'C:\Users\govbh\Downloads\transformed_data.xlsx'  # Provide the path for the output Excel file

transform_excel(file_path, output_path)
