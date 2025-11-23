"""Configuration settings"""
import dotenv
dotenv.load_dotenv()

API_TITLE = "FuelCast API"
API_DESCRIPTION = "AI-powered gasoline price forecasting using SARIMA and XGBoost models"
API_VERSION = "1.0.0"

CORS_ORIGINS = ["http://localhost:3000"]

MODEL_PATH = "xgboost_gas_model.joblib"
SARIMAX_MODEL_PATH = "sarimax_gas_model.pkl"

HISTORICAL_WEEKS = 52
FORECAST_WEEKS = 12
BASE_PRICE = 3.20
RANDOM_SEED = 42

TREND_RANGE = (0, 0.4)
SEASONALITY_AMPLITUDE = 0.15
NOISE_STD = 0.05
SARIMA_NOISE_STD = 0.03
XGBOOST_NOISE_STD = 0.02
FORECAST_NOISE_STD_SARIMA = 0.04
FORECAST_NOISE_STD_XGBOOST = 0.03
