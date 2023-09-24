import datetime
import pandas as pd
import streamlit as st
from st_card_component import card_component

unique_keys = []


def place_card(i: int, key: str, filtered: pd.DataFrame, city_selectbox: str):
    """
    Размещение карточки с датой и прогнозом погоды на эту дату

    Parameters
    ----------
    i: индекс элемента df
    key: уникальный ключ для карточки (формируется из названия города + даты)
    filtered: DataFrame, отфильтрованный по нужным датам (это может быть, как день, так и на больший промежуток времени)
    city_selectbox: название текущего города

    Returns
    -------
    None
    """
    # Получаем температуру в выбранный день по выбранному городу
    temp = round(filtered[city_selectbox].values[i], 2)

    # with st.container():
    #     st.write(f'### {filtered["Date"].values[i].strftime("%d.%m.%Y")}')
    #     st.write(f'#### {temp} °С')

    card_component(
        title=f'{filtered["Date"].values[i].strftime("%d.%m.%Y")}',
        context=f'{temp} °С',
        highlight_start=0,
        highlight_end=None,
        score=None,
        url=None,
        key=str(key),
    )


def set_containers(filtered: pd.DataFrame, city_selectbox: str, col_count=7):
    """
    Обёртка над функцией place_card. Размещает сразу несколько карточек по 7 столбцов (на каждый день недели)

    Parameters
    ----------
    filtered: DataFrame, отфильтрованный по нужным датам
    city_selectbox: название города
    col_count: количество столбцов

    Returns
    -------
    None
    """
    columns = st.columns(col_count)
    for i in range(len(filtered)):
        with columns[i % col_count]:
            unique_key = city_selectbox + filtered['Date'].values[i].strftime("%d.%m.%Y")

            idx = 0
            while unique_key in unique_keys:
                if '_' not in unique_key:
                    unique_key = unique_key + '_' + str(idx)
                else:
                    unique_key = unique_key[:unique_key.index('_') + 1] + str(idx)
                idx += 1

            unique_keys.append(unique_key)
            place_card(i, unique_key, filtered, city_selectbox)


# Эта функция будет вызывать отображение погоды на день, неделю, месяц
def show_tabs(date: datetime.date, end_date: datetime.date, df: pd.DataFrame, city_selectbox: str):
    """
    Функция, отвечающая за вывод табов (3-х вкладок по соответствующим промежуткам времени)

    Parameters
    ----------
    date: выбранная, в date_input дата, по которой и будет прогноз
    end_date: дата, замыкающая вывод прогнозов. Обычно это месяц после date, но если этот месяц выходит за 31.12.2023,
              то за конечную дату берётся 31 декабря
    df: DataFrame с прогнозированными данными за 2023 год
    city_selectbox: название города

    Returns
    -------
    None
    """
    day, week, month = st.tabs(['На день', 'На неделю', 'На месяц'])

    with day:
        # Отбираем данные на выбранный день
        filtered = df.loc[df['Date'] == date]
        set_containers(filtered, city_selectbox)

    with week:
        # Отбираем данные на неделю
        end_of_week = date + datetime.timedelta(days=7 - 1)
        filtered = df.loc[(df['Date'] >= date) & (df['Date'] <= end_of_week)]
        set_containers(filtered, city_selectbox)

    with month:
        # Отбираем данные на месяц
        filtered = df.loc[(df['Date'] >= date) & (df['Date'] <= end_date)]
        set_containers(filtered, city_selectbox)
