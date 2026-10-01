# Laptop Price Predictor

A machine learning web application that predicts laptop prices based on laptop specifications.

## Features

- Laptop price prediction
- Machine learning model comparison
- XGBoost prediction model
- Streamlit web interface
- Interactive laptop configuration

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Streamlit
- Jupyter Notebook

## Current Model

XGBoost

Current R² Score: ~88.9%

## Project Structure

- `app.py` — Streamlit application
- `laptop-price-predictor.ipynb` — ML notebook
- `laptop_data.csv` — Dataset
- `pipe.pkl` — Trained ML pipeline
- `df.pkl` — Processed dataframe
- `requirements.txt` — Python dependencies
- `.gitignore` — Files ignored by Git

## Run Locally

```bash
"C:\Program Files\Python313\python.exe" -m streamlit run app.py