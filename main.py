import numpy as np
import pandas as pd

from random import sample
from datetime import datetime
from prepare_data import *
from pu_bagging import pu_bagging


if __name__ == "__main__":
    # Reads data
    devices = custom_read_csv("data/data1.csv")
    df = pd.read_csv("data/data2.csv", delimiter=";")
    test = pd.read_excel("data/data3.csv", delimiter=";", header=None)
    test.columns = ["a", "b"]
    # Extracts time features
    df["datetime"] = df["tstamp"].apply(
        lambda x: datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))
    df["date"] = df["datetime"].apply(lambda x: str(
        datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date()))
    df["hour"] = df["datetime"].apply(
        lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)
    # Joins movement data with devices
    df["id1"] = df["id2"].apply(lambda x: str(x)[:8])
    df = df.merge(devices, on='tac')

    # Gets features for positive and unlabeled data
    test_df = get_test_data(test)
    numbers = df["id3"].unique()
    numbers_sample = sample(numbers, 500)
    unlabeled_df = get_unlabeled_data(df, phones_sample)

    # Remove accidental test data from unlabeled data
    intersection = set(final_df["phone1"]).intersection(test_df["phone1"])
    unlabeled_df = unlabeled_df[~unlabeled_df["phone1"].isin(intersection)]
    # Gets class probabilities for each unlabeled example
    unlabeled_df["proba"] = pu_bagging(test_df, unlabeled_df)
    # Gets person data and writes to .txt
    person_df = get_person_data(unlabeled_df)
    person_df.to_csv("person.txt")
