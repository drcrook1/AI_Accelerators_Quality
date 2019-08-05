import argparse
import glob
import json
import os

import fastavro
import pandas as pd
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def extract_row(rec):
    return {"telemetry":json.loads(rec['Body'].decode("utf-8"))['telemetry']}


def dataprep(args):

    avro_files = list(filter(os.path.isfile, glob.glob(args.data_dir + "/" + args.data_files_filter)))
    avro_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    remaining = args.max_read_rows
    read_records = None
    for avro_file in avro_files:
        print("Reading {}".format(avro_file))
        with open(avro_file, "rb") as f:
            reader = fastavro.reader(f)
            data = pd.DataFrame.from_records(list(map(extract_row, reader))[:remaining])
            data = data.explode("telemetry")
            data = pd.DataFrame.from_records(data.telemetry)
            data = data.drop("time_stamp", axis=1)
            if read_records is None:
                read_records = data
            else:
                read_records = read_records.append(data)
            remaining -= len(data)
        print("Read {} rows, total read {} rows".format(len(data), len(read_records)))
        if remaining <= 0:
            break

    (X_train, X_test) = train_test_split(read_records, test_size=0.1, random_state=42)

    preprocessing = make_pipeline(StandardScaler())

    X_train = pd.DataFrame(preprocessing.fit_transform(X_train.values), columns=X_train.columns, index=X_train.index)
    X_test = pd.DataFrame(preprocessing.transform(X_test.values), columns=X_test.columns, index=X_test.index)

    print("Writing outputs to {}".format(args.output_model_dir))
    X_train.to_pickle(args.output_data_dir + "/X_train.pkl.gz")
    X_test.to_pickle(args.output_data_dir + "/X_test.pkl.gz")
    dump(preprocessing, args.output_model_dir + '/preprocessing.joblib') 
    print("Completed writing outputs")


def main():
    # get command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default=".", help='data directory')
    parser.add_argument('--data_files_filter', type=str, default="*.avro", help='filter for Avro files in data_dir')
    parser.add_argument('--max_read_rows', type=int, default=100000, help='number of Avro telemetry rows to read (most recent first)')
    parser.add_argument('--output_model_dir', type=str, default="./outputs", help='output directory')
    parser.add_argument('--output_data_dir', type=str, default="./outputs", help='output directory')
    args = parser.parse_args()
    os.makedirs(args.output_model_dir, exist_ok=True)
    os.makedirs(args.output_data_dir, exist_ok=True)
    dataprep(args)


if __name__ == "__main__":
    main()
