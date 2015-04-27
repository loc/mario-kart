from sqlalchemy import *

engine = create_engine('sqlite:///kart.db', echo=True)
metadata = MetaData()

races = Table('races', metadata,
              Column('id', Integer, primary_key=True),
              Column('set_id', Integer),
              Column('datetime', Date))

ranks = Table('ranks', metadata,
              Column('race_id', Integer, ForeignKey('races.id'), primary_key=True),
              Column('elapsed', Float),
              Column('timestamp', Float, primary_key=True),
              Column('rank', Integer),
              Column('player', Integer, primary_key=True))

laps = Table('laps', metadata,
             Column('race_id', Integer, ForeignKey('races.id'), primary_key=True),
             Column('elapsed', Float),
             Column('timestamp', Float),
             Column('lap', Integer, primary_key=True),
             Column('player', Integer, primary_key=True))

hazards = Table('hazards', metadata,
             Column('race_id', Integer, ForeignKey('races.id'), primary_key=True),
             Column('timestamp', Float, primary_key=True),
             Column('player', Integer, primary_key=True))

metadata.create_all(engine, checkfirst=True) 
