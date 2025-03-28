// predictor.js
document.addEventListener("DOMContentLoaded", function () {
    // Initialize form with sample values
    document.getElementById("model_year").value = 2020;
    document.getElementById("mileage").value = 45000;
    document.getElementById("service_interval").value = 180;
    document.getElementById("days_since_service").value = 60;
    document.getElementById("tire_pressure").value = 33.5;
    document.getElementById("brake_wear").value = 35;
    document.getElementById("fault_codes").value = 2;

    const form = document.getElementById("prediction-form");
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        submitPredictionForm();
    });
});

async function submitPredictionForm() {
    const form = document.getElementById("prediction-form");
    const resultDiv = document.getElementById("prediction-result");

    resultDiv.innerHTML = '<div class="text-center"><div class="spinner-border text-dark" role="status"></div></div>';

    const formData = {
        make: document.getElementById("make").value,
        model_year: parseInt(document.getElementById("model_year").value),
        engine_type: document.getElementById("engine_type").value,
        mileage: parseFloat(document.getElementById("mileage").value),
        driving_condition: document.getElementById("driving_condition").value,
        service_interval: parseInt(document.getElementById("service_interval").value),
        days_since_service: parseInt(document.getElementById("days_since_service").value),
        oil_level: document.getElementById("oil_level").value,
        tire_pressure: parseFloat(document.getElementById("tire_pressure").value),
        brake_wear: parseFloat(document.getElementById("brake_wear").value),
        fault_codes: parseInt(document.getElementById("fault_codes").value)
    };

    try {
        const response = await fetch("/api/predict/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();

        resultDiv.innerHTML = `
            <div class="text-center">
                <h4 class="mb-3">Estimated Maintenance Cost</h4>
                <div class="prediction-cost">$${data.predicted_cost}</div>
                <div class="cost-category mt-2">${getCostCategory(data.predicted_cost)}</div>
                <div class="factors-list mt-4">
                    <h5>Key Factors:</h5>
                    <ul class="list-unstyled">
                        <li>${formData.make} Vehicle</li>
                        <li>${formData.mileage.toLocaleString()} km Mileage</li>
                        <li>${formData.brake_wear}% Brake Wear</li>
                        <li>${formData.fault_codes} Fault Codes</li>
                    </ul>
                </div>
            </div>
        `;

        updatePredictionChart(data.predicted_cost);
    } catch (error) {
        console.error("Error:", error);
        resultDiv.innerHTML = `
            <div class="alert alert-danger">
                Error generating estimate. Please try again.
            </div>
        `;
    }
}

function getCostCategory(cost) {
    if (cost > 1000) return "High Priority Maintenance";
    if (cost > 500) return "Moderate Maintenance Needed";
    return "Routine Maintenance";
}

function updatePredictionChart(predictedValue) {
    const ctx = document.getElementById("prediction-chart");
    if (window.predictionChart) window.predictionChart.destroy();

    const referenceData = { low: 300, average: 700, high: 1500 };

    window.predictionChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Routine", "Average", "Major", "Your Estimate"],
            datasets: [{
                label: "Maintenance Cost ($)",
                data: [referenceData.low, referenceData.average, referenceData.high, predictedValue],
                backgroundColor: ["#4CAF50", "#FFC107", "#F44336", "#2196F3"],
                borderColor: ["#388E3C", "#FFA000", "#D32F2F", "#1976D2"],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true } },
            plugins: { legend: { display: false } }
        }
    });
}
// Helper function to get CSRF token for Django
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
