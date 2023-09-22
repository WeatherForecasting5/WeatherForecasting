import pandas as pd
import streamlit as st
from DataBase.models import *


# Запрос, который будет выводить информацию о всех городах
@st.cache_data(show_spinner='Подождите, загружаем данные...')
def get_df(type_id: int) -> pd.DataFrame:
    with db.atomic():
        data = {'Date': []}

        source_data = Source.select(Source.date, Source.city_id, Source.weather).where(Source.type_id == type_id)

        for row in source_data:
            if row.date not in data['Date']:
                data['Date'].append(row.date)
            if row.city_id.name in data.keys():
                data[row.city_id.name].append(row.weather)
            else:
                # Инициализация списка
                data[row.city_id.name] = [row.weather]

    return pd.DataFrame(data)


# def get_cities():
#     cities = {}
#
#     with db.atomic():
#         cities_data = City.select()
#         for city in cities_data:
#             cities[city.id] = city.name
#
#     return cities
