import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px


def main_graphic(df: pd.DataFrame, title: str):
    """
    Вывод графика на главной странице

    Parameters
    ----------
    df: DataFrame с подготовленными к выводу данными
    title: название графика
    """
    fig = px.line(
        df,
        x='Date',
        y=df.columns[1::],
        title=title,
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def city_trace(fig, df: pd.DataFrame, title: str, city_selectbox: str, color=None):
    """
    Строит линии на уже имеющейся фрейме (fig)

    Parameters
    ----------
    fig: фрейм, на котором будет построен график
    df: данные, использующиеся для построения (pd.DataFrame)
    title: label к линии
    city_selectbox: город, к которому строится график
    color: цвет графика

    Returns
    -------
    Возвращает фрейм с данными о графике
    """
    fig.add_trace(go.Scatter(x=df['Date'],
                             y=df[city_selectbox],
                             name=title,
                             line=dict(color=color)))
    return fig


def set_layout(fig, title: str):
    """
    Задаёт настройки: убираем отступы, переносим легенду вниз, подписываем оси и т.п.

    Parameters
    ----------
    fig: фрейм, к которому применяются настройки
    title: название графика

    Returns
    -------
    Возвращает фрейм с нужными настройками
    """
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title=title,
                      xaxis_title="Дата",
                      yaxis_title="Температура",
                      margin=dict(l=0, r=0, t=50, b=0))
    return fig
