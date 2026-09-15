from crud import *
from database import *

import streamlit as st


def work_with_homework():
    city = st.session_state.selected_city
    school = st.session_state.selected_school
    class_name = st.session_state.selected_class

    db = next(get_db())

    subjects = db.query(Homework).with_entities(Homework.subject).filter(
        Homework.city == city,
        Homework.school == school,
        Homework.class_name == class_name
    ).all()

    tasks = db.query(Homework).with_entities(Homework.task).filter(
        Homework.city == city,
        Homework.school == school,
        Homework.class_name == class_name
    ).all()

    