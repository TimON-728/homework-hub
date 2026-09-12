from select_city import select_city
from select_school import select_school
from select_class import select_class
from validation import Registration
from crud import *

import streamlit as st
from pydantic import ValidationError

def Regist():
    if "selected_city" not in st.session_state:
        st.session_state.selected_city = None
    if "selected_school" not in st.session_state:
        st.session_state.selected_school = None
    if "selected_class" not in st.session_state:
        st.session_state.selected_class = None

    if st.session_state.selected_city is None:
        select_city()
    if (st.session_state.selected_school is None) and (st.session_state.selected_city != None):
        select_school()
    if (st.session_state.selected_class is None) and (st.session_state.selected_school != None):
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