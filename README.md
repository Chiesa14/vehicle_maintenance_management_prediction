# Electricity Consumption Predictor

## Overview
This project predicts electricity consumption based on various factors like temperature, household size, and time of day. It includes a machine learning model for predictions and interactive visualizations to analyze trends.

## Features
- **Prediction**: Predict energy consumption using a trained Random Forest model.
- **Visualizations**: Interactive charts for analyzing trends in energy usage.
- **API**: REST API for making predictions and fetching data.

## Setup

### Prerequisites
- Python 3.8+
- PostgreSQL (or any database supported by Django)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Chiesa14/vehicle_maintenance_management_prediction.git
   cd vehicle_maintenance_management_prediction
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Generate data:
   ```bash
   python generate.py
   ```

5. Train the model:
   ```bash
   python train.py
   ```

6. Set up the database:
   ```bash
   cd vmms
   python manage.py migrate
   ```
   

7. Run the server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000/`.

## Usage

### Predict Maintenance Costs
- Visit the homepage and input your vehicle details to get a maintenance cost estimate.

### Analytics Dashboard
- Navigate to the **Analytics** page to explore interactive insights:
  - Actual vs Predicted Maintenance Costs
  - Maintenance Cost Distribution
  - Feature Importance Analysis
  - Cost Breakdown by Vehicle Make and Driving Condition
  - Mileage vs Maintenance Cost Relationship
  - Vehicle Age vs Maintenance Cost Trends

### API Endpoints
- **Predict Maintenance Cost**: `POST /api/predict/`
- **Sample Vehicle Data**: `GET /api/sample-data/`
- **Feature Importance Data**: `GET /api/feature-importance/`

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
