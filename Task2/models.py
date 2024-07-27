from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    main = Column(String)
    temp = Column(Float)
    feels_like = Column(Float)
    dt = Column(DateTime)

class DailySummary(Base):
    __tablename__ = 'daily_summary'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    date = Column(DateTime)
    avg_temp = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    dominant_condition = Column(String)

def init_db():
    engine = create_engine('sqlite:///weather.db')
    Base.metadata.create_all(engine)
    return engine
