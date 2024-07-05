from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    is_active = Column(Boolean, default=True)
    is_m2m_account = Column(Boolean, default=False)
    hashed_password = Column(String)