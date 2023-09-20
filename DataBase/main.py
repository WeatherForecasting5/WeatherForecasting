from models import *
import pandas as pd
import os
import datetime

# DB model Initialising
with db:
    db.create_tables([Type, City, Configuration, Source])

# 'types' table data filling
data_type = [
    (1, 'pre-filtered'),
    (2, 'filtered'),
    (3, 'forcasted')
]

with db.atomic():
    Type.insert_many(data_type, fields=[Type.id, Type.name]).execute()

# 'cities' table data filling
current_directory = os.path.dirname(__file__)
csv_file_path = os.path.join(current_directory, '../Filtering_data/source_df.csv')
source_df = pd.read_csv(csv_file_path)
city_list = list(source_df.columns[1:])
data_city = list()  # data to writing into the DB
count = 1

for city in city_list:
    data = (count, city)
    data_city.append(data)
    count += 1

with db.atomic():
    City.insert_many(data_city, fields=[City.id, City.name]).execute()

# 'configurations' table data filling
data_config = [
    (1, 'original'),
    (2, 'random forrest model'),
    (3, 'xgbust model'),
    (4, 'tbats model')
]

with db.atomic():
    Configuration.insert_many(data_config, fields=[Configuration.id, Configuration.name]).execute()

################### Pre-filtered data for 'sources' table
################### id, date, city_id, weather, type_id, config_id
data_source = list() # main pre-filtered data container

type_id = data_type[0][0]  # 1: pre-filtered
config_id = data_config[0][0]  # 1: original

count = 1

for i in range(len(data_city)):
    for j in range(len(source_df)):
        city_name = data_city[i][1]
        weather = source_df[city_name][j]  # one weather value
        date = source_df['Date'][j]
        city_id = data_city[i][0]  # take an id of the city
        source = (count, date, city_id, weather, type_id, config_id)
        data_source.append(source)
        count += 1

batch_size = 1000

with db.atomic():
    for i in range(0, len(data_source), batch_size):
        batch = data_source[i:i + batch_size]
        Source.insert_many(batch, fields=[
            Source.id, 
            Source.date, 
            Source.city_id, 
            Source.weather, 
            Source.type_id, 
            Source.config_id
        ]).execute()

#################### Filtered data for 'sources' table
#################### id, date, city_id, weather, type_id, config_id
csv_file_path = os.path.join(current_directory, '../Filtering_data/filtered_df.csv')
filtered_df = pd.read_csv(csv_file_path)

data_filtered = list()  # main filtered data container

type_id = data_type[1][0]  # 2: 'filtered' type of data (after filtering)
config_id = data_config[0][0]  # 1: original

f_count = len(source_df) * len(data_city) + 1

for i in range(len(data_city)):
    for j in range(len(filtered_df)):
        city_name = data_city[i][1]
        weather = filtered_df[city_name][j]  # one weather value
        date = filtered_df['Date'][j]
        city_id = data_city[i][0]  # take an id of the city
        f_source = (f_count, date, city_id, weather, type_id, config_id)
        data_filtered.append(f_source)
        f_count += 1

batch_size = 1000

with db.atomic():
    for i in range(0, len(data_filtered), batch_size):
        batch = data_filtered[i:i + batch_size]
        Source.insert_many(batch, fields=[
            Source.id, 
            Source.date, 
            Source.city_id, 
            Source.weather, 
            Source.type_id, 
            Source.config_id
        ]).execute()
