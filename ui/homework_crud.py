from crud import *
from database import *

import streamlit as st
from streamlit_extras.floating_button import floating_button


def work_with_homework():
    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    if st.session_state.page == 'homework_select':
        st.markdown('### Смотрите и редактируйте ДЗ')
        city = st.session_state.selected_city
        school = st.session_state.selected_school
        class_name = st.session_state.selected_class

        db = next(get_db())

        homework = read_homework_by_class(city=city, school=school, class_name=class_name)

        cols = st.columns(4)

        """for i, (subject, task) in enumerate(homework.items()):
            col_id = i % 4
            with cols[col_id]:
                st.markdown(f'## {subject}')
                st.markdown(f'# {task}')""" #ПЕРЕПИСАТЬ НА НОВУЮ ЛОГИКУ

        if floating_button("➕ Добавить", key="add_btn", icon=":material/add:"):
            st.session_state.page = "add_homework"
            st.rerun()

    elif st.session_state.page == 'add_homework':
        pass

    db.close

