from ui.registration import Regist
from ui.homework_crud import work_with_homework
from ui.timetable_crud import work_with_timatable
from crud import load_all_data
import streamlit as st

load_all_data(0)

defaults = {
    "page": "city_select",
    "selected_city": None,
    "selected_school": None,
    "selected_class": None,
    "subject": None,
    "new_subject": False,
    "date": None,
    "date_select": " "
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
        if st.session_state.page != 'add_homework':
            st.session_state.page = 'homework_select'
        work_with_homework()
    elif view == 'Расписание':
        if st.session_state.page != 'add_timetable':
            st.session_state.page = 'timetable select'
        work_with_timatable()