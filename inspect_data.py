import pandas as pd
import os

file_path = os.path.join("data", "laptops.csv")

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found. Please ensure laptops.csv is in the data folder.")
else:
    df = pd.read_csv(file_path, low_memory=False)
    print("Dataset Loaded Successfully!")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    # Preview important columns
    sample_cols = [c for c in ['Brand', 'Name', 'Price', 'Memory.RAM', 'Display.Size', 'Display.Resolution'] if c in df.columns]
    print("\nSample Preview:")
    print(df[sample_cols].head(3))