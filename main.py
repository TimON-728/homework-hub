from ui.registration import Regist
from ui.homework_crud import work_with_homework
import streamlit as st


defaults = {
    "page": "city_select",
    "selected_city": None,
    "selected_school": None,
    "selected_class": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value    

if st.session_state.page in ['city_select', 'school_select', 'class_select']:
    Regist()
elif st.session_state.page in ['homework_select', 'add_homework']:
    work_with_homework()