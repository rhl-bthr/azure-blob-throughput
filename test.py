from azure.storage.blob import AppendBlobService
import argparse
from datetime import datetime
import os
import sys
import json

TIME_TAKEN = []

STORAGE_ACCOUNT_NAME = "<STORAGE_ACCOUNT_NAME>"
STORAGE_ACCOUNT_KEY = "<STORAGE_ACCOUNT_KEY>"
CONTAINER_NAME = "<CONTAINER_NAME>"
BLOB_NAME = "<BLOB_NAME>"



parser = argparse.ArgumentParser(description='Measuring Azure Blob write Throughput')

parser.add_argument('--iters', '-i', type=int, help='Number of iterations to run for this experiment', default = 20)
parser.add_argument('--data_size', '-d', type=int, help='Data size to be sent in each experiment (in MB)', default = 1024)
parser.add_argument('--chunk_size', '-c', type=int, help='Chunk size to sent in each request (in MB)', default = 4)
parser.add_argument('--temp_file_name', '-t', type=str, help='Name of the temporary file to be sent', default = "data-file")
parser.add_argument('--experiment_name', '-e', type=str, help='Experiment configuration name', default = "default")

args = parser.parse_args()

os.system("head -c " + str(args.chunk_size) + "M </dev/urandom > " + args.temp_file_name)
file_content = open(args.temp_file_name, "rb").read()

service = AppendBlobService(account_name=STORAGE_ACCOUNT_NAME, 
            account_key=STORAGE_ACCOUNT_KEY)
try:
    service.create_blob(container_name=CONTAINER_NAME, blob_name=BLOB_NAME, if_none_match="*")
except:
    pass
inner_iters = int(args.data_size/args.chunk_size)

for i in range(args.iters):
    start_time = datetime.now()
    for i in range(inner_iters):
        service.append_block(container_name=CONTAINER_NAME, blob_name=BLOB_NAME, block = file_content)
    end_time = datetime.now()

    time_diff = int((end_time - start_time).total_seconds() * 1000)
    TIME_TAKEN.append(time_diff)
os.system("rm " + args.temp_file_name)

average_time = sum(TIME_TAKEN)/len(TIME_TAKEN)
throughput = (args.data_size / average_time)*1000
print("Average bandwidth:", throughput, "MB/s")

results = {}
results["config"] = args.experiment_name
results["times"] = TIME_TAKEN
results["data_size"] = args.data_size
results["chunk_size"] = args.chunk_size
results["iters"] = args.iters
results["average"] = average_time
results["throughput"] = throughput
json.dump(results, open("results/" + args.experiment_name + ".json", "w"), indent = 4)
