# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('visualization/', views.visualization, name='visualization'),
    path('api/predict/', views.PredictMaintenance.as_view(), name='predict'),  # Updated view
    path('api/sample-data/', views.get_sample_data, name='sample-data'),
    path('api/feature-importance/', views.feature_importance, name='feature-importance'),
]