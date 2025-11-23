"""Utilities"""
import pandas as pd
import numpy as np
from typing import List, Dict


def calculate_rmse(actual: pd.Series, predicted: pd.Series) -> float:
    errors = actual - predicted
    return float(np.sqrt(np.mean(errors ** 2)))


def dataframe_to_forecast_list(df: pd.DataFrame) -> List[Dict]:
    result = []
    for _, row in df.iterrows():
        result.append({
            "date": row['date'],
            "actual": None if pd.isna(row['actual']) else round(float(row['actual']), 2),
            "sarima": None if pd.isna(row['sarima']) else round(float(row['sarima']), 2),
            "xgboost": None if pd.isna(row['xgboost']) else round(float(row['xgboost']), 2)
        })
    return result
