import streamlit as st

from models import *
from validation import *
from crud import *
from database import *


def render_ui():
    if "selected_city" not in st.session_state:
        st.session_state.selected_city = None

    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    # Получаем сессию
    db = next(get_db())
    city_list = []
    school_list = []
    class_list = []

    results = db.query(Homework).with_entities(
        Homework.city, Homework.school, Homework.class_name
    ).all()

    for city, school, class_name in results:
        city_list.append(city)
        school_list.append(school)
        class_list.append(class_name)

    city_list = list(set(city_list))
    school_list = list(set(school_list))
    class_list = list(set(class_list))    

    if st.session_state.selected_city is None: 
        st.markdown('#### Выберите город или добавте новый')
        cols = st.columns(4)

        for i, city in enumerate(city_list):
            col_id = i % 4
            with cols[col_id]:
                if st.button(city, key=f"city_{city}", use_container_width=True):
                    st.session_state.selected_city = city
                    st.rerun()

        if st.button("➕ Добавить город", use_container_width=True):
            st.session_state.selected_city = "add city"

    elif st.session_state.selected_city == "add city":
        new_city = st.text_area('Введите название нового города')

        col1, col2 = st.columns(2)
        if st.session_state.selected_city == "add city":
            with col1:
                if st.button('Подтвердить'):
                    if new_city and new_city.strip():
                        st.session_state.selected_city = new_city
                        st.rerun()
                    else:
                        st.warning('Название города не может быть пустым')

            with col2:
                if st.button('Назад'):
                    st.session_state.selected_city = None
                    st.rerun()

    db.close()

render_ui()