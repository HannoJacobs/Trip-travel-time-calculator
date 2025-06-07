// Flight class to represent a single flight
class Flight {
    constructor(departureCity, departureTime, departureTimezoneUtcOffsetInHours, 
                arrivalCity, arrivalTime, arrivalTimezoneUtcOffsetInHours) {
        this.departureCity = departureCity;
        this.departureTime = departureTime;
        this.departureTimezoneUtcOffsetInHours = departureTimezoneUtcOffsetInHours;
        this.arrivalCity = arrivalCity;
        this.arrivalTime = arrivalTime;
        this.arrivalTimezoneUtcOffsetInHours = arrivalTimezoneUtcOffsetInHours;
    }
}

// TravelTimeCalculator class to calculate travel times
class TravelTimeCalculator {
    constructor(flights, departureDate = '2024-01-01') {
        this.flights = flights;
        this.departureDate = departureDate;
        this.layoverTimes = [];
        this.totalAirTime = 0;
        this.totalTravelTime = 0;
        this.totalLayoverTime = 0;
    }

    // Parse time string to minutes since midnight
    parseTime(timeStr) {
        const [hours, minutes] = timeStr.split(':').map(Number);
        return hours * 60 + minutes;
    }

    // Convert minutes since midnight to time string
    formatTime(minutes) {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
    }

    // Calculate travel times
    calculateTravelTimes() {
        // Parse departure date
        let currentDate = new Date(this.departureDate);
        if (isNaN(currentDate.getTime())) {
            throw new Error('Invalid departure date format');
        }

        // Reset cumulative variables
        this.totalAirTime = 0;
        this.totalTravelTime = 0;
        this.totalLayoverTime = 0;
        this.layoverTimes = [];

        let prevArrivalUtc = null;
        let initialDepartureUtc = null;
        let finalArrivalUtc = null;

        for (let index = 0; index < this.flights.length; index++) {
            const flight = this.flights[index];
            
            // Parse departure and arrival times (in minutes since midnight)
            const depTimeMinutes = this.parseTime(flight.departureTime);
            const arrTimeMinutes = this.parseTime(flight.arrivalTime);

            // Create departure datetime in local timezone
            let depDatetimeLocal = new Date(currentDate);
            depDatetimeLocal.setHours(0, depTimeMinutes, 0, 0);

            // Convert to UTC
            let depDatetimeUtc = new Date(depDatetimeLocal.getTime() - 
                (flight.departureTimezoneUtcOffsetInHours * 60 * 60 * 1000));

            // If not the first flight, ensure departure is after previous arrival
            if (prevArrivalUtc) {
                let daysAdded = 0;
                while (depDatetimeUtc <= prevArrivalUtc) {
                    depDatetimeLocal.setDate(depDatetimeLocal.getDate() + 1);
                    depDatetimeUtc = new Date(depDatetimeLocal.getTime() - 
                        (flight.departureTimezoneUtcOffsetInHours * 60 * 60 * 1000));
                    daysAdded++;
                    if (daysAdded > 365) {
                        throw new Error('Infinite loop detected in flight scheduling');
                    }
                }

                // Calculate layover time
                const layoverDuration = depDatetimeUtc.getTime() - prevArrivalUtc.getTime();
                this.layoverTimes.push(layoverDuration);
                this.totalLayoverTime += layoverDuration;
            }

            // Create arrival datetime in local timezone
            let arrDatetimeLocal = new Date(depDatetimeLocal);
            arrDatetimeLocal.setHours(0, arrTimeMinutes, 0, 0);

            // Convert to UTC
            let arrDatetimeUtc = new Date(arrDatetimeLocal.getTime() - 
                (flight.arrivalTimezoneUtcOffsetInHours * 60 * 60 * 1000));

            // Adjust arrival date until arrival UTC is after departure UTC
            let daysAdded = 0;
            while (arrDatetimeUtc <= depDatetimeUtc) {
                arrDatetimeLocal.setDate(arrDatetimeLocal.getDate() + 1);
                arrDatetimeUtc = new Date(arrDatetimeLocal.getTime() - 
                    (flight.arrivalTimezoneUtcOffsetInHours * 60 * 60 * 1000));
                daysAdded++;
                if (daysAdded > 365) {
                    throw new Error('Infinite loop detected in flight scheduling');
                }
            }

            // Calculate flight duration
            const flightDuration = arrDatetimeUtc.getTime() - depDatetimeUtc.getTime();
            this.totalAirTime += flightDuration;

            // Update initial departure UTC
            if (index === 0) {
                initialDepartureUtc = depDatetimeUtc;
            }

            // Update final arrival UTC
            finalArrivalUtc = arrDatetimeUtc;

            // Update previous arrival UTC for next iteration
            prevArrivalUtc = arrDatetimeUtc;

            // Update current date for next flight
            currentDate = new Date(depDatetimeLocal);
        }

        // Calculate total travel time
        if (initialDepartureUtc && finalArrivalUtc) {
            this.totalTravelTime = finalArrivalUtc.getTime() - initialDepartureUtc.getTime();
        } else {
            this.totalTravelTime = 0;
        }

        return {
            totalAirTime: this.totalAirTime,
            totalTravelTime: this.totalTravelTime,
            totalLayoverTime: this.totalLayoverTime,
            layoverTimes: this.layoverTimes
        };
    }

    // Format milliseconds to human readable string
    static formatTimedelta(milliseconds) {
        if (milliseconds < 0) {
            return "Invalid time";
        }
        
        const totalMinutes = Math.floor(Math.abs(milliseconds) / (1000 * 60));
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        
        return `${hours} hours ${minutes} minutes`;
    }

    // Get formatted total air time
    getTotalAirTime() {
        this.calculateTravelTimes();
        return TravelTimeCalculator.formatTimedelta(this.totalAirTime);
    }

    // Get formatted total travel time
    getTotalTravelTime() {
        this.calculateTravelTimes();
        return TravelTimeCalculator.formatTimedelta(this.totalTravelTime);
    }

    // Get formatted total layover time
    getTotalLayoverTime() {
        this.calculateTravelTimes();
        return TravelTimeCalculator.formatTimedelta(this.totalLayoverTime);
    }

    // Get individual layover times as formatted strings
    getIndividualLayoverTimes() {
        this.calculateTravelTimes();
        return this.layoverTimes.map(layover => 
            TravelTimeCalculator.formatTimedelta(layover)
        );
    }

    // Add a flight to the itinerary
    addFlight(flight) {
        this.flights.push(flight);
    }
}

// Export for use in other files (if using modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Flight, TravelTimeCalculator };
} 