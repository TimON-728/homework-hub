from sqlalchemy import Column, Integer, String, JSON, Date, UniqueConstraint
from database import Base, engine

class Homework(Base):
    __tablename__ = "homework"
    id = Column(Integer, primary_key=True)

    subject = Column(String, nullable=False)
    task = Column(String)
    photos = Column(JSON)

    city = Column(String, nullable=False)
    school = Column(String, nullable=False)
    class_name = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('city', 'school', 'class_name', 'subject', name='unique_subject'),
        UniqueConstraint('city', 'school', 'class_name', name='unique_class'),
    )


class TimeTable(Base):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True)

    city = Column(String, nullable=False)
    school = Column(String, nullable=False)
    class_name = Column(String, nullable=False)

    timetable = Column(String, nullable=False)
    date_on = Column(Date, nullable=True)

    __table_args__ = (
        UniqueConstraint('city', 'school', 'class_name', name = 'unique_class'),
    )

Base.metadata.create_all(engine)
