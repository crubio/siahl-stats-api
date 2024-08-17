from sqlalchemy import Column, Integer, String
from .database import Base

class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)

class Player(Base):
    __tablename__ = "players"
    player_id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    stats_url = Column(String, nullable=False)

    