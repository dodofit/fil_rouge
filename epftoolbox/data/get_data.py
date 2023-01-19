from entsoe import EntsoePandasClient
import pandas as pd
import pytz

client = EntsoePandasClient(api_key="4e524938-86d0-4232-81a9-4c2aaf8cdceb")

country_code_FR = 'FR'
country_code_BE = 'BE'

timezone_FR = 'Europe/Paris'
timezone_BE = 'Europe/Brussels'

start_date = pd.to_datetime('2017-01-01 01:00:00')
end_date = pd.to_datetime('2023-01-01 01:00:00')

# The EPEX-BE market
"""The two exogenous data series represent the day-ahead load 
forecast and the day-ahead generation forecast in France"""

exogenous_1_BE = client.query_load_forecast(country_code = country_code_BE, 
                                            start = start_date.tz_localize(timezone_BE), 
                                            end = end_date.tz_localize(timezone_BE))

exogenous_2_BE = client.query_generation_forecast(country_code = country_code_FR, 
                                                  start = start_date.tz_localize(timezone_BE), 
                                                  end = end_date.tz_localize(timezone_BE))

prices_BE = client.query_day_ahead_prices(country_code = country_code_BE, 
                                          start = start_date.tz_localize(timezone_BE), 
                                          end = end_date.tz_localize(timezone_BE))

exogenous_1_BE = exogenous_1_BE.loc[exogenous_1_BE.index.minute == 0]
exogenous_1_BE = exogenous_1_BE.squeeze()

exogenous_1_BE = exogenous_1_BE[:-1]
exogenous_2_BE = exogenous_2_BE[:-1]
prices_BE = prices_BE[:-1]

df_BE = pd.DataFrame(data = {'Load forecast': exogenous_1_BE, 
                             'Generation forecast': exogenous_2_BE, 
                             'Price': prices_BE})

df_BE.index.names = ['Date']

df_BE.index = df_BE.index.tz_convert(pytz.FixedOffset(0))

df_BE.to_csv('EPEX_BE.csv', sep=',', index=True)


# The EPEX-FR market
"""The two exogenous data series represent the day-ahead load 
forecast and the day-ahead generation forecast"""

exogenous_1_FR = client.query_load_forecast(country_code = country_code_FR, 
                                            start = start_date.tz_localize(timezone_FR), 
                                            end = end_date.tz_localize(timezone_FR))

exogenous_2_FR = client.query_generation_forecast(country_code = country_code_FR, 
                                                  start = start_date.tz_localize(timezone_FR), 
                                                  end = end_date.tz_localize(timezone_FR))

prices_FR = client.query_day_ahead_prices(country_code = country_code_FR, 
                                          start = start_date.tz_localize(timezone_FR), 
                                          end = end_date.tz_localize(timezone_FR))

exogenous_1_FR = exogenous_1_FR.loc[exogenous_1_FR.index.minute == 0]
exogenous_1_FR = exogenous_1_FR.squeeze()

exogenous_1_FR = exogenous_1_FR[:-1]
exogenous_2_FR = exogenous_2_FR[:-1]
prices_FR = prices_FR[:-1]

df_FR = pd.DataFrame(data = {'Load forecast': exogenous_1_FR, 
                             'Generation forecast': exogenous_2_FR, 
                             'Price': prices_FR})

df_FR.index.names = ['Date']

df_FR.index = df_FR.index.tz_convert(pytz.FixedOffset(0))

df_FR.to_csv('EPEX_FR.csv', sep=',', index=True)