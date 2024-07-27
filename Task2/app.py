from flask import Flask, request, render_template, jsonify
from models import init_db, WeatherData, DailySummary
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from helper import get_weather_data, parse_weather_data, save_weather_data, calculate_daily_summary, check_alert_conditions

app = Flask(__name__)
engine = init_db()
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_weather', methods=['POST'])
def update_weather():
    session = Session()
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    for city in cities:
        data = get_weather_data(city)
        parsed_data = parse_weather_data(data)
        save_weather_data(session, city, parsed_data)
    session.close()
    return "Weather data updated"

@app.route('/daily_summary', methods=['GET'])
def daily_summary():
    session = Session()
    city = request.args.get('city')
    date = request.args.get('date')
    if date:
        date = datetime.strptime(date, '%Y-%m-%d')
    else:
        date = datetime.today()
    
    calculate_daily_summary(session, city, date)
    summary = session.query(DailySummary).filter(DailySummary.city == city, DailySummary.date == date).first()
    session.close()
    return jsonify({
        'city': summary.city,
        'date': summary.date,
        'avg_temp': summary.avg_temp,
        'max_temp': summary.max_temp,
        'min_temp': summary.min_temp,
        'dominant_condition': summary.dominant_condition
    })

@app.route('/set_alert_threshold', methods=['POST'])
def set_alert_threshold():
    session = Session()
    city = request.json['city']
    threshold_temp = request.json['threshold_temp']
    check_alert_conditions(session, city, threshold_temp)
    session.close()
    return "Alert threshold set"

if __name__ == '__main__':
    app.run(debug=True)
