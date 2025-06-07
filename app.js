// App state
let flightCount = 0;
let flights = [];

// Initialize app when DOM loads
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Add first flight form
    addFlightForm();
    
    // Event listeners
    document.getElementById('add-flight-btn').addEventListener('click', addFlightForm);
    document.getElementById('calculate-btn').addEventListener('click', calculateTravelTimes);
}

// Automatic timezone detection functions
async function getTimezoneOffset(cityName) {
    try {
        // First, geocode the city name to get coordinates
        const coordinates = await geocodeCity(cityName);
        if (!coordinates) {
            throw new Error(`Could not find location: ${cityName}`);
        }

        // Then get timezone information from coordinates
        const timezoneInfo = await getTimezoneFromCoordinates(coordinates.lat, coordinates.lon);
        return timezoneInfo;
    } catch (error) {
        console.error('Error getting timezone offset:', error);
        throw error;
    }
}

async function geocodeCity(cityName) {
    // Helper function to create a fetch with timeout
    const fetchWithTimeout = (url, timeout = 5000) => {
        return Promise.race([
            fetch(url),
            new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Request timeout')), timeout)
            )
        ]);
    };

    try {
        // Using OpenStreetMap Nominatim API (free geocoding service) with 5 second timeout
        const response = await fetchWithTimeout(
            `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(cityName)}&format=json&limit=1`,
            5000
        );
        
        if (!response.ok) {
            throw new Error('Geocoding service unavailable');
        }
        
        const data = await response.json();
        
        if (data.length === 0) {
            throw new Error(`No location found for: ${cityName}`);
        }
        
        return {
            lat: parseFloat(data[0].lat),
            lon: parseFloat(data[0].lon),
            displayName: data[0].display_name
        };
    } catch (error) {
        console.error('Geocoding error:', error);
        throw error;
    }
}

async function getTimezoneFromCoordinates(lat, lon) {
    // Helper function to create a fetch with timeout
    const fetchWithTimeout = (url, timeout = 3000) => {
        return Promise.race([
            fetch(url),
            new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Request timeout')), timeout)
            )
        ]);
    };

    try {
        // Try using the free GeoNames timezone API with 3 second timeout
        const response = await fetchWithTimeout(
            `https://secure.geonames.org/timezoneJSON?lat=${lat}&lng=${lon}&username=demo`,
            3000
        );
        
        if (response.ok) {
            const data = await response.json();
            if (data.rawOffset !== undefined) {
                const utcOffset = data.rawOffset + (data.dstOffset || 0);
                return {
                    utcOffset: utcOffset,
                    timezoneName: data.timezoneId || `UTC${utcOffset >= 0 ? '+' : ''}${utcOffset}`
                };
            }
        }
    } catch (error) {
        console.log('GeoNames API failed, falling back to TimeAPI.io');
    }
    
    try {
        // Fallback: Try TimeAPI.io (free service) with 3 second timeout
        const response = await fetchWithTimeout(
            `https://timeapi.io/api/TimeZone/coordinate?latitude=${lat}&longitude=${lon}`,
            3000
        );
        
        if (response.ok) {
            const data = await response.json();
            if (data.standardUtcOffset) {
                // Parse offset string like "-05:00" to number
                const offsetMatch = data.standardUtcOffset.match(/([+-])(\d{2}):(\d{2})/);
                if (offsetMatch) {
                    const sign = offsetMatch[1] === '+' ? 1 : -1;
                    const hours = parseInt(offsetMatch[2]);
                    const minutes = parseInt(offsetMatch[3]);
                    const utcOffset = sign * (hours + minutes / 60);
                    
                    return {
                        utcOffset: utcOffset,
                        timezoneName: data.timeZone || `UTC${utcOffset >= 0 ? '+' : ''}${utcOffset}`
                    };
                }
            }
        }
    } catch (error) {
        console.log('TimeAPI.io failed, falling back to estimation');
    }
    
    // Final fallback to coordinate-based estimation
    const utcOffset = estimateTimezoneOffset(lat, lon);
    return {
        utcOffset: utcOffset,
        timezoneName: `Estimated (UTC${utcOffset >= 0 ? '+' : ''}${utcOffset})`
    };
}

function estimateTimezoneOffset(lat, lon) {
    // Simple longitude-based timezone estimation
    // Each 15 degrees of longitude ≈ 1 hour of time difference
    let offset = Math.round(lon / 15);
    
    // Clamp to valid timezone range
    offset = Math.max(-12, Math.min(12, offset));
    
    // Apply regional adjustments for known exceptions
    
    // Asia adjustments
    if (lat > 5 && lat < 55 && lon > 70 && lon < 150) {
        if (lon > 68 && lon < 80) offset = 5; // Pakistan
        if (lon > 80 && lon < 92) offset = 5.5; // India
        if (lon > 92 && lon < 108) offset = 7; // Southeast Asia
        if (lon > 108 && lon < 128) offset = 8; // China, Philippines
        if (lon > 128 && lon < 146) offset = 9; // Japan, Korea
    }
    
    // Australia adjustments
    if (lat < -10 && lat > -45 && lon > 110 && lon < 155) {
        if (lon > 125 && lon < 141) offset = 9.5; // Central Australia
        if (lon > 141 && lon < 155) offset = 10; // Eastern Australia
    }
    
    // North America adjustments
    if (lat > 25 && lat < 70 && lon > -170 && lon < -50) {
        if (lon > -130 && lon < -100) offset = -7; // Mountain Time
        if (lon > -100 && lon < -85) offset = -6; // Central Time
        if (lon > -85 && lon < -65) offset = -5; // Eastern Time
    }
    
    // Europe adjustments
    if (lat > 35 && lat < 70 && lon > -10 && lon < 40) {
        if (lon > -10 && lon < 20) offset = 1; // Central European Time
        if (lon > 20 && lon < 40) offset = 2; // Eastern European Time
    }
    
    return offset;
}

// Debounce timers for auto-detection
const debounceTimers = {};

async function autoDetectTimezone(flightId, isArrival = false) {
    const cityInputId = isArrival ? `arrival-city-${flightId}` : `departure-city-${flightId}`;
    const timezoneSelectId = isArrival ? `arrival-timezone-${flightId}` : `departure-timezone-${flightId}`;
    const timezoneDisplayId = isArrival ? `arrival-timezone-display-${flightId}` : `departure-timezone-display-${flightId}`;
    
    const cityInput = document.getElementById(cityInputId);
    const timezoneSelect = document.getElementById(timezoneSelectId);
    const timezoneDisplay = document.getElementById(timezoneDisplayId);
    
    if (!cityInput.value.trim()) {
        return;
    }
    
    if (timezoneDisplay) {
        timezoneDisplay.innerHTML = 'Detecting timezone...';
        timezoneDisplay.className = 'timezone-display loading';
    }
    
    try {
        const timezoneInfo = await getTimezoneOffset(cityInput.value.trim());
        
        // Set the timezone in the select dropdown
        timezoneSelect.value = timezoneInfo.utcOffset;
        
        // Show timezone information
        if (timezoneDisplay) {
            timezoneDisplay.innerHTML = `Timezone: UTC${timezoneInfo.utcOffset >= 0 ? '+' : ''}${timezoneInfo.utcOffset}`;
            timezoneDisplay.className = 'timezone-display success';
        }
        

        
    } catch (error) {
        if (timezoneDisplay) {
            timezoneDisplay.innerHTML = 'Could not detect timezone';
            timezoneDisplay.className = 'timezone-display error';
        }

    }
}

// Auto-detect timezone when user stops typing
function setupAutoDetection(flightId, isArrival = false) {
    const cityInputId = isArrival ? `arrival-city-${flightId}` : `departure-city-${flightId}`;
    const timezoneDisplayId = isArrival ? `arrival-timezone-display-${flightId}` : `departure-timezone-display-${flightId}`;
    const cityInput = document.getElementById(cityInputId);
    const timezoneDisplay = document.getElementById(timezoneDisplayId);
    
    if (!cityInput) return;
    
    // Clear timezone display when input is cleared
    cityInput.addEventListener('input', function() {
        const debounceKey = `${flightId}-${isArrival}`;
        
        // Clear previous timer
        if (debounceTimers[debounceKey]) {
            clearTimeout(debounceTimers[debounceKey]);
        }
        
        // Clear timezone display if input is empty
        if (!this.value.trim()) {
            if (timezoneDisplay) {
                timezoneDisplay.innerHTML = '';
                timezoneDisplay.className = 'timezone-display';
            }
            return;
        }
        
        // Show "detecting..." after a short delay
        if (timezoneDisplay && this.value.trim().length > 2) {
            timezoneDisplay.innerHTML = 'Detecting timezone...';
            timezoneDisplay.className = 'timezone-display pending';
        }
        
        // Debounce the auto-detection (wait for user to stop typing)
        debounceTimers[debounceKey] = setTimeout(() => {
            if (this.value.trim().length > 2) {
                autoDetectTimezone(flightId, isArrival);
            }
        }, 1500); // Wait 1.5 seconds after user stops typing
    });
    
    // Also trigger on Enter key
    cityInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && this.value.trim().length > 2) {
            const debounceKey = `${flightId}-${isArrival}`;
            if (debounceTimers[debounceKey]) {
                clearTimeout(debounceTimers[debounceKey]);
            }
            autoDetectTimezone(flightId, isArrival);
        }
    });
}



function addFlightForm() {
    flightCount++;
    
    const flightsContainer = document.getElementById('flights-container');
    const flightDiv = document.createElement('div');
    flightDiv.className = 'flight-form fade-in';
    flightDiv.id = `flight-${flightCount}`;
    
    // Set default dates to today for departure and landing
    const today = new Date().toISOString().split('T')[0];
    
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
        
        <div class="flight-sections">
            <div class="departure-section">
                <h4 class="section-title">
                    <i class="fas fa-plane-departure"></i>
                    Departure
                </h4>
                <div class="section-grid">
                    <div class="form-group">
                        <label for="departure-city-${flightCount}">Departure City</label>
                        <input type="text" id="departure-city-${flightCount}" name="departure-city" 
                               placeholder="e.g., New York" required>
                        <input type="hidden" id="departure-timezone-${flightCount}" name="departure-timezone" value="0">
                        <div class="timezone-display" id="departure-timezone-display-${flightCount}"></div>
                    </div>
                    
                    <div class="form-group">
                        <label for="departure-date-${flightCount}">Departure Date</label>
                        <input type="date" id="departure-date-${flightCount}" name="departure-date" 
                               value="${today}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="departure-time-${flightCount}">Departure Time</label>
                        <input type="time" id="departure-time-${flightCount}" name="departure-time" required>
                    </div>
                </div>
            </div>
            
            <div class="arrival-section">
                <h4 class="section-title">
                    <i class="fas fa-plane-arrival"></i>
                    Arrival
                </h4>
                <div class="section-grid">
                    <div class="form-group">
                        <label for="arrival-city-${flightCount}">Arrival City</label>
                        <input type="text" id="arrival-city-${flightCount}" name="arrival-city" 
                               placeholder="e.g., London" required>
                        <input type="hidden" id="arrival-timezone-${flightCount}" name="arrival-timezone" value="0">
                        <div class="timezone-display" id="arrival-timezone-display-${flightCount}"></div>
                    </div>
                    
                    <div class="form-group">
                        <label for="arrival-date-${flightCount}">Landing Date</label>
                        <input type="date" id="arrival-date-${flightCount}" name="arrival-date" 
                               value="${today}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="arrival-time-${flightCount}">Arrival Time</label>
                        <input type="time" id="arrival-time-${flightCount}" name="arrival-time" required>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    flightsContainer.appendChild(flightDiv);
    
    // Setup auto-detection for this flight
    setupAutoDetection(flightCount, false); // departure
    setupAutoDetection(flightCount, true);  // arrival
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
        if (!formData.departureDate) {
            errors.push(`Flight ${flightNumber}: Please select departure date.`);
        }
        if (!formData.departureTime) {
            errors.push(`Flight ${flightNumber}: Please enter departure time.`);
        }
        if (!formData.arrivalCity.trim()) {
            errors.push(`Flight ${flightNumber}: Please enter arrival city.`);
        }
        if (!formData.arrivalDate) {
            errors.push(`Flight ${flightNumber}: Please select landing date.`);
        }
        if (!formData.arrivalTime) {
            errors.push(`Flight ${flightNumber}: Please enter arrival time.`);
        }
        
        // Validate that landing date is not before departure date
        if (formData.departureDate && formData.arrivalDate) {
            const depDate = new Date(formData.departureDate);
            const arrDate = new Date(formData.arrivalDate);
            if (arrDate < depDate) {
                errors.push(`Flight ${flightNumber}: Landing date cannot be before departure date.`);
            }
        }
    });
    
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
            data.departureDate,
            data.departureTime,
            parseFloat(data.departureTimezone),
            data.arrivalCity,
            data.arrivalDate,
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
        
        // Create calculator and calculate times
        const calculator = new TravelTimeCalculator(flights);
        
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