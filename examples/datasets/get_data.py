from entsoe import EntsoePandasClient
import pandas as pd

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
df = be_dataset.set_axis([' Prices', ' Generation forecast', ' System load forecast'], axis=1, inplace=False)
#print(df)
df1 = df.rename_axis('Date').reset_index()
df1.dropna()

df1['Date'] = pd.to_datetime(df1.Date).dt.tz_localize(None)
df1['Date'] = df1['Date'].astype(object)
#print(df1.dtypes)

#print(df1.head(5))
df1.to_csv('FR_new.csv', index=False)
