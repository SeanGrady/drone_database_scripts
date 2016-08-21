from code import interact
import re
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, Float, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship

#sneaky regex
def snake_case(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

db_name = 'mission_data'
db_url = 'mysql+mysqldb://root:password@localhost/' + db_name
engine = create_engine(db_url)
Base = declarative_base()

#I've did a clever thing :D
class MyMixin(object):

    @declared_attr
    def __tablename__(cls):
        return snake_case(cls.__name__)

    id = Column(Integer, primary_key=True)


class Sensors(MyMixin, Base):
    sensor_type_id = Column(Integer, ForeignKey('sensor_types'.id))
    sensor_type = relationship("SensorTypes", back_populates="extant_sensors")

    sensor_readings = relationship("SensorReads", back_populates="sensor")

    mission_drone_instances = relationship("MissionDroneSensors",
                                        back_populates="sensor")

class SensorTypes(MyMixin, Base):
    sensor_type = Column(String(100), nullable=False)

    extant_sensors = relationship("Sensors", back_populates="sensor_type")

#TODO: Ask Ryan if I've done this polymorphic business correctly
class SensorReads(MyMixin, Base):
    sensor_id = Column(Integer, ForeignKey('sensors'.id))
    sensor = relationship("Sensors", back_populates="sensor_readings")

    event_id = Column(Integer, ForeignKey('events'.id))
    event = relationship("Events", back_populates='sensor_readings')

    mission_time = Column(Integer)
    data_type = Column(String(50))

    __mapper_args__ = {'polymorphic_on': data_type}

    data = relationship("AirSensorReads", back_populates='read_metadata')


#TODO: Figure out how events are going to work and add fields accordingly
class Events(MyMixin, Base):
    sensor_readings = relationship("SensorReads", back_populates='event')

class MissionDrones(MyMixin, Base):
    mission_id = Column(Integer, ForeignKey('missions'.id))
    mission = relationship("Missions", back_populates='drones')

    drone_id = Column(Integer, ForeignKey('drones'.id))
    drone = relationship("Drones", back_populates='mission_instances')

    mission_sensors = relationship("MissionDroneSensors", 
                                    back_populates='mission_drone')

class MissionDroneSensors(MyMixin, Base):
    mission_drone_id = Column(Integer, ForeignKey('mission_drones'.id))
    mission_drone = relationship('MissionDrones',
                                 back_populates='mission_sensors')

    sensor_id = Column(Integer, ForeignKey('sensors'.id))
    sensor = relationship("Sensors", back_populates='mission_drone_instances')

#TODO: Figure out how missions are going to be stored and add fields
class Missions(MyMixin, Base):
    description = Column(String(100), nullable=False)

    drones = relationship("MissionDrones", back_populates="mission")

class Drones(MyMixin, Base):
    description = Column(String(100), nullable=False)

    mission_instances = relationship("MissionDrones", back_populates='drone')

#TODO: Ask Ryan what to do about frequently changing data structure
class AirSensorReads(SensorReads):
    __tablename__ = snake_case(cls.__name__)
    __mapper_args__ = {'polymorphic_identity': 'air_sensor'}

    id = Column(Integer, ForeignKey('sensor_reads'.id), primary_key=True)
    AQI = Column(Integer)

class GPSSensorReads(SensorReads):
    __tablename__ = snake_case(cls.__name__)
    __mapper_args__ = {'polymorphic_identity': 'GPS'}

    id = Column(Integer, ForeignKey('sensor_reads'.id), primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Float)


Base.metadata.create_all(engine)
