import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from streamlit_lottie import st_lottie
from lottie_animation import load_lottie_url

# Папка с данными
data_folder = '../Filtering_data/'

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

# Считываем исходные данные, преобразуя столбцы сразу в DateTime
source_df = pd.read_csv(data_folder + 'source_df.csv', parse_dates=[[0, 1, 2]])
filtered_df = pd.read_csv(data_folder + 'filtered_df.csv', parse_dates=[[0, 1, 2]])

# Преобразуем столбец Date_Month_Year в Date для вывода графиков
source_df = source_df.rename(columns={'Date_Month_Year': 'Date'})
filtered_df = filtered_df.rename(columns={'Date_Month_Year': 'Date'})

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
    fig = px.line(
        source_df,
        x='Date',
        y=source_df.columns[1::],
        title='Погода по всем городам',
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
else:
    st.write(f'### Прогноз по городу {city_selectbox}')

    # График отфильтрованной температуры по городам (см. GROUP #5 Roadmap, ВИЗУАЛИЗАЦИЯ ДАННЫХ (ГРАФИКИ))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=source_df['Date'],
                             y=source_df[city_selectbox],
                             name='Данные с выбросами',
                             line=dict(color='grey')))
    fig.add_trace(go.Scatter(x=filtered_df['Date'],
                             y=filtered_df[city_selectbox],
                             name='Отфильтрованные данные'))

    # Задаём настройки: убираем отступы, переносим легенду вниз, подписываем оси и т.п.
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="График с отфильтрованными данными и выбросами",
                      xaxis_title="Дата",
                      yaxis_title="Температура",
                      margin=dict(l=30, r=30, t=30, b=30))

    # Задаём подписи при наведении на точку
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>Температура: %{y}")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
