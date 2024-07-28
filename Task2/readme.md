```markdown
# Real-Time Weather Monitoring System

## Overview
This application monitors weather conditions in real-time using the OpenWeatherMap API. It provides daily summaries, real-time alerts, and visualizations.

## Features
- Real-time data retrieval from OpenWeatherMap API
- Daily weather summaries (average, max, min temperatures, dominant condition)
- User-configurable alert thresholds
- Data visualization
- Simple UI for interaction

## Requirements
- Python 3.x
- Flask
- SQLAlchemy
- Requests

## Setup

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd Task2
   ```

2. **Set up virtual environment and install dependencies:**
   ```sh
   python -m venv venv
    venv\Scripts\activate
   pip install flask
   ```

3. **Configure the application:**
   - Add your OpenWeatherMap API key in `config.py`

4. **Initialize the database:**
   ```sh
   python -c "from models import init_db; init_db()"
   ```

5. **Run the application:**
   ```sh
   python app.py
   ```

6. **Access the UI:**
   Open a browser and go to `http://127.0.0.1:5000/`

## Testing

- Run the test suite:
  ```sh
  python -m unittest discover tests
  ```

## Additional Notes
- The system can be extended to support more weather parameters and additional features such as forecast summaries.

## Project Structure


```

## API Reference

- **OpenWeatherMap API**: [OpenWeatherMap API Documentation](https://openweathermap.org/api)

