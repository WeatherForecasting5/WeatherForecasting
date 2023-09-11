import pandas as pd
import urllib.request
import calendar
import json
import ssl

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
        df[data['message']['name']]= data['message']['data']
        
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

    
def add_datatime(df: pd.DataFrame, start_year:int = 2003, end_year:int = 2023) -> pd.DataFrame:
    """  
    Добавляет даты к значениям

    Parameters
    ----------
    df : pd.DataFrame
        Массив данных к которому нужно добавить даты
    
    start_year: int
        Год начала отчёта

    end_year: int
        Год конца отчета

    Returns
    -------
    filter_df: pd.DataFrame
        Массив данных c датами.
    """
    miet_ssl = ssl._create_unverified_context()  # ignore the ssl sertifiacte becayse of the original university SSL certificate

    day_of_month_values = []
    corresponding_months = []
    corresponding_years = []

    for year in range(start_year, end_year):
        for month in range(1, 13):
            last_day = calendar.monthrange(year, month)[1]
            days_of_month = list(range(1, last_day + 1))
            day_of_month_values.extend(days_of_month)
            corresponding_months.extend([calendar.month_name[month]] * last_day)
            corresponding_years.extend([year] * last_day)

    # Provided data doesn't exist leap years
    filtered_values = [
        (day, month, year)
        for day, month, year in zip(day_of_month_values, corresponding_months, corresponding_years)
        if not (day == 29 and month == 'February')
    ]

    day_of_month_values, corresponding_months, corresponding_years = zip(*filtered_values)  # Unpack the filtered data

    df.insert(0, 'Date', day_of_month_values)
    df.insert(1, 'Month', corresponding_months)
    df.insert(2, 'Year', corresponding_years)

    return df

if __name__ == "__main__":
  df = add_datatime(weather_data_filter(load_data()))
  print(df)