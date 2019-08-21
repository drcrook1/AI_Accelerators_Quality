# Databricks notebook source
try:
  STORAGE_ACCOUNT = "aiaccqualitytelcapture"
  STORAGE_CONTAINER = "streamanalytics"
  STORAGE_KEY = "gYSbp/joJb2CnfOqI3OkHlAj5YFV0gFQg87wrf6RmelNLvSMv9wMut1Q5axuiwHTe6J24VSlekH9q+UJgTdV4A=="
  dbutils.fs.mount(
    source = "wasbs://" + STORAGE_CONTAINER + "@" + STORAGE_ACCOUNT + ".blob.core.windows.net",
    mount_point = "/mnt/telemetry",
    extra_configs = {"fs.azure.account.key." + STORAGE_ACCOUNT + ".blob.core.windows.net":STORAGE_KEY})
except Exception:
  print("already mounted.")

# COMMAND ----------

import os
def get_avros_file_list():
  file_paths = []
  for root, dirs, files in os.walk("/dbfs/mnt/telemetry"):
    if(len(files) >0):
      for file in files:
        path = os.path.join(root, file)
        print(path)
        file_paths.append(path)
  return file_paths

files = get_avros_file_list()
print("files found: {}".format(len(files)))

# COMMAND ----------

data = spark.read.option("multiline", "true").json(files[0][5:])
for file in files[1:]:
  try:
    df = spark.read.option("multiline", "true").json(file[5:])
    data = data.union(df)
  except Exception as e:
    print("failed on file: {}".format(file))
print(data.count())

# COMMAND ----------

print(data.count())
display(data)

# COMMAND ----------

n_samples = data.count()
telemetry_keys = list(data.collect()[0]["telemetry"][0].asDict().keys())
telemetry_keys.remove("time_stamp")
telemetry_keys.sort()
print(telemetry_keys)

feature_keys = list(data.collect()[0]["features"].asDict().keys())
feature_keys.sort()
print(feature_keys)

# COMMAND ----------

row = data.collect()[0]

# COMMAND ----------

import numpy as np

def prep_row_telemetry_ml(row, telemetry_keys):
  """
  telemetry keys must be a sorted list.
  """
  print("starting")
  sorted_tel_seq = sorted(row["telemetry"], key = lambda i: i["time_stamp"])
  n_steps = len(sorted_tel_seq)
  n_vars = len(telemetry_keys)
  print(n_steps)
  print(n_vars)
  tel_data = np.empty((n_steps, n_vars))
  for i in range(0,n_steps):
    for j in range(0,n_vars):
      tel_data[i,j] = sorted_tel_seq[i][telemetry_keys[j]]
  return tel_data

def prep_feature_ml(row, feature_keys):
  """
  feature keys must be a sorted list
  """
  n_vars = len(feature_keys)
  feature_data = np.empty((n_vars))
  for i in range(0,n_vars):
    feature_data[i] = row["features"][feature_keys[i]]
  return prep_feature_ml
  

tel_data = prep_row_telemetry_ml(row, telemetry_keys)
print(tel_data)
print(row["telemetry"])


# COMMAND ----------

display(data)

# COMMAND ----------

def get_unique_features(data, feature_keys):
  unique_features = {}
  for feature in feature_keys:
    unique_features[feature] = [row[0] for row in data.select(col("features").getItem(feature)).distinct().collect()]
  return unique_features

u_features = get_unique_features(data, feature_keys)
print(u_features)

# COMMAND ----------

from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed

# COMMAND ----------

sequence = array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
# reshape input into [samples, timesteps, features]
n_in = len(sequence)
sequence = sequence.reshape((1, n_in, 1))
# define model
model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(n_in,1)))
model.add(RepeatVector(n_in))
model.add(LSTM(100, activation='relu', return_sequences=True))
model.add(TimeDistributed(Dense(1)))
model.compile(optimizer='adam', loss='mse')
# fit model
model.fit(sequence, sequence, epochs=300, verbose=0)
# demonstrate recreation
yhat = model.predict(sequence, verbose=0)
print(yhat[0,:,0])

# COMMAND ----------

sequence = array([0.1, 0.2, 0.3, 0.4, 7.5, 0.6, 0.7, 0.8, 0.9]).reshape(1,n_in,1)
model.predict(sequence, verbose=0)

# COMMAND ----------

dbutils.fs.unmount("/mnt/telemetry")