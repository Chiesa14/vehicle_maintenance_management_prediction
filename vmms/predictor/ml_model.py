# ml_model.py
import os
import joblib
import pandas as pd
from django.conf import settings


class VehicleMaintenanceManagement:
    model = None

    @classmethod
    def get_model(cls):
        """Load the model if it's not already loaded"""
        if cls.model is None:
            model_path = os.path.join(settings.BASE_DIR, 'model', 'vehicle_maintenance_model.pkl')
            cls.model = joblib.load(model_path)
        return cls.model

    @classmethod
    def predict(cls, features):
        """Make a prediction using the loaded model"""
        model = cls.get_model()

        # Create DataFrame with the input features
        df = pd.DataFrame([{
            'make': features['make'],
            'model_year': features['model_year'],
            'engine_type': features['engine_type'],
            'mileage': features['mileage'],
            'driving_condition': features['driving_condition'],
            'service_interval': features['service_interval'],
            'days_since_service': features['days_since_service'],
            'oil_level': features['oil_level'],
            'tire_pressure': features['tire_pressure'],
            'brake_wear': features['brake_wear'],
            'fault_codes': features['fault_codes']
        }])

        # Calculate vehicle_age
        df['vehicle_age'] = 2024 - df['model_year']

        # Make prediction
        prediction = model.predict(df)[0]
        return round(prediction, 2)