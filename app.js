// App state
let flightCount = 0;
let flights = [];

// Initialize app when DOM loads
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set default departure date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('departure-date').value = today;
    
    // Add first flight form
    addFlightForm();
    
    // Event listeners
    document.getElementById('add-flight-btn').addEventListener('click', addFlightForm);
    document.getElementById('calculate-btn').addEventListener('click', calculateTravelTimes);
}

function addFlightForm() {
    flightCount++;
    
    const flightsContainer = document.getElementById('flights-container');
    const flightDiv = document.createElement('div');
    flightDiv.className = 'flight-form fade-in';
    flightDiv.id = `flight-${flightCount}`;
    
    flightDiv.innerHTML = `
        <div class="flight-header">
            <h3 class="flight-title">
                <i class="fas fa-plane"></i>
                Flight ${flightCount}
            </h3>
            ${flightCount > 1 ? `<button type="button" class="remove-flight-btn" onclick="removeFlightForm(${flightCount})">
                <i class="fas fa-trash"></i> Remove
            </button>` : ''}
        </div>
        
        <div class="flight-grid">
            <div class="form-group">
                <label for="departure-city-${flightCount}">Departure City</label>
                <input type="text" id="departure-city-${flightCount}" name="departure-city" 
                       placeholder="e.g., New York" required>
            </div>
            
            <div class="form-group">
                <label for="departure-time-${flightCount}">Departure Time</label>
                <input type="time" id="departure-time-${flightCount}" name="departure-time" required>
            </div>
            
            <div class="form-group">
                <label for="departure-timezone-${flightCount}">Departure Timezone (UTC Offset)</label>
                <select id="departure-timezone-${flightCount}" name="departure-timezone" class="timezone-input" required>
                    ${generateTimezoneOptions()}
                </select>
            </div>
            
            <div class="form-group">
                <label for="arrival-city-${flightCount}">Arrival City</label>
                <input type="text" id="arrival-city-${flightCount}" name="arrival-city" 
                       placeholder="e.g., London" required>
            </div>
            
            <div class="form-group">
                <label for="arrival-time-${flightCount}">Arrival Time</label>
                <input type="time" id="arrival-time-${flightCount}" name="arrival-time" required>
            </div>
            
            <div class="form-group">
                <label for="arrival-timezone-${flightCount}">Arrival Timezone (UTC Offset)</label>
                <select id="arrival-timezone-${flightCount}" name="arrival-timezone" class="timezone-input" required>
                    ${generateTimezoneOptions()}
                </select>
            </div>
        </div>
    `;
    
    flightsContainer.appendChild(flightDiv);
    
    // Set default timezone values
    document.getElementById(`departure-timezone-${flightCount}`).value = '0';
    document.getElementById(`arrival-timezone-${flightCount}`).value = '0';
}

function removeFlightForm(flightId) {
    const flightDiv = document.getElementById(`flight-${flightId}`);
    if (flightDiv) {
        flightDiv.remove();
        updateFlightNumbers();
    }
}

function updateFlightNumbers() {
    const flightForms = document.querySelectorAll('.flight-form');
    flightForms.forEach((form, index) => {
        const newNumber = index + 1;
        const title = form.querySelector('.flight-title');
        title.innerHTML = `<i class="fas fa-plane"></i> Flight ${newNumber}`;
    });
}

function generateTimezoneOptions() {
    const timezones = [
        { value: -12, label: 'UTC-12:00 (Baker Island)' },
        { value: -11, label: 'UTC-11:00 (American Samoa)' },
        { value: -10, label: 'UTC-10:00 (Hawaii)' },
        { value: -9, label: 'UTC-09:00 (Alaska)' },
        { value: -8, label: 'UTC-08:00 (Pacific Time)' },
        { value: -7, label: 'UTC-07:00 (Mountain Time)' },
        { value: -6, label: 'UTC-06:00 (Central Time)' },
        { value: -5, label: 'UTC-05:00 (Eastern Time)' },
        { value: -4, label: 'UTC-04:00 (Atlantic Time)' },
        { value: -3, label: 'UTC-03:00 (Argentina)' },
        { value: -2, label: 'UTC-02:00 (Mid-Atlantic)' },
        { value: -1, label: 'UTC-01:00 (Azores)' },
        { value: 0, label: 'UTC+00:00 (Greenwich Mean Time)' },
        { value: 1, label: 'UTC+01:00 (Central European Time)' },
        { value: 2, label: 'UTC+02:00 (Eastern European Time)' },
        { value: 3, label: 'UTC+03:00 (Moscow Time)' },
        { value: 4, label: 'UTC+04:00 (Gulf Time)' },
        { value: 5, label: 'UTC+05:00 (Pakistan Time)' },
        { value: 5.5, label: 'UTC+05:30 (India Standard Time)' },
        { value: 6, label: 'UTC+06:00 (Bangladesh Time)' },
        { value: 7, label: 'UTC+07:00 (Indochina Time)' },
        { value: 8, label: 'UTC+08:00 (China Standard Time)' },
        { value: 9, label: 'UTC+09:00 (Japan Standard Time)' },
        { value: 9.5, label: 'UTC+09:30 (Australian Central Time)' },
        { value: 10, label: 'UTC+10:00 (Australian Eastern Time)' },
        { value: 11, label: 'UTC+11:00 (Solomon Islands)' },
        { value: 12, label: 'UTC+12:00 (New Zealand)' }
    ];
    
    return timezones.map(tz => 
        `<option value="${tz.value}">${tz.label}</option>`
    ).join('');
}

function validateFlightData() {
    const flightForms = document.querySelectorAll('.flight-form');
    const errors = [];
    
    if (flightForms.length === 0) {
        errors.push('Please add at least one flight.');
        return errors;
    }
    
    flightForms.forEach((form, index) => {
        const flightNumber = index + 1;
        const formData = getFlightFormData(form);
        
        // Check required fields
        if (!formData.departureCity.trim()) {
            errors.push(`Flight ${flightNumber}: Please enter departure city.`);
        }
        if (!formData.departureTime) {
            errors.push(`Flight ${flightNumber}: Please enter departure time.`);
        }
        if (!formData.arrivalCity.trim()) {
            errors.push(`Flight ${flightNumber}: Please enter arrival city.`);
        }
        if (!formData.arrivalTime) {
            errors.push(`Flight ${flightNumber}: Please enter arrival time.`);
        }
    });
    
    const departureDate = document.getElementById('departure-date').value;
    if (!departureDate) {
        errors.push('Please select a departure date.');
    }
    
    return errors;
}

function getFlightFormData(form) {
    const inputs = form.querySelectorAll('input, select');
    const data = {};
    
    inputs.forEach(input => {
        const name = input.name || input.id.split('-').slice(0, -1).join('-');
        data[name.replace(/-([a-z])/g, (g) => g[1].toUpperCase())] = input.value;
    });
    
    return data;
}

function collectFlightData() {
    const flightForms = document.querySelectorAll('.flight-form');
    const flights = [];
    
    flightForms.forEach(form => {
        const data = getFlightFormData(form);
        
        const flight = new Flight(
            data.departureCity,
            data.departureTime,
            parseFloat(data.departureTimezone),
            data.arrivalCity,
            data.arrivalTime,
            parseFloat(data.arrivalTimezone)
        );
        
        flights.push(flight);
    });
    
    return flights;
}

function calculateTravelTimes() {
    // Clear previous errors
    clearErrorMessages();
    
    // Validate input
    const errors = validateFlightData();
    if (errors.length > 0) {
        showErrorMessages(errors);
        return;
    }
    
    try {
        // Show loading state
        setLoadingState(true);
        
        // Collect flight data
        const flights = collectFlightData();
        const departureDate = document.getElementById('departure-date').value;
        
        // Create calculator and calculate times
        const calculator = new TravelTimeCalculator(flights, departureDate);
        
        // Get results
        const totalAirTime = calculator.getTotalAirTime();
        const totalTravelTime = calculator.getTotalTravelTime();
        const totalLayoverTime = calculator.getTotalLayoverTime();
        const individualLayovers = calculator.getIndividualLayoverTimes();
        
        // Display results
        displayResults(totalAirTime, totalTravelTime, totalLayoverTime, individualLayovers);
        
        // Show success message
        showSuccessMessage('Travel times calculated successfully!');
        
    } catch (error) {
        console.error('Calculation error:', error);
        showErrorMessages([`Calculation error: ${error.message}`]);
    } finally {
        setLoadingState(false);
    }
}

function displayResults(totalAirTime, totalTravelTime, totalLayoverTime, individualLayovers) {
    // Update result values
    document.getElementById('total-air-time').textContent = totalAirTime;
    document.getElementById('total-travel-time').textContent = totalTravelTime;
    document.getElementById('total-layover-time').textContent = totalLayoverTime;
    
    // Display individual layovers
    const layoversContainer = document.getElementById('individual-layovers');
    
    if (individualLayovers.length > 0) {
        layoversContainer.innerHTML = individualLayovers.map((layover, index) => 
            `<div class="layover-item">Layover ${index + 1}: ${layover}</div>`
        ).join('');
        document.getElementById('layover-details').style.display = 'block';
    } else {
        document.getElementById('layover-details').style.display = 'none';
    }
    
    // Show results section
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function setLoadingState(isLoading) {
    const calculateBtn = document.getElementById('calculate-btn');
    const formSection = document.querySelector('.form-section');
    
    if (isLoading) {
        calculateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculating...';
        calculateBtn.disabled = true;
        formSection.classList.add('loading');
    } else {
        calculateBtn.innerHTML = '<i class="fas fa-calculator"></i> Calculate Travel Times';
        calculateBtn.disabled = false;
        formSection.classList.remove('loading');
    }
}

function showErrorMessages(errors) {
    clearErrorMessages();
    
    const formSection = document.querySelector('.form-section');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <div>
            <strong>Please fix the following errors:</strong>
            <ul style="margin: 5px 0 0 20px;">
                ${errors.map(error => `<li>${error}</li>`).join('')}
            </ul>
        </div>
    `;
    
    formSection.appendChild(errorDiv);
    
    // Scroll to error
    errorDiv.scrollIntoView({ behavior: 'smooth' });
}

function showSuccessMessage(message) {
    clearErrorMessages();
    
    const formSection = document.querySelector('.form-section');
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    
    formSection.appendChild(successDiv);
    
    // Remove success message after 3 seconds
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.parentNode.removeChild(successDiv);
        }
    }, 3000);
}

function clearErrorMessages() {
    const existingMessages = document.querySelectorAll('.error-message, .success-message');
    existingMessages.forEach(msg => msg.remove());
} 