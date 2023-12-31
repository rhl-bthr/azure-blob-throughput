# Azure Blob Throughput tests
Scripts to test thoughput offered by Azure blob storage.

## Setup
1. Create an Azure Virtual Machine(s) and run the following commands,
```
pip install azure.core
pip install azure-storage-blob==2.1.0
git clone https://github.com/rhl-bthr/azure-blob-throughput
```

2. Create an Azure Storage Account and a container within, and configure `STORAGE_ACCOUNT_NAME`, `STORAGE_ACCOUNT_KEY`, `CONTAINER_NAME`, `BLOB_NAME` in `main.py`.

## Usage
```
python3 main.py <config_name>
```
Results are stored in `results/`.
Configurable parameters include `NUM_ITERS`, `FILE_SIZE`, `DATA_FILE_NAME`, `CONFIG`

## Experiments
To run multiple processes on different cores, use
```
num_threads=5 # can be varied
x=0
while [ $x -lt $num_threads ]
do
    taskset -c $x python3 test.py --temp_file_name=data-file-$x --experiment_name=$num_threads-thread-$x &
    x=$(( $x + 1 ))
done
```
