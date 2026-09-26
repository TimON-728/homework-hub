from crud import *
from database import *
from validation import *
from photos_utilits import *

import streamlit as st
import datetime
from pydantic import ValidationError

def work_with_timatable():
    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    db = next(get_db())

    if st.session_state.page == 'timetable select':
        city = st.session_state.selected_city
        school = st.session_state.selected_school
        class_name = st.session_state.selected_class

        tts = read_timetable_by_week(db=db, city=city, school=school, class_name=class_name)

        cols = st.columns(2)

        for i, tt in enumerate(tts):
            col_id = i % 2
            with cols[col_id]:
                st.image(tt.timetable)
                days_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
                st.write(days_ru[tt.date_on.weekday()])

    db.close()