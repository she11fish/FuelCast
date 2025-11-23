"""Model service"""
import joblib
import pickle
import os
from typing import Optional, List, Dict
from app.config import MODEL_PATH, SARIMAX_MODEL_PATH


class ModelService:
    def __init__(self):
        self.xgboost_model = None
        self.sarimax_model = None
    
    def load_xgboost_model(self) -> bool:
        server_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        model_path = os.path.join(server_root, MODEL_PATH)
        
        try:
            self.xgboost_model = joblib.load(model_path)
            print(f"✓ Loaded XGBoost model from {model_path}")
            return True
        except Exception as e:
            print(f"✗ Failed to load XGBoost model: {e}")
            self.xgboost_model = None
            return False
    
    def load_sarimax_model(self) -> bool:
        """Load SARIMAX model from pickle file"""
        server_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        model_path = os.path.join(server_root, SARIMAX_MODEL_PATH)
        
        try:
            with open(model_path, 'rb') as f:
                self.sarimax_model = pickle.load(f)
            print(f"✓ Loaded SARIMAX model from {model_path}")
            return True
        except Exception as e:
            print(f"✗ Failed to load SARIMAX model: {e}")
            self.sarimax_model = None
            return False
    
    def predict_sarimax(self, exog_future, steps: int):
        """
        Generate SARIMAX predictions
        
        Args:
            exog_future: DataFrame or array of exogenous variables for forecast period
            steps: Number of steps to forecast
            
        Returns:
            Array of predictions or None if model not loaded
        """
        if self.sarimax_model is None:
            return None
        
        try:
            forecast = self.sarimax_model.get_forecast(steps=steps, exog=exog_future)
            predictions = forecast.predicted_mean
            return predictions
        except Exception as e:
            print(f"Error making SARIMAX predictions: {e}")
            return None
    
    def get_feature_importance(self) -> Optional[List[Dict]]:
        if self.xgboost_model is None:
            return None
        
        try:
            booster = self.xgboost_model.get_booster() if hasattr(self.xgboost_model, 'get_booster') else self.xgboost_model
            importance_dict = booster.get_score(importance_type='weight')
            
            features = [{"feature": f, "score": float(s)} for f, s in importance_dict.items()]
            
            if features:
                max_score = max(f['score'] for f in features)
                for f in features:
                    f['score'] = round(f['score'] / max_score, 3)
            
            features.sort(key=lambda x: x['score'], reverse=True)
            return features
        except Exception as e:
            print(f"Failed to extract feature importance: {e}")
            return None
    
    @staticmethod
    def get_fallback_importance() -> List[Dict]:
        return [
            {"feature": "Crude Oil Price Lag-4", "score": 0.850},
            {"feature": "Seasonal Index", "score": 0.720},
            {"feature": "Crude Oil Price Lag-1", "score": 0.680},
            {"feature": "Weekly Demand", "score": 0.620},
            {"feature": "Refinery Utilization", "score": 0.580},
            {"feature": "Inventory Levels", "score": 0.540},
            {"feature": "Dollar Index", "score": 0.480},
            {"feature": "Crude Oil Price Lag-8", "score": 0.420},
            {"feature": "Holiday Indicator", "score": 0.380},
            {"feature": "Production Volume", "score": 0.340},
            {"feature": "Temperature Anomaly", "score": 0.280},
            {"feature": "Import Volume", "score": 0.220}
        ]


model_service = ModelService()
