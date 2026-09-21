from crud import *
from database import *
from validation import *
from photos_utilits import *

import streamlit as st
from pydantic import ValidationError

def work_with_timatable():
    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    db = next(get_db())

    if st.session_state.page == 'timetable select':
        pass

    db.close()