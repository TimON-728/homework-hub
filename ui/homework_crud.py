from crud import *
from database import *

import streamlit as st
from streamlit_extras.floating_button import floating_button


def work_with_homework():
    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    db = next(get_db())

    if st.session_state.page == 'homework_select':
        st.markdown('### Смотрите и редактируйте ДЗ')

        city = st.session_state.selected_city
        school = st.session_state.selected_school
        class_name = st.session_state.selected_class

        hws = read_homework_by_class(db=db, city=city, school=school, class_name=class_name)

        cols = st.columns(4)

        for i, hw in enumerate(hws):
            col_id = i % 4
            with cols[col_id]:
                st.markdown(f'**{hw.subject}**')
                st.write(hw.task)
                if hw.photo:
                    st.image(hw.photo)


        if floating_button("Добавить", key="add_btn", icon=":material/add:"):
            st.session_state.page = "add_homework"
            st.rerun()

    elif st.session_state.page == 'add_homework':
        #Написать логику выбора предмета (как в select_city), потом добаление задания и фото, валидацию и добавление в бд
        #Если предмет новый, то нужно переключить флаг и при добавлении в бд использовать не Update, а Create
        pass

    db.close

