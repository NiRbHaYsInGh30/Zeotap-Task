import requests
import json
from datetime import datetime
from models import WeatherData, DailySummary
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import smtplib

API_KEY = 'your_api_key'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def parse_weather_data(data):
    weather_data = {
        'main': data['weather'][0]['main'],
        'temp': data['main']['temp'] - 273.15,  # Convert Kelvin to Celsius
        'feels_like': data['main']['feels_like'] - 273.15,
        'dt': datetime.fromtimestamp(data['dt'])
    }
    return weather_data

def save_weather_data(session, city, data):
    weather_entry = WeatherData(city=city, **data)
    session.add(weather_entry)
    session.commit()

def calculate_daily_summary(session, city, date):
    weather_entries = session.query(WeatherData).filter(
        WeatherData.city == city,
        WeatherData.dt >= date,
        WeatherData.dt < date + timedelta(days=1)
    ).all()

    if not weather_entries:
        return

    temps = [entry.temp for entry in weather_entries]
    main_conditions = [entry.main for entry in weather_entries]

    summary = DailySummary(
        city=city,
        date=date,
        avg_temp=sum(temps) / len(temps),
        max_temp=max(temps),
        min_temp=min(temps),
        dominant_condition=max(set(main_conditions), key=main_conditions.count)
    )
    session.add(summary)
    session.commit()

def send_alert(message):
    # Use smtplib or other email library to send alert emails
    pass

def check_alert_conditions(session, city, threshold_temp):
    latest_weather = session.query(WeatherData).filter(
        WeatherData.city == city
    ).order_by(WeatherData.dt.desc()).first()

    if latest_weather and latest_weather.temp > threshold_temp:
        send_alert(f"Temperature in {city} exceeded {threshold_temp}C: {latest_weather.temp}C")

