from azure.storage.blob import AppendBlobService
from datetime import datetime
import os
import sys
import json

NUM_ITERS = 20 # Number of iterations to run for this experiment
FILE_SIZE = 1024 # File size to send in each iteration (in MB)
DATA_FILE_NAME = "data-file" # Name of the temporary file that gets created to send
CONFIG = "default" # Result 

if len(sys.argv) > 1:
    CONFIG = sys.argv[1]
TIME_TAKEN = []

STORAGE_ACCOUNT_NAME = "<STORAGE_ACCOUNT_NAME>"
STORAGE_ACCOUNT_KEY = "<STORAGE_ACCOUNT_KEY>"
CONTAINER_NAME = "<CONTAINER_NAME>"
BLOB_NAME = "<BLOB_NAME>"

def append_files_to_blob():
    service = AppendBlobService(account_name=STORAGE_ACCOUNT_NAME, 
            account_key=STORAGE_ACCOUNT_KEY)
    try:
        service.append_blob_from_path(container_name=CONTAINER_NAME, blob_name=BLOB_NAME, file_path = DATA_FILE_NAME)
    except:
        service.create_blob(container_name=CONTAINER_NAME, blob_name=BLOB_NAME)
        service.append_blob_from_path(container_name=CONTAINER_NAME, blob_name=BLOB_NAME, file_path = DATA_FILE_NAME)

os.system("head -c " + str(FILE_SIZE) + "M </dev/urandom > " + DATA_FILE_NAME)
for i in range(NUM_ITERS):
    start_time = datetime.now()
    append_files_to_blob()
    end_time = datetime.now()

    time_diff = int((end_time - start_time).total_seconds() * 1000)
    print("Iter", i, "time taken:", time_diff)
    TIME_TAKEN.append(time_diff)
os.system("rm " + DATA_FILE_NAME)

average_time = sum(TIME_TAKEN)/len(TIME_TAKEN)
print("Average time:", average_time)
print("Average bandwidth:", (FILE_SIZE / average_time)*1000, "MB/s")

results = {}
results["config"] = CONFIG
results["times"] = TIME_TAKEN
results["size"] = FILE_SIZE
results["iters"] = NUM_ITERS
results["average"] = average_time
json.dump(results, open("results/" + CONFIG + ".json", "w"), indent = 4)
