from sqlalchemy import *

class Database():
    def __init__(self):

        self.engine = create_engine('sqlite:///kart.db')
        self.metadata = MetaData()
        self.races = Table('races', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('set_id', Integer),
                      Column('datetime', Date))

        self.ranks = Table('ranks', self.metadata,
                      Column('race_id', Integer, ForeignKey('races.id'), primary_key=True),
                      Column('elapsed', Float),
                      Column('timestamp', Float, primary_key=True),
                      Column('rank', Integer),
                      Column('player', Integer, primary_key=True))

        self.laps = Table('laps', self.metadata,
                     Column('race_id', Integer, ForeignKey('races.id'), primary_key=True),
                     Column('elapsed', Float),
                     Column('timestamp', Float),
                     Column('lap', Integer, primary_key=True),
                     Column('player', Integer, primary_key=True))

        self.hazards = Table('hazards', self.metadata,
                     Column('race_id', Integer, ForeignKey('races.id'), primary_key=True),
                     Column('timestamp', Float, primary_key=True),
                     Column('player', Integer, primary_key=True))

        self.players = Table('players', self.metadata,
                        Column('set_id', Integer),
                        Column('player', Integer),
                        Column('name', String(100), nullable=True),
                        Column('character', String(100), nullable=True),
                        Column('vehicle', String(100), nullable=True))



if __name__ == "__main__":
    db = Database()
    db.metadata.create_all(db.engine, checkfirst=True) 
