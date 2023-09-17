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
city_list = list(source_df.columns[3:])
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
