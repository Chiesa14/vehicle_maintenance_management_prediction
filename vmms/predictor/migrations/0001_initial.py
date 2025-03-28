# Generated by Django 5.1.7 on 2025-03-28 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Prediction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("make", models.CharField(max_length=20)),
                ("model_year", models.IntegerField()),
                ("engine_type", models.CharField(max_length=10)),
                ("mileage", models.FloatField()),
                ("driving_condition", models.CharField(max_length=10)),
                ("service_interval", models.IntegerField()),
                ("days_since_service", models.IntegerField()),
                ("oil_level", models.CharField(max_length=10)),
                ("tire_pressure", models.FloatField()),
                ("brake_wear", models.FloatField()),
                ("fault_codes", models.IntegerField()),
                ("predicted_cost", models.FloatField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
