from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_name = 'simple_test'
db_url = 'mysql+mysqldb://root:password@localhost/' + db_name
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class SensorReading(Base):
    __tablename__ = 'sensor_readings'

    id = Column(Integer, primary_key=True)
    AQI = Column(Integer)
    mission_time = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Float)

Base.metadata.create_all(engine)

first_reading = SensorReading(
        AQI=7, 
        mission_time=10,
        lat=37.,
        lon=153.,
        alt=150
    )

session = Session()
session.add(first_reading)
session.commit()
