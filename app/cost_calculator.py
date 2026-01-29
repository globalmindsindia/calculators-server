import pandas as pd
import os

def calculate_total_cost(selected_buckets):
    try:
        # Use hardcoded bucket mapping instead of Excel file
        bucket_mapping = {
            'Bucket-1': 1500,
            'Bucket-2': 75000,
            'Bucket-3': 21000,
            'Bucket-4': 75000,
            'Bucket-5': 125000,
            'Bucket-6': 100000,
            'Bucket-7': 80000
        }
        
        # Calculate total from selected buckets
        total_cost = sum(bucket_mapping.get(bucket, 0) for bucket in selected_buckets)
        
        print(f"DEBUG: Selected buckets: {selected_buckets}")
        print(f"DEBUG: Individual costs: {[bucket_mapping.get(bucket, 0) for bucket in selected_buckets]}")
        print(f"DEBUG: Total calculated: {total_cost}")
        
        return int(total_cost)
    except Exception as e:
        print("Error:", str(e))
        return None