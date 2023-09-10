import streamlit as st
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
from PIL import Image
from lottie_animation import load_lottie_url

# Устанавливаем настройки страницы
st.set_page_config(page_title='Прогноз погоды', page_icon='images/sun-icon.png', layout='wide')

# Сохраняем изображение с анимацией в переменную
# lottie = load_lottie_url('https://lottie.host/c12c9369-c5e6-4613-b61e-928516774793/TlgHM8PWZA.json')
lottie = load_lottie_url('https://lottie.host/d62d8066-bdfc-487c-bdfd-f2005924161a/nDRYGGSRFj.json')

# Выводим заголовок страницы
image_box, header_box = st.columns([0.05, 0.95])
with image_box:
    st_lottie(lottie, height=80, width=80)
    # image = Image.open('header-icon.png')
    # st.image(image)
with header_box:
    st.header('Прогноз погоды', )

# Задаём настройки боковой панели
with st.sidebar:
    # Заголовок боковой панели. '#' отвечают за размер текста (см. https://doka.guide/tools/markdown)
    st.write("# Погоду какого города Вы хотели бы рассмотреть?")
    city_selectbox = st.sidebar.selectbox(
        label='Выбор города',
        # Здесь подгружаем данные о городах из БД
        options=('Город А', 'Город Б', 'Город В'),
        label_visibility="collapsed"
    )

# Пример графика из документации
# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c']
# )
#
# st.line_chart(chart_data)

# Интересный пример спиннера, если данные из бд подгружаются не сразу
# with st.spinner("Loading..."):
#     time.sleep(5)
# st.success("Done!")
