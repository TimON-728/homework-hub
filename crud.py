from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta

from models import *
from validation import *

#=============HOMEWORK=============
#==============CREATE==============
def add_homework(db: Session, data: HomeworkCreate) -> Homework:
    new_hw = Homework(
        subject = data.subject,
        task = data.task,
        photos = data.photos,

        city = data.city,
        school = data.school,
        class_name = data.class_name,
    )

    db.add(new_hw)
    db.commit()
    db.refresh(new_hw)

    return new_hw


#==============READ===============
def read_homework_by_class(db: Session, city: str, school: str, class_name: str):
    return db.query(Homework).filter(
        Homework.city == city,
        Homework.school == school,
        Homework.class_name == class_name
    ).all()


def get_hw_dy_id(db: Session, hw_id: int):
    return db.query(Homework).filter(
        Homework.id == hw_id
    ).first()


#==============UPDATE==============
def update_homework(db: Session, hw_id: int, new_data: dict):
    hw = get_hw_dy_id(db, hw_id)
    if hw:
        for key, value in new_data.items():
            setattr(hw, key, value)
        db.commit()
        db.refresh(hw)
    return hw


#==============DELETE==============
def delete_subject(db: Session, hw_id: int):
    hw = get_hw_dy_id(db, hw_id)
    if hw:
        db.delete(hw)
        db.commit()
    return hw


#=============TIMETBLE=============
#==============CREATE==============
def add_timetable(db: Session, data: TimetableCreate) -> TimeTable:
    new_tt = TimeTable(
        city = data.city,
        school = data.school,
        class_name = data.class_name,

        timetable = data.timetable,
        date_on = data.date_on,
    )

    db.add(new_tt)
    db.commit()
    db.refresh(new_tt)
    return new_tt


#==============READ===============
def read_timetable_by_week(db: Session, city: str, school: str, class_name: str):
    today = date.today()
    week_back = today - timedelta(days=7)
    return db.query(TimeTable).filter(
        TimeTable.city == city,
        TimeTable.school == school,
        TimeTable.class_name == class_name,
        TimeTable.date_on >= week_back
    ).all()


#==============UPDATE==============
def update_timetable(db: Session, city: str, school: str, class_name: str, date_on: date, new_timetable: str):
    tt = db.query(TimeTable).filter(
        TimeTable.city == city,
        TimeTable.school == school,
        TimeTable.class_name == class_name,
        TimeTable.date_on == date_on
    ).first()

    if tt:
        tt.timetable = new_timetable
        db.commit()
        db.refresh(tt)
    return tt
