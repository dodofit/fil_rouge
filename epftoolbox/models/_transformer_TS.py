print("Starting making prediction")

import torch
import pandas as pd
from datasets import Dataset
from transformers import TimeSeriesTransformerConfig, TimeSeriesTransformerModel, TimeSeriesTransformerForPrediction

device = torch.device("cuda:2" if torch.cuda.is_available() else "cpu")
context =720

df = pd.read_csv("/home/infres/dfitton-21/pfr/fil_rouge/examples/datasets/EPEX_FR 2.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Hour of the day'] = df['Date'].dt.hour
df['Day of the week'] = df['Date'].dt.dayofweek
df['Day of the year'] = df['Date'].dt.dayofyear
df['Year'] = df['Date'].dt.year
df['Month of the year'] = df['Date'].dt.month
print(df.head())

nb_time_feat = 7

dataset = Dataset.from_pandas(df)

dataset = dataset.map(lambda x: {'Day of the week': x['Date'].dayofweek})
dataset = dataset.map(lambda x: {'Hour of the day': x['Date'].hour})
dataset = dataset.map(lambda x: {'Day of the year': x['Date'].dayofyear})
dataset = dataset.map(lambda x: {'Year': x['Date'].year})
dataset = dataset.map(lambda x: {'Month of the year': x['Date'].month})


train_dataset = dataset.filter(lambda x: x['Date'].year < 2021)
test_dataset = dataset.filter(lambda x: x['Date'].date() == pd.to_datetime('2021-01-01').date())

date = train_dataset['Date'][24*context].date()

past_values_all = train_dataset.filter(lambda x: x['Date'].date() < date)
past_observed_mask = torch.ones(24*context).reshape(1, -1)
#past_observed_mask[-24:,-1] = 0
past_time_features = torch.tensor(list(zip(past_values_all['Day of the week'], past_values_all['Hour of the day'],past_values_all['Day of the year'], past_values_all['Year'], past_values_all['Month of the year'] ,past_values_all['Load forecast'], past_values_all['Generation forecast']))).reshape(1, -1, nb_time_feat)
past_values = torch.tensor(past_values_all['Price']).reshape(1, -1) 



future_values_all = train_dataset.filter(lambda x: x['Date'].date() == date)
future_values = torch.tensor(future_values_all['Price']).reshape(1, -1)

future_time_features = torch.tensor(list(zip(future_values_all['Day of the week'], future_values_all['Hour of the day'], future_values_all['Day of the year'], future_values_all['Year'], future_values_all['Month of the year'],future_values_all['Load forecast'], future_values_all['Generation forecast']))).reshape(1, -1, nb_time_feat)



#number_of_days =0
#for i in range(number_of_days):
#date = date + pd.Timedelta(hours=24)
#past_values_all_2 = train_dataset.filter(lambda x: date - pd.Timedelta(days = context) <= x['Date'].date() < date)
#past_observed_mask_temp = torch.ones(24*context)
#past_observed_mask=torch.cat((past_observed_mask, past_observed_mask_temp), dim=0)#.reshape(i+3, 24*context, nb_time_feat)
#past_time_features = torch.cat((past_time_features, torch.tensor(list(zip(past_values_all_2['Day of the week'], past_values_all_2['Hour of the day'],past_values_all_2['Day of the year'], past_values_all_2['Year'], past_values_all_2['Month of the year'], past_values_all_2['Load forecast'], past_values_all_2['Generation forecast'])))))#.reshape(i+3, 24*16, 2)
#past_values = torch.cat((past_values, torch.tensor(past_values_all_2['Price'])))#.reshape(i+3, 24*context, 3)

#future_values_all_2 = train_dataset.filter(lambda x: x['Date'].date() == date)
#future_values = torch.cat((future_values, torch.tensor(future_values_all_2['Price'])))#.reshape(i+3, 24, nb_time_feat)
#future_time_features = torch.cat((future_time_features, torch.tensor(list(zip(future_values_all_2['Day of the week'], future_values_all_2['Hour of the day'],future_values_all_2['Day of the year'], future_values_all_2['Year'], future_values_all_2['Month of the year'], future_values_all_2['Load forecast'], future_values_all_2['Generation forecast'])))))#.reshape(i+3, 24, 2)

#past_values = past_values.reshape(number_of_days+1, 24*context)
#past_time_features = past_time_features.reshape(number_of_days+1, 24*context, nb_time_feat)
#past_observed_mask = past_observed_mask.reshape(number_of_days+1, 24*context)

#future_values = future_values.reshape(number_of_days+1, 24)
#future_time_features = future_time_features.reshape(number_of_days+1, 24, nb_time_feat)
print(past_time_features.shape)
print(past_values.shape)
print(past_observed_mask.shape)

print(future_time_features.shape)
print(future_values.shape)

past_values = past_values.to(device)
past_time_features = past_time_features.to(device)
past_observed_mask = past_observed_mask.to(device)
future_values = future_values.to(device)
future_time_features = future_time_features.to(device)




# Initializing a Time Series Transformer configuration with 24 time steps for prediction
configuration = TimeSeriesTransformerConfig(prediction_length=24, context_length=24*(context-1)+17, input_size=1, output_size=1, num_time_features=nb_time_feat )

# Randomly initializing a model (with random weights) from the configuration
model = TimeSeriesTransformerForPrediction(configuration)

# Accessing the model configuration
configuration = model.config

model = model.to(device)



# during training, one provides both past and future values
# as well as possible additional features
outputs = model(
    past_values=past_values,
    past_time_features=past_time_features,
    past_observed_mask=past_observed_mask,
    future_values=future_values,
    future_time_features=future_time_features
)

loss = outputs.loss
loss.backward()

# during inference, one only provides past values
# as well as possible additional features
# the model autoregressively generates future values
outputs = model.generate(
    past_values=past_values,
    past_time_features=past_time_features,
    past_observed_mask=past_observed_mask,
    future_time_features=future_time_features
)

mean_prediction = outputs.sequences.mean(dim=1).detach().cpu()
df_pred = pd.DataFrame(mean_prediction.numpy())

df_pred.to_csv('/home/infres/dfitton-21/pfr/fil_rouge/forecasts/transformer_pred.csv')