// Flight class to represent a single flight
class Flight {
    constructor(departureCity, departureDate, departureTime, departureTimezoneUtcOffsetInHours, 
                arrivalCity, arrivalDate, arrivalTime, arrivalTimezoneUtcOffsetInHours) {
        this.departureCity = departureCity;
        this.departureDate = departureDate;
        this.departureTime = departureTime;
        this.departureTimezoneUtcOffsetInHours = departureTimezoneUtcOffsetInHours;
        this.arrivalCity = arrivalCity;
        this.arrivalDate = arrivalDate;
        this.arrivalTime = arrivalTime;
        this.arrivalTimezoneUtcOffsetInHours = arrivalTimezoneUtcOffsetInHours;
    }
}

// TravelTimeCalculator class to calculate travel times
class TravelTimeCalculator {
    constructor(flights) {
        this.flights = flights;
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

    // Create a datetime object from date and time strings with timezone offset
    createDateTime(dateStr, timeStr, timezoneOffset) {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) {
            throw new Error(`Invalid date format: ${dateStr}`);
        }
        
        const timeMinutes = this.parseTime(timeStr);
        const hours = Math.floor(timeMinutes / 60);
        const minutes = timeMinutes % 60;
        
        // Create local datetime
        const localDateTime = new Date(date);
        localDateTime.setHours(hours, minutes, 0, 0);
        
        // Convert to UTC
        const utcDateTime = new Date(localDateTime.getTime() - (timezoneOffset * 60 * 60 * 1000));
        
        return utcDateTime;
    }

    // Calculate travel times
    calculateTravelTimes() {
        // Reset cumulative variables
        this.totalAirTime = 0;
        this.totalTravelTime = 0;
        this.totalLayoverTime = 0;
        this.layoverTimes = [];

        if (this.flights.length === 0) {
            return {
                totalAirTime: this.totalAirTime,
                totalTravelTime: this.totalTravelTime,
                totalLayoverTime: this.totalLayoverTime,
                layoverTimes: this.layoverTimes
            };
        }

        let prevArrivalUtc = null;
        let initialDepartureUtc = null;
        let finalArrivalUtc = null;

        for (let index = 0; index < this.flights.length; index++) {
            const flight = this.flights[index];
            
            try {
                // Create departure datetime in UTC
                const depDatetimeUtc = this.createDateTime(
                    flight.departureDate, 
                    flight.departureTime, 
                    flight.departureTimezoneUtcOffsetInHours
                );

                // Create arrival datetime in UTC
                const arrDatetimeUtc = this.createDateTime(
                    flight.arrivalDate, 
                    flight.arrivalTime, 
                    flight.arrivalTimezoneUtcOffsetInHours
                );

                // Validate that arrival is after departure
                if (arrDatetimeUtc <= depDatetimeUtc) {
                    throw new Error(`Flight ${index + 1}: Arrival time must be after departure time`);
                }

                // Calculate layover time if not the first flight
                if (prevArrivalUtc) {
                    if (depDatetimeUtc < prevArrivalUtc) {
                        throw new Error(`Flight ${index + 1}: Departure time must be after the previous flight's arrival time`);
                    }
                    
                    const layoverDuration = depDatetimeUtc.getTime() - prevArrivalUtc.getTime();
                    this.layoverTimes.push(layoverDuration);
                    this.totalLayoverTime += layoverDuration;
                }

                // Calculate flight duration
                const flightDuration = arrDatetimeUtc.getTime() - depDatetimeUtc.getTime();
                this.totalAirTime += flightDuration;

                // Set initial departure UTC
                if (index === 0) {
                    initialDepartureUtc = depDatetimeUtc;
                }

                // Update final arrival UTC
                finalArrivalUtc = arrDatetimeUtc;

                // Update previous arrival UTC for next iteration
                prevArrivalUtc = arrDatetimeUtc;

            } catch (error) {
                throw new Error(`Error processing flight ${index + 1}: ${error.message}`);
            }
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