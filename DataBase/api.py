import calendar
import datetime
import pandas as pd
import streamlit as st
from DataBase.models import *


def get_converted_data(source_data) -> dict:
    """
    Функция преобразует данные, полученные из БД, в удобный для вывода графиков вид

    Parameters
    ----------
    source_data: данные, полученные из БД

    Returns
    -------
    dict
    """
    data = {'Date': []}

    for row in source_data:
        if row.date not in data['Date']:
            data['Date'].append(row.date)
        if row.city_id.name in data.keys():
            data[row.city_id.name].append(row.weather)
        else:
            # Инициализация списка
            data[row.city_id.name] = [row.weather]

    return data


# Запрос, который будет выводить информацию о всех городах
@st.cache_data(show_spinner='Пожалуйста, подождите, загружаем данные...')
def get_df(type_id: int) -> pd.DataFrame:
    """
    Получение данных из БД по их типу, их последующий перевод в pd.DataFrame. Полученные данные кешируются.

    Parameters
    ----------
    type_id: тип данных (1 - pre-filtered, 2 - filtered, 3 - 'random forest', 4 - 'xgboost', 5 - 'tbats')

    Returns
    -------
    pd.DataFrame
    """
    with db.atomic():
        source_data = (Source
                       .select(Source.date, Source.city_id, Source.weather)
                       .where(Source.type_id == type_id))

    return pd.DataFrame(get_converted_data(source_data))


@st.cache_data(show_spinner='Пожалуйста, подождите, загружаем данные...')
def get_forecast_by_month(start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """
    Получение спрогнозированных на месяц данных. Полученные данные кешируются.

    Parameters
    ----------
    start_date: дата, начиная с которой нужно получить информацию из БД
    end_date: максимально возможная дата (в нашем случае - 31.12.2023)

    Returns
    -------
    pd.DataFrame
    """
    type_id = 4  # xgboost type

    # Если разница между start_date и end_date больше месяца, то приравниваем end_date к значению следующего месяца
    days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
    temp_end = start_date + datetime.timedelta(days=days_in_month - 1)      # -1 = не включительно
    if temp_end < end_date:
        end_date = temp_end

    with db.atomic():
        # Тут также надо будет выбрать конкретную конфигурацию модели
        source_data = (Source
                       .select(Source.id, Source.date, Source.city_id, Source.weather)
                       .where((Source.type_id == type_id) & ((Source.date >= start_date) & (Source.date <= end_date))))

    return pd.DataFrame(get_converted_data(source_data))
