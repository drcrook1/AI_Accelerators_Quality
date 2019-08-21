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

df = spark.read.option("multiline", "true").json(files[0][5:])
display(df)

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

from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.utils import plot_model

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
plot_model(model, show_shapes=True, to_file='reconstruct_lstm_autoencoder.png')
# demonstrate recreation
yhat = model.predict(sequence, verbose=0)
print(yhat[0,:,0])

# COMMAND ----------

dbutils.fs.unmount("/mnt/telemetry")