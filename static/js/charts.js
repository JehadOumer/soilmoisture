document.addEventListener('DOMContentLoaded', function() {
    initializeDateInputs();
    fetchCurrentReading();
    fetchTodayData();
    fetchLast7DaysData();
});

function initializeDateInputs() {
    fetch('/data/available_dates')
        .then(response => response.json())
        .then(dates => {
            const startDateInput = document.getElementById('startDate');
            const endDateInput = document.getElementById('endDate');
            startDateInput.min = dates.min;
            startDateInput.max = dates.max;
            endDateInput.min = dates.min;
            endDateInput.max = dates.max;
        })
        .catch(error => console.error('Error loading available dates:', error));
}

function setMinMaxDates() {
    fetch('/data/available_dates')
        .then(response => response.json())
        .then(dates => {
            const startDateInput = document.getElementById('startDate');
            const endDateInput = document.getElementById('endDate');
            startDateInput.min = dates.min;
            startDateInput.max = dates.max;
            endDateInput.min = dates.min;
            endDateInput.max = dates.max;
        })
        .catch(error => console.error('Error loading available dates:', error));
}

function fetchCurrentReading() {
    fetch('/data/current')
        .then(response => response.json())
        .then(data => updateCurrentReading(data))
        .catch(error => console.error('Error loading current data:', error));
}

function updateCurrentReading(data) {
    const currentDate = new Date(data.year, data.month - 1, data.day, data.hour, data.minute, data.second);
    const formattedDate = currentDate.toLocaleString();
    const categoryClass = getCategoryClass(data.category);
    document.getElementById('currentValue').innerHTML = `
        <strong>Latest Reading:</strong> Date: ${formattedDate}, Category: <span class="${categoryClass}">${data.category}</span>, Value: ${data.sensor_value.toFixed(2)}
        <div class="small">Latest value is updated after each time the sensor takes a reading. Check parameters for more information about sampling scheduling.</div>
    `;
}

function getCategoryClass(category) {
    switch (category) {
        case 'Very Dry': return 'text-danger';
        case 'Dry': return 'text-warning';
        case 'Humid': return 'text-success';
        default: return 'text-muted';
    }
}

function fetchTodayData() {
    fetch('/data/today')
        .then(response => response.json())
        .then(data => plotTodayData(data))
        .catch(error => console.error('Error loading today\'s data:', error));
}

function plotTodayData(data) {
    const ctx = document.getElementById('todayPlot').getContext('2d');
    if (window.todayChart) window.todayChart.destroy();
    window.todayChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(reading => `${reading.hour}:${reading.minute}:${reading.second}`),
            datasets: [{
                label: 'Sensor Value Today',
                data: data.map(reading => reading.sensor_value),
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: chartOptions('Time', 'Humidity Level')
    });
}

function fetchLast7DaysData() {
    fetch('/data/last7days')
        .then(response => response.json())
        .then(data => plotLast7DaysData(data))
        .catch(error => console.error('Error loading last 7 days data:', error));
}

function plotLast7DaysData(data) {
    const ctx = document.getElementById('last7DaysPlot').getContext('2d');
    if (window.last7DaysChart) window.last7DaysChart.destroy();
    window.last7DaysChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(reading => `${reading.year}-${reading.month}-${reading.day}`),
            datasets: [{
                label: 'Sensor Values Last 7 Days',
                data: data.map(reading => reading.sensor_value),
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: chartOptions('Date', 'Humidity Level')
    });
}

function fetchCustomRangeData() {
    // Modify this to ensure consistent settings
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    fetch('/data/custom_range', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({start: startDate, end: endDate})
    })
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('customPlot').getContext('2d');
        if (window.customChart) window.customChart.destroy();
        window.customChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => `${d.year}-${d.month}-${d.day}`),
                datasets: [{
                    label: 'Custom Range Values',
                    data: data.map(d => d.sensor_value),
                    borderColor: 'rgba(102, 153, 255, 1)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: chartOptions('Date', 'Humidity Level')
        });
    })
    .catch(error => console.error('Error loading custom range data:', error));
}

function chartOptions(xLabel, yLabel) {
    // Maintain consistency in how charts are displayed
    return {
        scales: {
            y: {
                suggestedMin: 0,
                suggestedMax: 1,
                title: {
                    display: true,
                    text: yLabel
                }
            },
            x: {
                title: {
                    display: true,
                    text: xLabel
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    };
}