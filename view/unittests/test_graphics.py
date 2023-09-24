import pandas as pd
import plotly.graph_objs as go
import pytest
from view.graphics import city_trace, set_layout


@pytest.fixture
def sample_data():
    data = {
        'Date': ['2022-01-01', '2022-01-02', '2022-01-03'],
        'City1': [10, 15, 20],
        'City2': [5, 10, 15],
    }
    return pd.DataFrame(data)


def test_city_trace(sample_data):
    fig = go.Figure()
    df = sample_data
    title = "City Trace"
    city_selectbox = 'City1'
    color = 'blue'
    updated_fig = city_trace(fig, df, title, city_selectbox, color)
    # Check if the trace is added to the figure
    assert len(updated_fig.data) == 1
    assert updated_fig.data[0].name == title
    assert updated_fig.data[0].x.tolist() == df['Date'].tolist()
    assert updated_fig.data[0].y.tolist() == df[city_selectbox].tolist()
    assert updated_fig.data[0].line.color == color


def test_set_layout(sample_data):
    fig = go.Figure()
    title = "Set Layout"
    updated_fig = set_layout(fig, title)
    # Check if the layout is updated
    assert updated_fig.layout.title.text == title
    assert updated_fig.layout.xaxis.title.text == "Дата"
    assert updated_fig.layout.yaxis.title.text == "Температура"
    assert updated_fig.layout.margin.l == 0
    assert updated_fig.layout.margin.r == 0
    assert updated_fig.layout.margin.t == 50
    assert updated_fig.layout.margin.b == 0
