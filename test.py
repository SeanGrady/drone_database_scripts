from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from code import interact

Base = automap_base()

engine = create_engine('mysql+mysqldb://root:password@localhost/drone_logs')

Base.prepare(engine, reflect=True)

Sensors = Base.classes.sensors
SensorTypes = Base.classes.sensor_types

#session.add(Base.classes.sensor_types(sensor_type='air_sensor'))

session = Session(engine)

#session.add(Sensors(sensor_type_id=SensorTypes(sensor_type="air_sensor")))
#session.add(Address(email_address="foo@bar.com", user=User(name="foo")))

interact(local=locals())
