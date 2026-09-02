from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, JSON, UniqueConstraint
from sqlalchemy.sql import func

engine = create_engine("sqlite:///./homework.db")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Homework(Base):
    __tablename__ = "homework"
    id = Column(Integer, primary_key=True)

    subject = Column(String)
    description = Column(String)
    photos = Column(JSON)

    city = Column(String, nullable=False)
    school = Column(String, nullable=False)
    class_name = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('city', 'school', 'class_name', 'subject', name='unique_subject'),
        UniqueConstraint('city', 'school', 'class_name', name='unique_class'),
    )

Base.metadata.create_all(engine)
