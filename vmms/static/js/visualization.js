// static/js/visualization.js
document.addEventListener("DOMContentLoaded", function () {
    loadSampleData().then((data) => {
        renderActualVsPredicted(data);
        renderCostDistribution(data);
        renderMakeChart(data);
        renderConditionChart(data);
        renderMileageChart(data);
        renderAgeChart(data);
    });

    loadFeatureImportance().then((data) => {
        renderFeatureImportanceChart(data);
    });
});

async function loadSampleData() {
    try {
        const response = await fetch("/api/sample-data/");
        if (!response.ok) throw new Error("Failed to load sample data");
        return await response.json();
    } catch (error) {
        console.error("Error loading sample data:", error);
        return [];
    }
}

async function loadFeatureImportance() {
    try {
        const response = await fetch("/api/feature-importance/");
        if (!response.ok) throw new Error("Failed to load feature importance");
        return await response.json();
    } catch (error) {
        console.error("Error loading feature importance:", error);
        return [];
    }
}
function renderActualVsPredicted(data) {
    const ctx = document.getElementById("actual-vs-predicted-chart");
    const actual = data.map(d => d.maintenance_cost);
    const predicted = actual.map(cost => cost * (1 + (Math.random() * 0.2 - 0.1))); // Simulated predictions

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Actual vs Predicted',
                data: actual.map((a, i) => ({ x: a, y: predicted[i] })),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                pointRadius: 5
            }, {
                label: 'Perfect Prediction',
                data: [{ x: Math.min(...actual), y: Math.min(...actual) },
                      { x: Math.max(...actual), y: Math.max(...actual) }],
                type: 'line',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Actual Cost ($)' }},
                y: { title: { display: true, text: 'Predicted Cost ($)' }}
            }
        }
    });
}


function renderMakeChart(data) {
    const ctx = document.getElementById("make-chart");
    const makes = [...new Set(data.map(d => d.make))];
    const avgCosts = makes.map(make => {
        const filtered = data.filter(d => d.make === make);
        return filtered.reduce((sum, d) => sum + d.maintenance_cost, 0) / filtered.length;
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: makes,
            datasets: [{
                label: 'Average Maintenance Cost',
                data: avgCosts,
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                ]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { title: { display: true, text: 'Average Cost ($)' }}
            }
        }
    });
}

function renderConditionChart(data) {
    const ctx = document.getElementById("condition-chart");
    const conditions = ['city', 'highway', 'mixed'];
    const avgCosts = conditions.map(cond => {
        const filtered = data.filter(d => d.driving_condition === cond);
        return filtered.reduce((sum, d) => sum + d.maintenance_cost, 0) / filtered.length;
    });

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: conditions.map(c => c.charAt(0).toUpperCase() + c.slice(1)),
            datasets: [{
                label: 'Maintenance Cost by Condition',
                data: avgCosts,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function renderMileageChart(data) {
    const ctx = document.getElementById("mileage-chart");

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Mileage vs Cost',
                data: data.map(d => ({ x: d.mileage, y: d.maintenance_cost })),
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Mileage (km)' }},
                y: { title: { display: true, text: 'Maintenance Cost ($)' }}
            }
        }
    });
}

function renderAgeChart(data) {
    const ctx = document.getElementById("age-chart");
    const ages = [...new Set(data.map(d => d.vehicle_age))].sort((a, b) => a - b);
    const avgCosts = ages.map(age => {
        const filtered = data.filter(d => d.vehicle_age === age);
        return filtered.reduce((sum, d) => sum + d.maintenance_cost, 0) / filtered.length;
    });

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ages,
            datasets: [{
                label: 'Average Maintenance Cost by Vehicle Age',
                data: avgCosts,
                borderColor: '#4BC0C0',
                tension: 0.4,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Vehicle Age (years)' }},
                y: { title: { display: true, text: 'Average Cost ($)' }}
            }
        }
    });
}

function renderFeatureImportanceChart(data) {
    const ctx = document.getElementById("feature-importance-chart");
    const sortedData = data.sort((a, b) => b.importance - a.importance).slice(0, 10);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedData.map(d => d.feature),
            datasets: [{
                label: 'Feature Importance',
                data: sortedData.map(d => d.importance),
                backgroundColor: 'rgba(153, 102, 255, 0.6)'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Importance' }}
            }
        }
    });
}


// visualization.js - Update renderCostDistribution function
function renderCostDistribution(data) {
    const ctx = document.getElementById("cost-distribution-chart");
    const costs = data.map(d => d.maintenance_cost);

    // Create bins for histogram
    const binSize = 200; // $200 intervals
    const maxCost = Math.ceil(Math.max(...costs) / binSize) * binSize;
    const bins = Array.from({length: maxCost/binSize}, (_, i) => (i * binSize));

    // Count values in each bin
    const counts = bins.map((bin, index) => {
        const nextBin = bins[index + 1] || Infinity;
        return costs.filter(c => c >= bin && c < nextBin).length;
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: bins.map(bin => `$${bin}-$${bin + binSize}`),
            datasets: [{
                label: 'Maintenance Cost Distribution',
                data: counts,
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                barThickness: 20
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: { display: true, text: 'Maintenance Cost Range ($)' },
                },
                y: {
                    title: { display: true, text: 'Number of Vehicles' },
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}
