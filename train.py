import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# Create directories
os.makedirs('vmms/model', exist_ok=True)
os.makedirs('vmms/visualizations', exist_ok=True)

# Load data
data = pd.read_csv('vehicle_maintenance_data.csv')

# Data preview
print("Dataset preview:")
print(data.head())

# Correlation matrix
numeric_cols = ['model_year', 'vehicle_age', 'mileage', 'service_interval',
                'days_since_service', 'tire_pressure', 'brake_wear',
                'fault_codes', 'maintenance_cost']
corr = data[numeric_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Feature Correlation Matrix')
plt.tight_layout()
plt.savefig('vmms/visualizations/correlation_matrix.png')
plt.close()

# Prepare data for modeling
X = data.drop('maintenance_cost', axis=1)
y = data['maintenance_cost']

# Define features
categorical_features = ['make', 'engine_type', 'driving_condition', 'oil_level']
numerical_features = ['model_year', 'vehicle_age', 'mileage', 'service_interval',
                      'days_since_service', 'tire_pressure', 'brake_wear', 'fault_codes']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

# Hyperparameter grid
param_grid = {
    'regressor__n_estimators': [50, 100, 200],
    'regressor__max_depth': [None, 10, 20, 30],
    'regressor__min_samples_split': [2, 5, 10],
}

# Quick grid for demonstration
quick_param_grid = {
    'regressor__n_estimators': [100],
    'regressor__max_depth': [20],
    'regressor__min_samples_split': [5],
}

# Grid search
print("Starting hyperparameter tuning...")
grid_search = GridSearchCV(model, param_grid=quick_param_grid, cv=3,
                           n_jobs=-1, verbose=1, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
print("Best parameters:", grid_search.best_params_)

# Evaluation
y_pred = best_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"\nModel Evaluation on Test Set:")
print(f"Mean Absolute Error: ${mae:.2f}")
print(f"Root Mean Squared Error: ${rmse:.2f}")
print(f"R-squared: {r2:.4f}")

# Actual vs Predicted plot
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual Maintenance Cost')
plt.ylabel('Predicted Maintenance Cost')
plt.title('Actual vs Predicted Maintenance Costs')
plt.tight_layout()
plt.savefig('vmms/visualizations/actual_vs_predicted.png')
plt.close()

# Feature importance
feature_names = numerical_features + list(best_model.named_steps['preprocessor']
                                          .named_transformers_['cat']
                                          .get_feature_names_out(categorical_features))

importances = best_model.named_steps['regressor'].feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(12, 8))
plt.title('Feature Importance')
plt.bar(range(len(importances)), importances[indices], align='center')
plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
plt.tight_layout()
plt.savefig('vmms/visualizations/feature_importance.png')
plt.close()

# Feature relationships
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

sns.scatterplot(x='mileage', y='maintenance_cost', data=data, ax=axs[0, 0], alpha=0.3)
axs[0, 0].set_title('Mileage vs Maintenance Cost')

sns.boxplot(x='driving_condition', y='maintenance_cost', data=data, ax=axs[0, 1])
axs[0, 1].set_title('Driving Condition vs Maintenance Cost')

sns.boxplot(x='oil_level', y='maintenance_cost', data=data, ax=axs[1, 0])
axs[1, 0].set_title('Oil Level vs Maintenance Cost')

sns.scatterplot(x='brake_wear', y='maintenance_cost', data=data, ax=axs[1, 1], alpha=0.3)
axs[1, 1].set_title('Brake Wear vs Maintenance Cost')

plt.tight_layout()
plt.savefig('vmms/visualizations/feature_relationships.png')
plt.close()

# Save model
joblib.dump(best_model, 'vmms/model/vehicle_maintenance_model.pkl')
print("\nModel saved to 'vmms/model/vehicle_maintenance_model.pkl'")


# Prediction function
def predict_maintenance(make, model_year, engine_type, mileage,
                        driving_condition, service_interval, days_since_service,
                        oil_level, tire_pressure, brake_wear, fault_codes):
    """Function to generate predictions for API use"""
    data = pd.DataFrame({
        'make': [make],
        'model_year': [model_year],
        'engine_type': [engine_type],
        'mileage': [mileage],
        'driving_condition': [driving_condition],
        'service_interval': [service_interval],
        'days_since_service': [days_since_service],
        'oil_level': [oil_level],
        'tire_pressure': [tire_pressure],
        'brake_wear': [brake_wear],
        'fault_codes': [fault_codes]
    })

    # Calculate vehicle_age
    data['vehicle_age'] = 2024 - data['model_year']

    prediction = best_model.predict(data)[0]
    return round(prediction, 2)


# Save sample data for visualization
sample_data = data.sample(1000)
sample_data.to_csv('vmms/visualizations/sample_data.csv', index=False)

print("\nTraining and evaluation complete!")