import requests
import pandas 
import time 
import datetime as dt
import pandas as pd

token = 'NDcxNTY0ZmEtOGNjZC00ZDY1LTg4ZjUtNDgwNGMyMDk1M2ZjOjNlNDcyZmQ0LWI2NDAtNDE1ZC05YjhmLWQ4ZjI2N2YyNDMzYw=='

#
url = 'https://digital.iservices.rte-france.com/token/oauth/'

data = {
    'Authorization' : 'Basic NDcxNTY0ZmEtOGNjZC00ZDY1LTg4ZjUtNDgwNGMyMDk1M2ZjOjNlNDcyZmQ0LWI2NDAtNDE1ZC05YjhmLWQ4ZjI2N2YyNDMzYw==',
    'Content-Type' : 'application/x-www-form-urlencoded'
}
response = requests.post(url, headers=data)
status_code = response.status_code
if status_code == 200:
    infos_rte_token = response.json()
    token = infos_rte_token['access_token']
    print(f'token = {token}')
else:
    print(f"API request failed with status_code: {status_code}")


end_date = str(dt.datetime.today())
start_date = str(dt.datetime.today() - dt.timedelta(days=365*4))
print(start_date, end_date)


endpoint_gen = f'https://digital.iservices.rte-france.com/open_api/generation_forecast/v2/forecasts?\
    production_type=<valeur(s)>&\
    type=<valeur(s)>&\
    start_date=<{start_date}>&\
    end_date=<{end_date}>'

data = {
    'Authorization' : 'Bearer ' + token ,
    'Content-Type' : 'application/soap+xml',
    'charset' : 'UTF-8'
}

response = requests.get(endpoint_gen, headers=data)
status_code = response.status_code
print(status_code)
infos_rte_data_gen_json = response.json()
data = infos_rte_data_gen_json['forecasts']
df_data = pd.DataFrame(data=data)

print(f'gen data : {df_data}')