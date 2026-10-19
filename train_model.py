import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor

data_path = os.path.join("data", "cleaned_laptops_2026.csv")
print("Loading cleaned dataset...")
df = pd.read_csv(data_path)

# Prepare features and target
X = df.drop(columns=['Price'])
y = np.log(df['Price'])

# 85% train, 15% test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

# OneHotEncode categorical columns: Company (0), TypeName (1), Cpu_brand (7), Gpu_Brand (10), os (11)
step1 = ColumnTransformer(transformers=[
    ('col_tnf', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), [0, 1, 7, 10, 11])
], remainder='passthrough')

# XGBoost model
step2 = XGBRegressor(n_estimators=120, max_depth=6, learning_rate=0.15, random_state=42)

pipe = Pipeline([
    ('step1', step1),
    ('step2', step2)
])

print("Training XGBoost model on new data...")
pipe.fit(X_train, y_train)

y_pred = pipe.predict(X_test)
print(f"\nR2 Score: {r2_score(y_test, y_pred):.4f}")
print(f"MAE (log scale): {mean_absolute_error(y_test, y_pred):.4f}")

# Export updated artifacts
pickle.dump(df, open('df.pkl', 'wb'))
pickle.dump(pipe, open('pipe.pkl', 'wb'))
print("\nUpdated 'pipe.pkl' and 'df.pkl' successfully!")