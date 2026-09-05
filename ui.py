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
    city, school, class_name = db.query(Homework).with_entities(Homework.city, Homework.school, Homework.class_name).all() #ПЕРЕПИСАТЬ
    
    db.close()

render_ui()