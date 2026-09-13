import streamlit as st

from models import *
from validation import *
from crud import *
from database import *


def select_class():
    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    # Получаем сессию
    db = next(get_db())
    class_list = []

    results = db.query(Homework).with_entities(Homework.class_name).filter(
        Homework.city == st.session_state.selected_city,
        Homework.school == st.session_state.selected_school
    ).all()

    class_list = list(set(class_name[0] for class_name in results))   

    if st.session_state.selected_class is None: 
        st.markdown('#### Выберите класс или добавте новый')
        cols = st.columns(4)

        for i, class_name in enumerate(class_list):
            col_id = i % 4
            with cols[col_id]:
                if st.button(class_name, key=f"class_{class_name}", use_container_width=True):
                    st.session_state.selected_class = class_name
                    st.rerun()

        if st.button("➕ Добавить класс", use_container_width=True):
            st.session_state.selected_class = "add class"
            st.rerun()

    elif st.session_state.selected_class == "add class":
        new_class = st.text_input('Введите название нового класса')

        col1, col2 = st.columns(2)
        if st.session_state.selected_class == "add class":
            with col1:
                if st.button('Подтвердить'):
                    if new_class and new_class.strip():
                        st.session_state.selected_class = new_class
                        st.rerun()
                    else:
                        st.warning('Название класса не может быть пустым')

            with col2:
                if st.button('Назад'):
                    st.session_state.selected_class = None
                    st.rerun()

    if st.session_state.selected_class not in ["add class", None]:
        st.session_state.page = 'homework_select'
        print('Переключаю')
        db.close()
        st.rerun()