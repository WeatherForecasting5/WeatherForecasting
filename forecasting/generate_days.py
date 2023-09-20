import pandas as pd
import calendar

days = []
months = []
years = []

for year in range(2003, 2023):
    for month in range(1, 13):
        if calendar.isleap(year) == True:
            for day in range(1, calendar.monthrange(2007, month)[1] + 1):
                days.append(day)
                months.append(calendar.month_name[month])
                years.append(year)
        else:
            for day in range(1, calendar.monthrange(year, month)[1] + 1):
                days.append(day)
                months.append(calendar.month_name[month])
                years.append(year)

data = pd.DataFrame()
data['Date'] = days
data['Month'] = months
data['Year'] = years

test_data = data[:365]
test_data['Year'] = test_data['Year'].replace(2003, 2023)

# test_year = []
# for i in range(366):
#     test_year






