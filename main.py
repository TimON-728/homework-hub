from ui.registration import Regist
from ui.homework_crud import work_with_homework
from ui.timetable_crud import work_with_timatable
import streamlit as st


defaults = {
    "page": "city_select",
    "selected_city": None,
    "selected_school": None,
    "selected_class": None,
    "subject": None,
    "new_subject": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value



if st.session_state.page in ['city_select', 'school_select', 'class_select']:
    Regist()
else:
    view = st.sidebar.radio(
        "Что смотрим?",
        ["Домашнее задание", "Расписание"]
    )
    if view == 'Домашнее задание':
        work_with_homework()
    elif view == 'Расписание':
        work_with_timatable()