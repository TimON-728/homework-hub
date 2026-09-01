from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func

engine = create_engine("sqlite:///./homework.db")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Homework(Base):
    __tablename__ = "homework"
    id = Column(Integer, primary_key=True)
    subject = Column(String)
    description = Column(String)
    photos = Column

Base.metadata.create_all(engine)

db = SessionLocal()
hw = db.query(Homework).first()  
db.close()  