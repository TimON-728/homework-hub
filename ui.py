import streamlit as st

from models import *
from validation import *
from crud import *
from database import *


def render_ui():
    st.title('📚 HOMEWORK-HUB 📚')
    st.subheader('🏠 Место, где вы можете удобно хранить ваше домашнее задание')

    # Получаем сессию
    db = next(get_db())
    result = db.query(Homework).with_entities(Homework.city, Homework.school, Homework.class_name).all()
    st.
    db.close()

render_ui()