from ui.select_city import select_city
from ui.select_school import select_school
from ui.select_class import select_class
from validation import Registration
from crud import *

import streamlit as st
from pydantic import ValidationError

def Regist():
    if st.session_state.page == 'city_select':
        select_city()
    elif st.session_state.page == 'school_select':
        select_school()
    elif st.session_state.page == 'class_select':
        select_class()
    elif st.session_state.page == 'homework_select':
        city = st.session_state.selected_city
        school = st.session_state.selected_school
        class_name = st.session_state.selected_class

        try:
            reg = Registration(
                city=city,
                school=school,
                class_name=class_name
            )
        except ValidationError as e:
            st.error(f'Ошибка валидации: {e}')