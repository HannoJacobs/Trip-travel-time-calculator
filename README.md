# [✈️ Trip Travel Time Calculator](hannojacobs.github.io/Trip-travel-time-calculator/)

> **Calculate total flight time, layover time, and travel time for complex multi-stage journeys across time zones**


## 🌟 Features

- **Multi-Stage Trip Planning**: Handle complex itineraries with multiple connecting flights
- **Timezone Intelligence**: Automatically handles timezone conversions across different regions
- **Comprehensive Time Calculations**: 
  - Total flight time (actual time in the air)
  - Total travel time (door-to-door journey time)
  - Individual and total layover times
- **Multiple Interfaces**:
  - 🐍 **Python API** for programmatic use and integration
  - 🌐 **Web Interface** for interactive trip planning
  - 📱 **Responsive Design** that works on all devices

## 🚀 Quick Start

### 🐍 Python API

**Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 🌐 Web Interface (Recommended)

1. **Start a local server:**
   ```bash
   # Option 1: Using Python (if you have Python installed)
   python -m http.server 8000
   ```

2. **Open your browser and navigate to [http://localhost:8000](http://localhost:8000):**

3. **Start planning your trip:**
   - Add your flights with departure/arrival cities, dates, and times
   - The interface will automatically handle timezone detection
   - Click "Calculate Travel Times" to see your results instantly!


## 🛠️ How It Works

The calculator handles the complexity of:

- **Timezone Conversions**: Automatically converts all times to UTC for accurate calculations
- **Date Line Crossing**: Properly handles flights that cross the international date line
- **Layover Validation**: Ensures departure times are after previous arrival times
- **Duration Calculations**: Computes precise flight and layover durations

### Supported Time Formats

- **Dates**: `YYYY-MM-DD` (e.g., `2024-01-01`)
- **Times**: `HH:MM` in 24-hour format (e.g., `14:30`)
- **Timezones**: UTC offset in hours (e.g., `-5` for EST, `+1` for CET)

## 🧪 Testing

Run the test suite:
```bash
bash test.sh
```

## 🌍 Use Cases

Perfect for:
- **Complex International Travel**: Multi-city trips with various layovers
- **Travel Planning**: Understanding total journey time for scheduling
- **Business Travel**: Calculating actual travel time for expense reporting
- **Vacation Planning**: Optimizing itineraries and connection times
- **Travel Agencies**: Providing accurate time estimates to clients


## Use cases

- Built for travelers who need accurate time calculations across time zones
- Inspired by the complexity of modern multi-stage international travel
- Designed to eliminate manual timezone math and calculation errors

---

**Happy Travels!** ✈️🌍
