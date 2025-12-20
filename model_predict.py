# model_predict.py
import sys
import os
import pandas as pd
import numpy as np
import joblib

# Load model dynamically for PyInstaller frozen executable
if getattr(sys, 'frozen', False):
    # Running as .exe
    base_path = sys._MEIPASS
else:
    # Running as normal script
    base_path = os.path.dirname(__file__)

model_path = os.path.join(base_path, "model", "random_forest_model.pkl")
rf_model = joblib.load(model_path)

def preprocess_input(data):
    # Log-transform numeric columns
    for col in ['total_rooms', 'total_bedrooms', 'population', 'households']:
        data[col] = np.log(data[col] + 1)

    # Feature engineering
    data['rooms_per_household'] = data['total_rooms'] / data['households']
    data['bedrooms_per_room'] = data['total_bedrooms'] / data['total_rooms']
    data['population_per_household'] = data['population'] / data['households']

    # One-hot encode ocean_proximity
    ocean_cols = ['INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN']
    for col in ocean_cols:
        data[col] = (data['ocean_proximity'] == col).astype(int)

    # Drop original column
    data = data.drop('ocean_proximity', axis=1)

    # Ensure columns are in the same order as during training
    final_order = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms',
                   'population', 'households', 'median_income', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN',
                   'rooms_per_household', 'bedrooms_per_room', 'population_per_household']

    data = data[final_order]
    return data

def predict_house_value(input_data):
    """
    input_data: pandas DataFrame with raw input
    returns: prediction as float
    """
    input_df = preprocess_input(input_data)
    prediction = rf_model.predict(input_df)[0]
    return prediction
