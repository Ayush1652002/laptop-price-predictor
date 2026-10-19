import pickle
import numpy as np
import pandas as pd

# Load the newly trained pipeline
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Sample test query: Modern Dell Laptop with Intel Core Ultra & RTX GPU
test_laptop = pd.DataFrame([[
    'Dell',                  # Company
    'Notebook',              # TypeName
    16,                      # Ram (GB)
    1.6,                     # Weight (kg)
    0,                       # Touchscreen (0 or 1)
    1,                       # Ips (0 or 1)
    141.2,                   # PPI (1920x1080 on 15.6")
    'Intel Core Ultra',      # Cpu_brand
    0,                       # HDD (GB)
    512,                     # SSD (GB)
    'Nvidia',                # Gpu_Brand
    'Windows'                # os
]], columns=[
    'Company', 'TypeName', 'Ram', 'Weight', 'Touchscreen', 
    'Ips', 'PPI', 'Cpu_brand', 'HDD', 'SSD', 'Gpu_Brand', 'os'
])

predicted_log_price = pipe.predict(test_laptop)[0]
final_price = int(np.exp(predicted_log_price))

print("\n--- Model Test Prediction ---")
print(f"Predicted Price: ₹{final_price:,}")