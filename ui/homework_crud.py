from crud import *
from database import *
from photos_utilits import *

import json
import streamlit as st
from pydantic import ValidationError
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
                if hw.photos:
                    photos = json.loads(hw.photos)
                    for photo_path in photos:
                        st.image(photo_path)


        if floating_button("Добавить", key="add_btn", icon=":material/add:"):
            st.session_state.page = "add_homework"
            st.rerun()

    elif st.session_state.page == 'add_homework':
        st.markdown('### Выберете предмет для изменения или добавте новый')

        city = st.session_state.selected_city
        school = st.session_state.selected_school
        class_name = st.session_state.selected_class 

        hws = read_homework_by_class(db=db, city=city, school=school, class_name=class_name)

        if st.session_state.subject is None:
            cols = st.columns(4)

            for i, hw in enumerate(hws):
                col_id = i % 4
                with cols[col_id]:
                    if st.button(hw.subject, key=f'subject_{hw.subject}', use_container_width=True):
                        st.session_state.subject = hw.subject
                        st.rerun()

            if st.button("➕ Добавить передмет", use_container_width=True):
                st.session_state.subject = "add subject"
                st.rerun()

        elif st.session_state.subject is not None:
            col1, col2 = st.columns(2)
            new_subject = st.session_state.subject

            if st.session_state.subject == "add subject":
                new_subject = st.text_input('Введите новый предмет')

                with col1:
                    if st.button('Подтвердить'):
                        if new_subject and new_subject.strip():
                            st.session_state.subject = new_subject
                            st.session_state.new_subject = True
                            st.rerun()
                        else:
                            st.warning('Название предмета не может быть пустым')

                with col2:
                    if st.button('Назад'):
                        st.session_state.subject = None
                        st.rerun()

            new_task = st.text_input('Введите задание')
            new_photo = st.file_uploader('Вставте одно или несколько фотографий', accept_multiple_files=True)

            with col1:
                if st.button('Подтвердить'):
                    try:
                        photos_path = save_photos(new_photo)

                        photos_json = json.dumps(photos_path)

                        reg = Registration(
                            city=city,
                            school=school,
                            class_name=class_name
                        )

                        hw_validation = HomeworkCreate(
                            city=reg.city,
                            school=reg.school,
                            class_name=reg.class_name,

                            subject=new_subject,
                            task=new_task,
                            photos=photos_json
                        )

                        if st.session_state.new_subject:
                            add_homework(db=db, data=hw_validation)

                        else:
                            for hw in hws:
                                if hw.subject == new_subject:
                                    update_homework(db=db, hw_id=hw.id, new_data=hw_validation)

                        st.session_state.subject = None
                        st.session_state.new_subject = False
                        st.rerun()
                    except (ValidationError, ValueError) as e:
                        st.error(f'Ошибка валидации: {e}')

            with col2:
                if st.button('Назад'):
                    st.session_state.subject = None
                    st.session_state.new_subject = False
                    st.rerun()

    db.close()
