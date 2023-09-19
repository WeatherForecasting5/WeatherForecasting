import datetime
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from streamlit_lottie import st_lottie
from lottie_animation import load_lottie_url
import graphics

# Папка с данными
data_folder = '../Filtering_data/'

# Формат даты
date_format = '%d.%m.%Y'

# Устанавливаем настройки страницы
st.set_page_config(page_title='Прогноз погоды', page_icon='images/sun-icon.png', layout='wide')

# Сохраняем изображение с анимацией в переменную
lottie = load_lottie_url('https://lottie.host/d62d8066-bdfc-487c-bdfd-f2005924161a/nDRYGGSRFj.json')

# Выводим заголовок страницы
image_box, header_box = st.columns([0.06, 0.94])
with image_box:
    st_lottie(lottie, height=85, width=85)
with header_box:
    st.header('Прогноз погоды')

# Считываем исходные данные, преобразуя столбцы в DateTime
source_df = pd.read_csv(data_folder + 'source_df.csv')
source_df['Date'] = pd.to_datetime(source_df['Date'], format=date_format)
filtered_df = pd.read_csv(data_folder + 'filtered_df.csv')
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format=date_format)

cities = source_df.columns[1::]

# Задаём настройки боковой панели
with st.sidebar:
    # Заголовок боковой панели. '#' отвечают за размер текста (см. https://doka.guide/tools/markdown)
    st.write("# Погоду какого города Вы хотели бы рассмотреть?")

    city_selectbox = st.sidebar.selectbox(
        label='Выбор города',
        # Здесь подгружаем данные о городах из БД
        options=('Общая информация', *cities),
        label_visibility="collapsed"
    )

# Вывод информации обо всех городах
if city_selectbox == 'Общая информация':
    graphics.main_graphic(source_df, 'Погода по всем городам')

else:
    st.write(f'### Прогноз по городу {city_selectbox}')

    st.write('Здесь хотелось бы видеть табы для прогноза из 3 разделов:')
    st.write('1. На день')
    st.write('2. На неделю')
    st.write('3. На месяц')
    st.write('День выбирается при помощи виджета-календаря (ниже)')

    date = st.date_input("Выберите день, на который нужно предсказать температуру:",
                         value=datetime.date(2023, 1, 1),
                         min_value=datetime.date(2023, 1, 1),
                         max_value=datetime.date(2023, 12, 31),
                         format='DD.MM.YYYY')

    # Аккордеон с графиками
    with st.expander('Вывести графики'):
        # Подписи при наведении на график
        hover_template = 'Дата: %{x}<br>Температура: %{y}'

        # График отфильтрованной температуры по городам (см. GROUP #5 Roadmap, ВИЗУАЛИЗАЦИЯ ДАННЫХ (ГРАФИКИ))
        fig = go.Figure()

        # Добавляем линии - график с выбросами и без
        fig = graphics.city_trace(fig, source_df, 'Данные с выбросами', city_selectbox, color='gray')
        fig = graphics.city_trace(fig, filtered_df, 'Отфильтрованные данные', city_selectbox)

        # Задаём настройки: убираем отступы, переносим легенду вниз, подписываем оси и т.п.
        fig = graphics.set_layout(fig, 'График с отфильтрованными данными и выбросами')

        # Задаём подписи при наведении на точку
        fig.update_traces(hoverinfo="all", hovertemplate=hover_template)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        # График для медианы по месяцам
        df_group_by_year_and_month = filtered_df.groupby([filtered_df['Date'].dt.year, filtered_df['Date'].dt.month])
        df_grouped_mean = df_group_by_year_and_month.mean()

        fig_mean = go.Figure()

        # Добавляем линию с медианой за 20 лет
        fig_mean = graphics.city_trace(fig_mean, df_grouped_mean, 'Медиана по месяцам', city_selectbox)

        # Задаём настройки: убираем отступы, переносим легенду вниз, подписываем оси и т.п.
        fig_mean = graphics.set_layout(fig_mean, 'Медиана по месяцам за каждый год')

        # Задаём подписи при наведении на точку
        fig_mean.update_traces(hoverinfo="all", hovertemplate=hover_template)
        st.plotly_chart(fig_mean, theme="streamlit", use_container_width=True)
