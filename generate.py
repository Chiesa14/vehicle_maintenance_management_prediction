import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import OneHotEncoder

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


def generate_vehicle_maintenance_data(num_samples=5000):
    """
    Generate synthetic vehicle maintenance data with realistic patterns
    """
    current_year = 2024
    num_vehicles = 200

    # Create base vehicle characteristics
    vehicles = []
    makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Tesla']
    engine_types = ['gas', 'diesel', 'electric']
    conditions = ['city', 'highway', 'mixed']

    for _ in range(num_vehicles):
        make = random.choice(makes)
        model_year = random.randint(2010, 2023)
        engine = random.choice(engine_types)
        daily_km = random.randint(20, 100)
        condition = random.choice(conditions)
        service_interval = random.choice([90, 180, 365])
        reliability = random.uniform(0.8, 1.2)

        vehicles.append({
            'make': make,
            'model_year': model_year,
            'engine_type': engine,
            'daily_km': daily_km,
            'condition': condition,
            'service_interval': service_interval,
            'reliability': reliability
        })

    # Assign samples to vehicles
    vehicle_indices = np.random.choice(num_vehicles, num_samples)
    selected_vehicles = [vehicles[i] for i in vehicle_indices]

    # Extract base features
    make = [v['make'] for v in selected_vehicles]
    model_year = np.array([v['model_year'] for v in selected_vehicles])
    engine_type = [v['engine_type'] for v in selected_vehicles]
    daily_km = np.array([v['daily_km'] for v in selected_vehicles])
    condition = [v['condition'] for v in selected_vehicles]
    service_interval = np.array([v['service_interval'] for v in selected_vehicles])
    reliability = np.array([v['reliability'] for v in selected_vehicles])

    # Calculate derived features
    vehicle_age = current_year - model_year
    mileage = daily_km * 365 * vehicle_age + np.random.normal(0, 1000, num_samples)
    mileage = np.abs(np.round(mileage, 1))

    days_since_service = np.random.randint(0, service_interval, num_samples)

    # Oil level calculation
    oil_level = []
    for i in range(num_samples):
        if engine_type[i] == 'electric':
            oil_level.append('N/A')
        else:
            if days_since_service[i] > service_interval[i] * 0.75:
                oil_level.append('Low')
            elif days_since_service[i] > service_interval[i] * 0.5:
                oil_level.append('Medium')
            else:
                oil_level.append('High')

    # Tire pressure with some outliers
    tire_pressure = np.round(np.clip(np.random.normal(33, 3, num_samples), 25, 40), 1)

    # Brake wear calculation
    brake_wear = (mileage / 50000) * 100
    for i in range(num_samples):
        if condition[i] == 'city':
            brake_wear[i] *= 1.3
        elif condition[i] == 'highway':
            brake_wear[i] *= 0.7
    brake_wear = np.clip(brake_wear + np.random.normal(0, 5, num_samples), 0, 100)
    brake_wear = np.round(brake_wear, 1)

    # Fault codes simulation
    fault_codes = np.random.poisson((vehicle_age / 10) * (1 / reliability), num_samples)

    # Maintenance cost calculation
    base_cost = np.random.normal(150, 30, num_samples)
    cost = base_cost.copy()

    for i in range(num_samples):
        # Oil change impact
        if oil_level[i] == 'Low':
            cost[i] += 80
        elif oil_level[i] == 'Medium':
            cost[i] += 40

        # Brake repairs
        if brake_wear[i] > 80:
            cost[i] += 300
        elif brake_wear[i] > 60:
            cost[i] += 150

        # Engine type adjustments
        if engine_type[i] == 'diesel':
            cost[i] *= 1.25
        elif engine_type[i] == 'electric':
            cost[i] *= 0.85

        # Fault code costs
        cost[i] += fault_codes[i] * 75

        # Reliability factor
        cost[i] *= (2 - reliability[i])

        # Random variance
        cost[i] += np.random.normal(0, 50)

    maintenance_cost = np.clip(np.round(cost, 2), 50, 2000)

    # Create DataFrame
    data = pd.DataFrame({
        'make': make,
        'model_year': model_year,
        'engine_type': engine_type,
        'vehicle_age': vehicle_age,
        'mileage': mileage,
        'driving_condition': condition,
        'service_interval': service_interval,
        'days_since_service': days_since_service,
        'oil_level': oil_level,
        'tire_pressure': tire_pressure,
        'brake_wear': brake_wear,
        'fault_codes': fault_codes,
        'maintenance_cost': maintenance_cost
    })

    return data


# Generate the data
data = generate_vehicle_maintenance_data(5000)

# Display basic statistics
print("Generated dataset with", len(data), "rows")
print("\nBasic statistics:")
print(data.describe())

print("\nAverage maintenance cost by manufacturer:")
print(data.groupby('make')['maintenance_cost'].mean().sort_values(ascending=False))

print("\nAverage maintenance cost by engine type:")
print(data.groupby('engine_type')['maintenance_cost'].mean().sort_values(ascending=False))

print("\nAverage maintenance cost by driving condition:")
print(data.groupby('driving_condition')['maintenance_cost'].mean().sort_values(ascending=False))

# Save the data to a CSV file
data.to_csv('vehicle_maintenance_data.csv', index=False)
print("\nData saved to 'vehicle_maintenance_data.csv'")