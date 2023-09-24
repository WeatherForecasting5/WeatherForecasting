# %%
import pandas as pd
import matplotlib.pyplot as plt
from filtering import *

data = filtered_df.copy(deep=True)

data['Date'] = pd.to_datetime(data['Date'])
data['Year'] = data['Date'].dt.year

# Calculate median
city_list = list(filtered_df.columns[1:])
for city in city_list:
    yearly_median = data.groupby('Year')[city].median().reset_index()

    # Create the graph
    plt.figure(figsize=(15, 9))
    plt.plot(yearly_median['Year'], yearly_median[city], label=city)
    plt.xlabel('Year')
    plt.ylabel('Weather Median value')
    plt.title('20-Year')
    plt.legend()
    plt.grid(True)
    plt.show()