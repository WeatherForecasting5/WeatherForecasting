import pandas as pd
import urllib.request
import json


def load_data (url:str = "https://dt.miet.ru/spinteh/api/", start_id:int = 1, stop_id:int = 13) -> pd.DataFrame:
  """
   Запрашивает у сервера данные и сохраняет их в pandas DataFrame

  Parameters
  ----------
  url : str
    Адрес где лежит база исходных данных
  start_id: int
    Индекс первого рассматриваемого города
  stop_id: int
    Индекс последнего рассматриваемого города

  Returns
  -------
  df: pd.DataFrame
    Массив полученных данных.
  """

  df = pd.DataFrame()
  for i in range(start_id, stop_id + 1):
    with urllib.request.urlopen("https://dt.miet.ru/spinteh/api/" + str(i)) as url:
        data = json.load(url)
    df[data['message']['name']] = values = data['message']['data']
  return df


def weather_data_filter (input_df: pd.DataFrame) -> pd.DataFrame:
  """
  Выполняет фильтрацию данных о погоде от точечных выбросов

  Parameters
  ----------
  input_df : pd.DataFrame
    Входной массив данных, должен содержать значения в виде чисел, без пропусков.

  Returns
  -------
  filter_df: pd.DataFrame
    Массив отфильтрованных данных.
  """
  filter_df = pd.DataFrame()
  k = 6
  for col in input_df.columns:
    df = pd.DataFrame()
    df["smooth"] = input_df[col].ewm(span = 30).mean()
    df["deviation"] = abs(input_df[col] - df.smooth)
    outliers_points = []
    outliers_points.append(df[df.deviation > df.deviation.std() * k]["deviation"].index)
    filter_df[col] = input_df[col].copy()
    for i in outliers_points:
      filter_df[col][i] = df.smooth[i]
  return filter_df


if __name__ == "__main__":
  df = weather_data_filter(load_data())
  print(df)