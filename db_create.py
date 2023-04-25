from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:111111@localhost/data_base_agroserver", echo=True)
Base = declarative_base()


class AgroserverTechnic(Base):
    __tablename__ = 'sh_technic_agroserver'

    id = Column(Integer, primary_key=True)
    hex_id = Column(String(40), unique=True)
    reference_ad = Column(String(255), nullable=False)
    header_ad = Column(String(255), nullable=False)
    type_technic = Column(String(30), nullable=True)
    price_alone = Column(Float, nullable=True)
    price_lower = Column(Float, nullable=True)
    price_upper = Column(Float, nullable=True)
    price_unit = Column(String(10), nullable=False)
    offer_datetime = Column(DateTime, nullable=False)
    address = Column(String(250), nullable=True)
    model_technic = Column(String(30), nullable=True)
    year = Column(Float, nullable=True)
    condition = Column(String(30), nullable=True)
    maker = Column(String(30), nullable=True)
    moto_hours = Column(Float, nullable=True)
    power_engine = Column(Float, nullable=True)
    traktor_base = Column(String(30), nullable=True)

Base.metadata.create_all(engine)

