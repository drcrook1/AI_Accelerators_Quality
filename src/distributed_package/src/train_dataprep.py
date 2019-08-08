import argparse
import glob
import itertools
import json
import os

import fastavro
import joblib
import numpy as np
from ai_acc_quality.data_models.widget import Widget
from ai_acc_quality.ml.preprocessing import widget_to_input
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def extract_row(rec):
    row_data = rec['Body'].decode("utf-8")
    w:Widget = Widget.from_json(row_data)
    return widget_to_input(w)

def flatmap(func, *iterable):
    return itertools.chain.from_iterable(map(func, *iterable))

def dataprep(args):

    avro_files = list(filter(os.path.isfile, glob.glob(args.data_dir + "/" + args.data_files_filter)))
    avro_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    read_records = []
    for avro_file in avro_files:
        print("Reading {}".format(avro_file))
        with open(avro_file, "rb") as f:
            reader = fastavro.reader(f)
            max_read = args.max_read_rows - len(read_records)
            read_data = list(flatmap(extract_row, reader))[:max_read]
            read_records.extend(read_data)
        print("Read {} rows, total read {} rows".format(len(read_data), len(read_records)))
        if len(read_records) >= args.max_read_rows:
            break

    (X_train, X_test) = train_test_split(read_records, test_size=0.1, random_state=42)

    preprocessing = make_pipeline(StandardScaler())

    X_train = preprocessing.fit_transform(X_train)
    X_test = preprocessing.transform(X_test)

    print("Writing outputs to {}".format(args.output_model_dir))
    np.savez_compressed(args.output_data_dir + "/X.npz", X_train=X_train, X_test=X_test)
    joblib.dump(preprocessing, args.output_model_dir + '/preprocessing.joblib') 
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
