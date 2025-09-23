<<<<<<< HEAD
# Quantumix

A collection of innovative technology projects and experiments.

## 🦾 Bionic Hand IoT Dashboard

A real-time IoT monitoring dashboard for bionic hand prosthetics built with Django and Chart.js.

### 🚀 Features

- **Real-time Data Monitoring**: Live sensor data updates every 2 seconds
- **Comprehensive Sensor Display**: 
  - Grip Force tracking with timeline chart
  - EMG Signal strength monitoring
  - Individual finger flex sensors (5 fingers)
  - Temperature monitoring
  - Hand status indicators (Open/Closing/Closed)
- **Professional Dashboard**: Modern, responsive design optimized for medical applications
- **Error Handling**: Robust connection error handling with retry mechanisms
- **Mobile Responsive**: Works seamlessly on desktop, tablet, and mobile devices

### 📊 Dashboard Components

#### Status Cards
- **Hand Status**: Current state of the bionic hand
- **EMG Signal**: Electromyography signal strength
- **Temperature**: Real-time temperature monitoring
- **Grip Force**: Current grip force percentage

#### Real-time Charts
- **Grip Force Timeline**: Historical grip force data over time
- **EMG Signal Chart**: EMG signal strength visualization

#### Finger Monitoring
- **Individual Flex Sensors**: Real-time monitoring of all 5 fingers
- **Color-coded Status**: Visual indicators based on flex angles
  - Green: Low flex (0-30°)
  - Yellow: Medium flex (30-60°)
  - Red: High flex (60°+)

### 🛠️ Technology Stack

- **Backend**: Django 5.2.6
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Database**: SQLite (development)
- **Real-time Updates**: AJAX polling

### ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Skand03/Quantumix.git
   cd Quantumix
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install django channels
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser**
   Navigate to `http://127.0.0.1:8000/` to view the dashboard

### 📡 API Endpoints

#### `/api/sensors/`
Returns real-time sensor data in JSON format:

```json
{
  "flex_sensor": [45, 30, 60, 25, 80],
  "emg_signal": 250,
  "grip_force": 75,
  "temperature": 36.5,
  "hand_status": "Closed"
}
```

### 🎯 Use Cases

- **Medical Monitoring**: Real-time patient prosthetic monitoring
- **Research & Development**: Data collection for bionic hand improvements
- **Training & Therapy**: Visual feedback for prosthetic training
- **Quality Assurance**: Performance testing of bionic hand devices

### 🔧 Customization

#### Adding New Sensors
1. Update the API response in `api/views.py`
2. Add new display elements in `dashboard/templates/dashboard/dashboard.html`
3. Update JavaScript to handle new data fields

#### Styling
- Modify CSS in the dashboard template for custom themes
- Responsive breakpoints can be adjusted for different screen sizes

### 📱 Screenshots

The dashboard features a modern, medical-grade interface with:
- Gradient backgrounds and professional styling
- Real-time status indicators with pulse animations
- Interactive charts with smooth animations
- Mobile-responsive design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

- Built for innovative technology solutions
- Designed with accessibility and usability in mind
- Optimized for real-world applications

---

**Note**: The bionic hand dashboard uses simulated sensor data for development. For production use, replace the dummy data in `api/views.py` with actual sensor integrations.
=======
# Quantumix
>>>>>>> f2951b1fe61ea2b24a63a777861faa560edebffa
