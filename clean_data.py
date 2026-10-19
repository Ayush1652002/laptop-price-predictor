import pandas as pd
import numpy as np
import re
import os

raw_path = os.path.join("data", "laptops.csv")
out_path = os.path.join("data", "cleaned_laptops_2026.csv")

print("Loading raw dataset...")
raw_df = pd.read_csv(raw_path, low_memory=False)

df = pd.DataFrame()
df['Company'] = raw_df['Brand'].fillna('Other')
df['Price'] = pd.to_numeric(raw_df['Price'], errors='coerce')

# Drop rows missing price
df = df.dropna(subset=['Price'])

# 1. Clean RAM
def extract_ram(val):
    if pd.isna(val): return 8
    match = re.search(r'(\d+)\s*GB', str(val), re.IGNORECASE)
    return int(match.group(1)) if match else 8

df['Ram'] = raw_df['Memory.RAM'].apply(extract_ram)

# 2. Clean Storage (SSD / HDD)
def extract_ssd(val):
    if pd.isna(val): return 512
    val = str(val).upper()
    if 'TB' in val:
        match = re.search(r'(\d+)\s*TB', val)
        return int(match.group(1)) * 1024 if match else 1024
    match = re.search(r'(\d+)\s*GB', val)
    return int(match.group(1)) if match else 512

df['SSD'] = raw_df['Memory.Solid State Drive'].apply(extract_ssd)
df['HDD'] = 0

# 3. Calculate PPI
def extract_inches(val):
    match = re.search(r'(\d+(\.\d+)?)', str(val))
    return float(match.group(1)) if match else 15.6

def extract_resolution(val):
    match = re.search(r'(\d+)\s*x\s*(\d+)', str(val))
    if match:
        return int(match.group(1)), int(match.group(2))
    return 1920, 1080

inches = raw_df['Display.Size'].apply(extract_inches)
res = raw_df['Display.Resolution'].apply(extract_resolution)
x_res = res.apply(lambda r: r[0])
y_res = res.apply(lambda r: r[1])

df['PPI'] = np.sqrt(x_res**2 + y_res**2) / inches
df['Touchscreen'] = raw_df['Display.Touch'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
df['Ips'] = raw_df['Display.Type'].apply(lambda x: 1 if 'ips' in str(x).lower() else 0)

# 4. Clean CPU
def categorize_cpu(val):
    val = str(val).lower()
    if 'core ultra' in val or 'ultra' in val:
        return 'Intel Core Ultra'
    elif 'i7' in val or 'core 7' in val:
        return 'Intel Core i7'
    elif 'i5' in val or 'core 5' in val:
        return 'Intel Core i5'
    elif 'i3' in val or 'core 3' in val:
        return 'Intel Core i3'
    elif 'ryzen 7' in val:
        return 'AMD Ryzen 7'
    elif 'ryzen 5' in val:
        return 'AMD Ryzen 5'
    elif any(k in val for k in ['apple', 'm1', 'm2', 'm3', 'm4', 'm5']):
        return 'Apple Silicon'
    elif 'snapdragon' in val:
        return 'Snapdragon X'
    else:
        return 'Other'

df['Cpu_brand'] = raw_df['Processor.Processor'].apply(categorize_cpu)

# 5. Clean GPU
def categorize_gpu(val):
    val = str(val).lower()
    if any(k in val for k in ['nvidia', 'geforce', 'rtx']):
        return 'Nvidia'
    elif any(k in val for k in ['amd', 'radeon']):
        return 'AMD'
    elif 'apple' in val:
        return 'Apple'
    else:
        return 'Intel'

df['Gpu_Brand'] = raw_df['Graphics.GPU'].apply(categorize_gpu)

# 6. Clean OS & Defaults
def categorize_os(val):
    val = str(val).lower()
    if 'win' in val: return 'Windows'
    elif 'mac' in val: return 'Mac'
    elif any(k in val for k in ['linux', 'ubuntu']): return 'Linux'
    else: return 'Others'

df['os'] = raw_df['General.OS'].apply(categorize_os)
df['Weight'] = 1.8
df['TypeName'] = 'Notebook'

# Reorder columns to match your model
final_cols = ['Company', 'TypeName', 'Ram', 'Weight', 'Touchscreen', 'Ips', 'PPI', 'Cpu_brand', 'HDD', 'SSD', 'Gpu_Brand', 'os', 'Price']
df = df[final_cols]

df.to_csv(out_path, index=False)
print(f"Data cleaned successfully! Saved to {out_path}")
print(f"Final shape: {df.shape}")