# models.py
from django.db import models

class Prediction(models.Model):
    make = models.CharField(max_length=20)
    model_year = models.IntegerField()
    engine_type = models.CharField(max_length=10)
    mileage = models.FloatField()
    driving_condition = models.CharField(max_length=10)
    service_interval = models.IntegerField()
    days_since_service = models.IntegerField()
    oil_level = models.CharField(max_length=10)
    tire_pressure = models.FloatField()
    brake_wear = models.FloatField()
    fault_codes = models.IntegerField()
    predicted_cost = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id}: ${self.predicted_cost} on {self.timestamp}"