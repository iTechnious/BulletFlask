import sqlalchemy.ext.declarative
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, TEXT, DateTime, Enum, JSON
from sqlalchemy.orm import sessionmaker

from routes.user import User
from statics import config

"""
uri = f"mysql:///?User={config.DB.user}&;"
      f"Password={config.DB.password}&"
      f"Database={config.DB.db}&"
      f"Server={config.DB.host}&"
      f"Port={config.DB.port}"
"""

uri = f"{config.DB.type}+{config.DB.driver}://{config.DB.user}:{config.DB.password}@" \
                                 f"{config.DB.host}:{config.DB.port}/{config.DB.db}"

engine = sqlalchemy.create_engine(uri)
factory = sessionmaker(bind=engine)

Base = sqlalchemy.ext.declarative.declarative_base()

class Content(Base):
    __tablename__ = f"{config.Instance.instance}_content"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    location = Column(Integer)
    type = Column(String(255))
    permissions = Column(JSON, default={})
    content = Column(TEXT)

class Groups(Base):
    __tablename__ = f"{config.Instance.instance}_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    permissions = Column(JSON, default={})

class Versions(Base):
    __tablename__ = f"{config.Instance.instance}_versions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    content = Column(TEXT)
    date = Column(DateTime, nullable=False)

class Users(User, Base, UserMixin):
    pass
