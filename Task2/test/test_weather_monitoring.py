import unittest
from helper import get_weather_data, parse_weather_data
from models import init_db, WeatherData, DailySummary
from datetime import datetime

class TestWeatherMonitoring(unittest.TestCase):

    def setUp(self):
        self.engine = init_db()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_get_weather_data(self):
        city = 'Delhi'
        data = get_weather_data(city)
        self.assertIn('weather', data)
        self.assertIn('main', data['weather'][0])
        self.assertIn('temp', data['main'])

    def test_parse_weather_data(self):
        sample_data = {
            "weather": [{"main": "Clear"}],
            "main": {"temp": 300, "feels_like": 295},
            "dt": 1609459200
        }
        parsed_data = parse_weather_data(sample_data)
        self.assertEqual(parsed_data['main'], "Clear")
        self.assertAlmostEqual(parsed_data['temp'], 26.85, places=1)
        self.assertAlmostEqual(parsed_data['feels_like'], 21.85, places=1)
        self.assertEqual(parsed_data['dt'], datetime.fromtimestamp(1609459200))

    def test_save_weather_data(self):
        weather_data = {
            'main': 'Clear',
            'temp': 26.85,
            'feels_like': 21.85,
            'dt': datetime.now()
        }
        save_weather_data(self.session, 'Delhi', weather_data)
        result = self.session.query(WeatherData).filter_by(city='Delhi').first()
        self.assertIsNotNone(result)
        self.assertEqual(result.main, 'Clear')
        self.assertAlmostEqual(result.temp, 26.85, places=1)

    def test_calculate_daily_summary(self):
        city = 'Delhi'
        date = datetime(2021, 1, 1)
        weather_entries = [
            WeatherData(city=city, main='Clear', temp=20, feels_like=19, dt=date),
            WeatherData(city=city, main='Rain', temp=25, feels_like=24, dt=date + timedelta(hours=1)),
            WeatherData(city=city, main='Clear', temp=22, feels_like=21, dt=date + timedelta(hours=2))
        ]
        self.session.bulk_save_objects(weather_entries)
        self.session.commit()
        calculate_daily_summary(self.session, city, date)
        summary = self.session.query(DailySummary).filter_by(city=city, date=date).first()
        self.assertIsNotNone(summary)
        self.assertEqual(summary.avg_temp, 22.33)
        self.assertEqual(summary.max_temp, 25)
        self.assertEqual(summary.min_temp, 20)
        self.assertEqual(summary.dominant_condition, 'Clear')

    def test_check_alert_conditions(self):
        city = 'Delhi'
        threshold_temp = 30
        weather_entry = WeatherData(city=city, main='Clear', temp=35, feels_like=34, dt=datetime.now())
        self.session.add(weather_entry)
        self.session.commit()
        check_alert_conditions(self.session, city, threshold_temp)
        # Test should include mock or capture to verify alerting logic

if __name__ == '__main__':
    unittest.main()
