import pandas as pd

from generate_days import test_data
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
# dfghoudfnhondfh

pd.set_option('display.max_columns', None)
plt.figure(figsize=(15, 5))


days = test_data.copy()
one_hot = OneHotEncoder(handle_unknown='ignore')

def preproc(data):
    data = data.rename(columns={
        'Date': 'День',
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

df = pd.read_csv('filtered_df.csv')
df = preproc(df)

names = []
for el in list(df)[2:15]:
    names.append(el)
for el in list(df)[:2]:
    names.append(el)
for el in list(df)[15:]:
    names.append(el)

df = df[names]
print(df.head())


target_names = list(df)[:13]
test_data = preproc(test_data)

y = df[target_names]
x = df.drop(target_names, axis=1)

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
print(y_pred_df.head())

# print(days.head())


pred_df = y_pred_df.merge(days, left_index=True, right_index=True)
pred_df = pred_df.sort_index()
print(pred_df.head())

pred_df.to_csv('result_model_xgb.csv')



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