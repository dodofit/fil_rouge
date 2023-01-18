from entsoe import EntsoePandasClient
import pandas as pd
from datetime import datetime, timedelta

client = EntsoePandasClient(api_key="4e524938-86d0-4232-81a9-4c2aaf8cdceb")

start = pd.Timestamp('20170101', tz='Europe/Brussels')
end = pd.Timestamp('20221231', tz='Europe/Brussels')
country_code = 'BE'  # Belgium
country_code_from = 'FR'  # France
country_code_to = 'DE_LU' # Germany-Luxembourg
type_marketagreement_type = 'A01'
contract_marketagreement_type = "A01"

# methods that return Pandas Series
p = client.query_day_ahead_prices(country_code_from, start=start,end=end)

# methods that return Pandas DataFrames
s = client.query_load_forecast(country_code_from, start=start,end=end)
e = client.query_generation_forecast(country_code_from, start=start,end=end)

lst1 = list()
lst1.append(s)
lst2 = list()
lst2.append(e)
lst3 = list()
lst3.append(p)

result1 = pd.concat(lst1)
#print(result1)
result2 = pd.concat(lst2)
result3 = pd.concat(lst3)
#print(result3)
be_dataset = pd.concat([result3, result2, result1], axis=1)
#print(be_dataset)
df = be_dataset.set_axis(['Prices', 'Generation forecast', 'System load forecast'], axis=1, inplace=False)
#print(df)
df1 = df.rename_axis('Date').reset_index()
df1.dropna()

df1['Date'] = pd.to_datetime(df1.Date).dt.tz_localize(None)
df1['Date'] = df1['Date'].astype(object)
#print(df1.dtypes)

def daterange(start_date, end_date):
    delta = timedelta(hours=1)
    while start_date < end_date:
        yield start_date
        start_date += delta

df1=df1.set_index('Date')
df1.index = pd.to_datetime(df1.index)
start_date = df1.index[0]
end_date = df1.index[-1]+timedelta(hours=1)

i=0
real_date_list=[]
for single_date in daterange(start_date, end_date):
    real_date_list.append(single_date.strftime("%Y-%m-%d %H:%M:%S"))
    i+=1

list_index=df1.index.astype(str)
list_index_2=[]
for i in list_index:
    list_index_2.append(str(i))

difference = list()

for item in real_date_list:
    if item not in list_index_2:
        difference.append(item)

for ts in difference:
    ts = pd.to_datetime(ts)
    av = ts-timedelta(hours=1)
    ap = ts+timedelta(hours=1)
    price = (df1['Prices'].loc[pd.to_datetime(str(av))]+df1['Prices'].loc[pd.to_datetime(str(ap))])/2
    load = (df1['System load forecast'].loc[pd.to_datetime(str(av))]+ df1['System load forecast'].loc[pd.to_datetime(str(ap))])/2
    generation = (df1['Generation forecast'].loc[pd.to_datetime(str(av))]+ df1['Generation forecast'].loc[pd.to_datetime(str(ap))])/2
    new_row = pd.DataFrame([[price, generation, load]], columns = ["Prices", "Generation forecast", "System load forecast"], index=[ts])
    new_row.index = new_row.index.astype(str)
    dfs=[df1, new_row]

    df1=pd.concat(dfs)

df1.index = pd.to_datetime(df1.index)

seen = []
duplicates = []
for date in df1.index:
    if date in seen:
        duplicates.append(date)
    else:
        seen.append(date)

list_row=[]
for item in duplicates:
    new_row = pd.DataFrame([[df1['Prices'].loc[item].mean(), df1['Generation forecast'].loc[item].mean(), df1['System load forecast'].loc[item].mean()]], columns = ["Prices", "Generation forecast", "System load forecast"], index=[item])
    df1=df1.drop(item)
    df1= pd.concat([df1, new_row])

df1=df1.sort_index()

df1=df1.reset_index(names=['Date'])

#print(df1.head(5))
df1.to_csv('FR_new.csv', index=False)
