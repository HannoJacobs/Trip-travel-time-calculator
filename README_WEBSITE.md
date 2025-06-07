# Travel Time Calculator - Web Application

A beautiful, modern web application that calculates total flight time, layover time, and travel time for multi-stage trips across different timezones.

## 🌐 Live Website

Visit the calculator at: `https://[your-username].github.io/Trip-travel-time-calculator`

## ✈️ Features

- **Multi-flight Support**: Add multiple flights to calculate complex itineraries
- **Timezone Awareness**: Handles flights across different timezones automatically
- **Beautiful Interface**: Modern, responsive design that works on all devices
- **Real-time Calculations**: Instant results as you input your flight data
- **Layover Analysis**: Shows individual layover times between flights
- **No Installation Required**: Runs entirely in your web browser

## 🚀 How to Use

1. **Set Departure Date**: Choose the date for your first flight
2. **Add Flights**: Click "Add Flight" to input your flight details:
   - Departure city and time
   - Departure timezone (UTC offset)
   - Arrival city and time  
   - Arrival timezone (UTC offset)
3. **Multiple Flights**: Add as many connecting flights as needed
4. **Calculate**: Click "Calculate Travel Times" to see your results
5. **View Results**: See total flight time, total travel time, total layover time, and individual layover breakdowns

## 📊 Results Explained

- **Total Flight Time**: Time spent actually flying (wheels up to wheels down)
- **Total Travel Time**: End-to-end time from first departure to final arrival
- **Total Layover Time**: Combined time spent waiting between flights
- **Individual Layovers**: Breakdown of each layover period

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS with gradients, animations, and responsive design
- **Icons**: Font Awesome 6
- **Fonts**: Inter (Google Fonts)
- **Hosting**: GitHub Pages
- **No Dependencies**: Pure vanilla JavaScript, no frameworks required

## 🏗️ Architecture

The application is built with three main components:

1. **calculator.js**: Core calculation logic (converted from Python)
   - `Flight` class: Represents individual flights
   - `TravelTimeCalculator` class: Handles timezone conversions and time calculations

2. **app.js**: User interface and interaction logic
   - Dynamic form generation
   - Input validation
   - Results display
   - Error handling

3. **styles.css**: Modern, responsive styling
   - Mobile-first design
   - Smooth animations
   - Accessible color scheme

## 🌍 Timezone Support

The calculator supports timezones from UTC-12 to UTC+12, including:
- Half-hour offsets (e.g., India Standard Time UTC+5:30)
- Major world timezones with friendly names
- Automatic daylight saving time considerations

## 📱 Responsive Design

The website is fully responsive and optimized for:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes and orientations

## 🔧 Development

To modify or extend the calculator:

1. Clone the repository
2. Edit the HTML, CSS, or JavaScript files
3. Test locally by opening `index.html` in a browser
4. Commit and push changes to deploy via GitHub Pages

## 🐛 Error Handling

The application includes comprehensive error handling for:
- Invalid date formats
- Missing required fields
- Timezone calculation errors
- Flight scheduling conflicts

## 💡 Tips for Accurate Results

- Use 24-hour time format (e.g., 14:30 for 2:30 PM)
- Double-check timezone offsets for accuracy
- Consider daylight saving time when applicable
- Ensure flight times are in local time for each city

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements such as:
- Additional timezone support
- Enhanced UI features
- Performance optimizations
- Mobile app version

## 📄 License

This project is open source and available under the MIT License.

---

Built with ❤️ for travelers who want to better understand their journey times. 