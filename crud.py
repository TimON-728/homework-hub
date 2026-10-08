from sqlalchemy.orm import Session
from datetime import date, timedelta
import streamlit as st

from models import *
from validation import *
from photos_utilits import *


# ═══════════════════════════════════════════
# КЭШ ВСЕЙ БД (обновляется раз в 60 секунд)
# ═══════════════════════════════════════════

@st.cache_data(ttl=60)
def load_all_data(version: int = 0):
    """Загружает всю БД в память. Аргумент version сбрасывает кэш после записи."""
    from database import get_db
    db = next(get_db())
    try:
        return {
            "homework": db.query(Homework).all(),
            "timetable": db.query(TimeTable).all(),
        }
    finally:
        db.close()


def _get_version() -> int:
    """Читает текущую версию кэша. Если её нет — создаёт 0."""
    if "db_version" not in st.session_state:
        st.session_state.db_version = 0
    return st.session_state.db_version


def _bump_version() -> None:
    """Увеличивает версию на 1 — сбрасывает кэш после записи."""
    if "db_version" not in st.session_state:
        st.session_state.db_version = 0
    st.session_state.db_version += 1


# ═══════════════════════════════════════════
# СПИСКИ ДЛЯ ВЫПАДАЮЩИХ МЕНЮ
# ═══════════════════════════════════════════

def read_all_cities():
    data = load_all_data(_get_version())
    return sorted(set(hw.city for hw in data["homework"]))


def read_schools_by_city(city: str):
    data = load_all_data(_get_version())
    return sorted(set(hw.school for hw in data["homework"] if hw.city == city))


def read_classes_by_school(city: str, school: str):
    data = load_all_data(_get_version())
    return sorted(set(
        hw.class_name for hw in data["homework"]
        if hw.city == city and hw.school == school
    ))


#=============HOMEWORK=============
#==============CREATE==============
def add_homework(data: HomeworkCreate) -> Homework:
    from database import get_db
    db = next(get_db())
    try:
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
    finally:
        db.close()
    _bump_version()
    return new_hw


#==============READ===============
def read_homework_by_class(city: str, school: str, class_name: str):
    data = load_all_data(_get_version())
    return [
        hw for hw in data["homework"]
        if hw.city == city and hw.school == school and hw.class_name == class_name
    ]


def get_hw_dy_id(hw_id: int):
    data = load_all_data(_get_version())
    for hw in data["homework"]:
        if hw.id == hw_id:
            return hw
    return None


#==============UPDATE==============
def update_homework(hw_id: int, new_data: dict) -> Homework:
    from database import get_db
    db = next(get_db())
    try:
        hw = db.get(Homework, hw_id)
        if not hw:
            return None

        old_photos = hw.photos or []
        new_photos = new_data.get("photos", [])

        for key, value in new_data.items():
            setattr(hw, key, value)

        db.commit()
        db.refresh(hw)

        for path in old_photos:
            if path not in new_photos:
                delete_photos([path])
    finally:
        db.close()
    _bump_version()
    return hw


#==============DELETE==============
def delete_subject(hw_id: int):
    from database import get_db
    db = next(get_db())
    try:
        hw = db.get(Homework, hw_id)
        if hw:
            db.delete(hw)
            db.commit()
    finally:
        db.close()
    _bump_version()
    return hw


#=============TIMETBLE=============
#==============CREATE==============
def add_timetable(data: TimetableCreate) -> TimeTable:
    from database import get_db
    db = next(get_db())
    try:
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
    finally:
        db.close()
    _bump_version()
    return new_tt


#==============READ===============
def read_timetable_by_week(city: str, school: str, class_name: str):
    today = date.today()
    week_back = today - timedelta(days=7)
    data = load_all_data(_get_version())
    return [
        tt for tt in data["timetable"]
        if tt.city == city and tt.school == school
        and tt.class_name == class_name
        and tt.date_on is not None
        and tt.date_on >= week_back
    ]


#==============UPDATE==============
def update_timetable(data: TimetableCreate):
    from database import get_db
    db = next(get_db())
    try:
        tt = db.query(TimeTable).filter(
            TimeTable.city == data.city,
            TimeTable.school == data.school,
            TimeTable.class_name == data.class_name,
            TimeTable.date_on == data.date_on
        ).first()

        if tt:
            tt.timetable = data.timetable
            db.commit()
            db.refresh(tt)
    finally:
        db.close()
    _bump_version()
    return tt