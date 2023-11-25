from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Asset(Base):
    __tablename__ = 'assets'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    measurements_ = relationship('Measurement', back_populates='asset')

class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    timestamp = Column('timestamp', String)
    wind_speed = Column('wind_speed', String)
    power = Column('power', String)
    air_temperature = Column('air_temperature', String)
    created_at = Column('created_at', DateTime, server_default=func.now())
    updated_at = Column('updated_at', DateTime, onupdate=func.now())
    assets_id = Column('assets_id', ForeignKey('assets.id'), nullable=False)
    asset = relationship('Asset', back_populates='measurements_')


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
