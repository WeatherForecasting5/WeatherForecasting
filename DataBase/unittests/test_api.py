import pytest
from DataBase.api import get_converted_data


# Фиктивные данные для теста
class Row:
    def __init__(self, date, city_id, weather):
        self.date = date
        self.city_id = city_id
        self.weather = weather


class City:
    def __init__(self, name):
        self.name = name


@pytest.fixture
def mock_source_data():
    # Создаем фиктивные данные для теста
    city1 = City('City1')
    city2 = City('City2')

    rows = [
        Row('2022-01-01', city1, 10.0),
        Row('2022-01-01', city2, 20.0),
        Row('2022-01-02', city1, 15.0),
        Row('2022-01-02', city2, 25.0),
    ]

    return rows


def test_get_converted_data(mock_source_data):
    # Вызываем функцию с фиктивными данными
    result = get_converted_data(mock_source_data)

    # Проверяем результаты
    assert len(result['Date']) == 2  # Должно быть две уникальные даты
    assert len(result['City1']) == 2  # Должно быть два значения для города City1
    assert len(result['City2']) == 2  # Должно быть два значения для города City2
    assert result['City1'] == [10.0, 15.0]  # Правильные значения для города City1
    assert result['City2'] == [20.0, 25.0]  # Правильные значения для города City2
