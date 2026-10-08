import streamlit as st

from validation import *
from crud import *


def select_school():
    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    school_list = read_schools_by_city(st.session_state.selected_city)

    if st.session_state.selected_school is None:
        st.markdown('#### Выберите школу или добавте новую')
        cols = st.columns(4)

        for i, school in enumerate(school_list):
            col_id = i % 4
            with cols[col_id]:
                if st.button(school, key=f"school_{school}", use_container_width=True):
                    st.session_state.selected_school = school
                    st.rerun()

        if st.button("➕ Добавить школу", use_container_width=True):
            st.session_state.selected_school = "add school"
            st.rerun()

    elif st.session_state.selected_school == "add school":
        new_school = st.text_input('Введите название новой школы')

        col1, col2 = st.columns(2)
        with col1:
            if st.button('Подтвердить'):
                if new_school and new_school.strip():
                    st.session_state.selected_school = new_school
                    st.rerun()
                else:
                    st.warning('Название школы не может быть пустым')

        with col2:
            if st.button('Назад'):
                st.session_state.selected_school = None
                st.rerun()

    if st.session_state.selected_school not in ["add school", None]:
        st.session_state.page = 'class_select'
        st.rerun()