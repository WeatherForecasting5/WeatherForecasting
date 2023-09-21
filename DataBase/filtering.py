import urllib.request
import json
import pandas as pd

# Pre-filtering data (adding data)
from datetime import datetime, timedelta

start_date = datetime(2003, 1, 1)
end_date = datetime(2022, 12, 31)

dates_list = []


# Iterate through each date in the range, skipping leap days
current_date = start_date
while current_date <= end_date:
    if current_date.month == 2 and current_date.day == 29:
        pass
    else:
        dates_list.append(current_date.strftime("%d.%m.%Y"))
    
    current_date += timedelta(days=1)  # move next day


# Taking data from University API
import ssl
miet_ssl = ssl._create_unverified_context()  # ignore the ssl sertifiacte becayse of the original university SSL certificate

source_df = pd.DataFrame()
values = pd.DataFrame()

source_df['Date'] = dates_list

for i in range(1, 14):
    with urllib.request.urlopen('https://dt.miet.ru/spinteh/api/' + str(i), context = miet_ssl) as url:
        city_data = json.load(url)
    source_df[city_data['message']['name']] = city_data['message']['data']


# Implementing Exponential Moving Average filtering
filtered_df = source_df.copy(deep=True)

alpha = 0.2  # the less the resent
threshold = 15

for city in filtered_df.columns[1:]:
    column = str(city+'_EMA')
    filtered_df[column] = filtered_df[city].ewm(alpha=alpha, adjust=False).mean()

    filtered_df['Is_Outlier'] = abs(filtered_df[city] - filtered_df[column]) > threshold
    filtered_df.loc[filtered_df['Is_Outlier'], city] = filtered_df.loc[filtered_df['Is_Outlier'], column]  # replace ouliers
    filtered_df.drop([column, 'Is_Outlier'], axis=1, inplace=True)
