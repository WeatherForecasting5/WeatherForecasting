import sys
sys.path.append('../WeatherForecasting/DataBase')
from filtering import *

import pandas as pd
import xgboost as xgb
from generate_days import test_data
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

pd.set_option('display.max_columns', None)
plt.figure(figsize=(15, 5))

days = test_data.copy()
one_hot = OneHotEncoder(handle_unknown='ignore')

def preproc(data):
    data = data.rename(columns={
        'Day': 'День',
        'Month': 'Месяц',
        'Year': 'Год'
    })

    one_hot_df = pd.DataFrame(one_hot.fit_transform(data[['Месяц']]).toarray())
    data.drop(['Месяц'], axis=1, inplace=True)
    data = data.join(one_hot_df)

    mesyaci = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    for i in range(12):
        data = data.rename(columns={
            i: mesyaci[i]
        })

    return data

look_df = filtered_df.copy(deep=True)

def separating_date(dataframe):    
    dataframe['Year'] = pd.to_datetime(dataframe['Date']).dt.year
    dataframe['Month'] = pd.to_datetime(dataframe['Date']).dt.strftime('%B')
    dataframe['Day'] = pd.to_datetime(dataframe['Date']).dt.day
    dataframe = dataframe.drop('Date', axis=1)

    dataframe = dataframe[[dataframe.columns[0], dataframe.columns[15], dataframe.columns[14], dataframe.columns[1],dataframe.columns[2],
                           dataframe.columns[3], dataframe.columns[4], dataframe.columns[5], dataframe.columns[6], dataframe.columns[7], 
                           dataframe.columns[8], dataframe.columns[9], dataframe.columns[10], dataframe.columns[11], dataframe.columns[12], dataframe.columns[13]]]
        
    return dataframe

look_df = separating_date(look_df)
df = preproc(look_df)

names = []
for el in list(df)[:1]:
    names.append(el)
for el in list(df)[2:14]:
    names.append(el)
for el in list(df)[1:2]:
    names.append(el)
for el in list(df)[14:]:
    names.append(el)

df = df[names]

target_names = list(df)[:13]
test_data = preproc(test_data)

y = df[target_names]  # данные за 20 лет
x = df.drop(target_names, axis=1)  # датасет с пустыми значениями

# Сплит данных для теста
# x_train, x_valid, y_train, y_valid = train_test_split(x, y, train_size=0.8, random_state=98)
# model = xgb.XGBRegressor()
# model.fit(x_train, y_train)
# y_pred = model.predict(x_valid)
# mae = mean_absolute_error(y_valid, y_pred)
# print(f'MAE: {mae}')


# На всех данных с предиктом на 2023
model = xgb.XGBRegressor()
model.fit(x, y)
y_pred = model.predict(test_data)
y_pred_df = pd.DataFrame(data=y_pred, columns=target_names)

pred_df = y_pred_df.merge(days, left_index=True, right_index=True)
pred_df = pred_df.sort_index()

# Transform data columns
month_to_number = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

pred_df['Date'] = pred_df.apply(lambda row: datetime(row['Year'], month_to_number[row['Month']], row['Day']).date(), axis=1)
pred_df = pred_df.drop(['Year', 'Month', 'Day'], axis=1) 

# По городам-----------------------------
# for city in target_names:
#     slice_y = y[6935:7300].copy()
#     slice_y = slice_y.reset_index()
#     plt.title(f"MAE: {mean_absolute_error(slice_y[city], y_pred_df[city])}, Город: {city}")
#     y_pred_df[city].plot()
#     slice_y[city].plot()
#     plt.legend(['Нейронка', 'Исходник'])
#     plt.xlabel('Дни, n')
#     plt.ylabel('Температура, C')
#     plt.show()


# По срезам лет-----------------------------
# print(y[365:365+365].head())
# for n in range(0, 7300, 365):
#     slice_y = y[n: n + 365].copy()
#     slice_y = slice_y.reset_index()
#     print(y.head())
#     plt.title(f"MAE: {mean_absolute_error(slice_y['Садовый'], y_pred_df['Садовый'])}, Город: Садовый")
#     y_pred_df['Садовый'].plot()
#     slice_y['Садовый'].plot()
#     plt.legend(['Нейронка', 'Исходник'])
#     plt.xlabel('Дни, n')
#     plt.ylabel('Температура, C')
#     plt.show()

