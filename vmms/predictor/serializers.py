# serializers.py
from rest_framework import serializers
from .models import Prediction

class PredictionInputSerializer(serializers.Serializer):
    make = serializers.ChoiceField(choices=['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Tesla'])
    model_year = serializers.IntegerField(min_value=2010, max_value=2024)
    engine_type = serializers.ChoiceField(choices=['gas', 'diesel', 'electric'])
    mileage = serializers.FloatField(min_value=0)
    driving_condition = serializers.ChoiceField(choices=['city', 'highway', 'mixed'])
    service_interval = serializers.IntegerField(min_value=90, max_value=365)
    days_since_service = serializers.IntegerField(min_value=0)
    oil_level = serializers.ChoiceField(choices=['Low', 'Medium', 'High', 'N/A'])
    tire_pressure = serializers.FloatField(min_value=25, max_value=40)
    brake_wear = serializers.FloatField(min_value=0, max_value=100)
    fault_codes = serializers.IntegerField(min_value=0)

class PredictionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'