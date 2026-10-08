from crud import *
from validation import *
from photos_utilits import *

import streamlit as st
from streamlit_extras.floating_button import floating_button
from pydantic import ValidationError
from datetime import date, timedelta


def date_of_weekday(weekday: int, base_date: date = None) -> date:
    if base_date is None:
        base_date = date.today()
    monday = base_date - timedelta(days=base_date.weekday())
    return monday + timedelta(days=weekday)


def work_with_timatable():
    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    if st.session_state.page == 'timetable select':
        city = st.session_state.selected_city
        school = st.session_state.selected_school
        class_name = st.session_state.selected_class

        tts = read_timetable_by_week(city=city, school=school, class_name=class_name)

        cols = st.columns(2)

        for i, tt in enumerate(tts):
            col_id = i % 2
            with cols[col_id]:
                st.image(tt.timetable)
                days_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
                st.write(days_ru[tt.date_on.weekday()])

        if floating_button("Добавить", key="add_btn_2", icon=":material/add:"):
            st.session_state.page = "add_timetable"
            st.rerun()

    elif st.session_state.page == 'add_timetable':
        st.markdown('### Выберите дату')

        city = st.session_state.selected_city
        school = st.session_state.selected_school
        class_name = st.session_state.selected_class

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button('Сегодня'):
                st.session_state.date = date.today()
                st.session_state.date_select = " "
                st.rerun()

        with col2:
            if st.button('Завтра'):
                st.session_state.date = date.today() + timedelta(days=1)
                st.session_state.date_select = " "
                st.rerun()

        with col3:
            options = {
                " ": None,
                "Понедельник": date_of_weekday(0),
                "Вторник": date_of_weekday(1),
                "Среда": date_of_weekday(2),
                "Четверг": date_of_weekday(3),
                "Пятница": date_of_weekday(4),
                "Суббота": date_of_weekday(5),
                "Воскресенье": date_of_weekday(6),
            }

            chosen_day = st.selectbox(
                "Другая дата",
                options=list(options.keys()),
                format_func=lambda d: " " if d == " " else f"{d} ({options[d].strftime('%d.%m.%Y')})",
                key="date_select"
            )

            if chosen_day != " ":
                st.session_state.date = options[chosen_day]

        new_tt = st.file_uploader('Вставте фотографию расписания')

        col1, col2 = st.columns(2)
        with col1:
            if st.button('Подтвердить', key='confirm_tt'):
                new_date = st.session_state.date
                if not new_tt:
                    st.error('Фото не может быть пустым')
                elif not new_date:
                    st.error('Выберите дату')
                else:
                    try:
                        photos_path = save_photos([new_tt])

                        reg = Registration(
                            city=city,
                            school=school,
                            class_name=class_name
                        )

                        tt_validation = TimetableCreate(
                            city=reg.city,
                            school=reg.school,
                            class_name=reg.class_name,

                            timetable=photos_path[0],
                            date_on=new_date
                        )

                        update = False
                        tts = read_timetable_by_week(city=city, school=school, class_name=class_name)
                        for tt in tts:
                            if new_date == tt.date_on:
                                update = True
                                break

                        if update:
                            update_timetable(data=tt_validation)
                        else:
                            add_timetable(data=tt_validation)

                        st.session_state.page = "timetable select"
                        st.rerun()

                    except (ValidationError, ValueError) as e:
                        st.error(f'Ошибка валидации: {e}')

        with col2:
            if st.button('Назад'):
                st.rerun()