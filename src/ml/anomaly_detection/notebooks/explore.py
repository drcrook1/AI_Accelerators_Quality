# Databricks notebook source
STORAGE_ACCOUNT = "aiaccqualitytelcapture"
STORAGE_CONTAINER = "streamanalytics"
STORAGE_KEY = "gYSbp/joJb2CnfOqI3OkHlAj5YFV0gFQg87wrf6RmelNLvSMv9wMut1Q5axuiwHTe6J24VSlekH9q+UJgTdV4A=="
dbutils.fs.mount(
  source = "wasbs://" + STORAGE_CONTAINER + "@" + STORAGE_ACCOUNT + ".blob.core.windows.net",
  mount_point = "/mnt/telemetry",
  extra_configs = {"fs.azure.account.key." + STORAGE_ACCOUNT + ".blob.core.windows.net":STORAGE_KEY})

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

print((df.count(), len(df.columns)))

# COMMAND ----------

dbutils.fs.unmount("/mnt/telemetry")