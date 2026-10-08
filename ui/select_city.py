import streamlit as st

from validation import *
from crud import *


def select_city():
    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    city_list = read_all_cities()

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
            st.rerun()

    elif st.session_state.selected_city == "add city":
        new_city = st.text_input('Введите название нового города')

        col1, col2 = st.columns(2)
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

    if st.session_state.selected_city not in ["add city", None]:
        st.session_state.page = 'school_select'
        st.rerun()