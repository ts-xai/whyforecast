import pandas as pd

data= pd.read_csv('spain_energy_market.csv')
# Lower case column names
data.columns = map(str.lower, data.columns)

print(data.columns)

data.drop(columns='id', inplace=True)
data.drop(columns='name', inplace=True)
data.drop(columns='geoid', inplace=True)
data.drop(columns='geoname', inplace=True)

data['datetime'] = data['datetime'].str.split(' ').str[0]
print(data)

data['datetime'] = pd.to_datetime(data['datetime'])
data.set_index('datetime', inplace=True)

monthly_average_sales = data.resample('MS').mean()
print(monthly_average_sales)

monthly_average_sales.to_csv('energySales.csv')
# #Replace spaces with '_'
# data.columns = data.columns.str.replace(" ", "_")
# data.columns = data.columns.str.replace("-", "_")
# furniture=data.loc[data['category'] == 'Furniture']
#
# technology=data.loc[data['category'] == 'Technology']
# office=data.loc[data['category'] == 'Office Supplies']
#
# furniture= furniture.groupby('order_date')['sales'].sum().reset_index()
#
# technology= technology.groupby('order_date')['sales'].sum().reset_index()
# office= office.groupby('order_date')['sales'].sum().reset_index()
# #Set index
# furniture = furniture.set_index('order_date')
#
# technology = technology.set_index('order_date')
# office = office.set_index('order_date')
#
# df = furniture['sales'].resample('MS').mean()
#
# df.to_csv('furnitureSales.csv')
