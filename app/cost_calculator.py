import pandas as pd
import os

def calculate_total_cost(selected_buckets):
    try:
        # Load the Excel file
        excel_path = os.path.join(os.path.dirname(__file__), 'services.xlsx')
        df = pd.read_excel(excel_path)

        # Clean the Prices column: remove commas and convert to float
        df['Prices'] = df['Prices'].replace({',': ''}, regex=True).astype(float)

        # Filter rows where the 'Buckets' match the selected list
        filtered_df = df[df['Buckets'].isin(selected_buckets)]

        # Sum the prices
        total_cost = filtered_df['Prices'].sum()

        return int(total_cost)  # Convert to int for clean output
    except Exception as e:
        print("Error:", str(e))
        return None