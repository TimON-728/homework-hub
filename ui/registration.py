from select_city import select_city
from select_school import select_school
from select_class import select_class
from validation import Registration
from crud import *

import streamlit as st
from pydantic import ValidationError

def Regist():
    defaults = {
        "page": "city_selection",
        "selected_city": None,
        "selected_school": None,
        "selected_class": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.page == 'city_select':
        select_city()
    elif st.session_state.page == 'school_select':
        select_school()
    elif st.session_state.page == 'class_select':
        select_class()

    city = st.session_state.selected_city
    school = st.session_state.selected_school
    class_name = st.session_state.selected_class

    try:
        reg = Registration(
            city,
            school,
            class_name
        )
        #
        #Здесь будет логика изменения дз
        #
        st.session_state.selected_city = None
        st.session_state.selected_school = None
        st.session_state.selected_class = None
    except ValidationError as e:
        st.error(f'Ошибка валидации: {e}')