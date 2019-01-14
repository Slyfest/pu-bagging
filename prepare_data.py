import numpy as np
import pandas as pd


def custom_read_csv(path):
    """
    Custom file reader to overcome some issues with personal machine.
    In other cases, pd.read_csv should do.
    """
    data = []
    for line in open(path, "r").readlines()[1:]:
        values = line.split(",")
        data.append(dict(
            tac=values[0][1:],
            vendor=values[1][2:-2],
            platform=values[2][2:-2],
            type=values[3][2:-4]
        ))
    df = pd.DataFrame.from_records(data)
    return df


def get_mutual_data(df, a, b):
    """
    Extract features for the supplied id pair

    Parameters
    ----------
    df : Dataframe
        Input data
    a : int
        First id
    b : int
        Second id

    Returns
    -------
    Dict with extracted features
    """

    # Initializing feature dict
    features = dict(
        a=0,
        b=0,
        lat1=0,
        long1=0,
        lat2=0,
        long2=0,
        location_equals=0,
    )

    # Extracts subsets for each msisdn
    df1 = df[df["a"] == a]
    df2 = df[df["b"] == b]
    # Writes numbers into feature dict
    features["a"] = a
    features["b"] = b

    counter = 1
    # Iterates over date to only match relevant locations
    for date in set(df1["date"]):
        for i, row in df1[df1["date"] == date].iterrows():
            # Writes coordinates of first msisdn into feature dict
            lat = row["lat"]
            long = row["long"]

            features["lat1"] = lat
            features["long1"] = long
            # Iterates over values of the second msisdn for the same date
            for i, row2 in df2[df2["date"] == date].iterrows():
                lat2 = row2["lat"]
                long2 = row2["long"]
                # Writes coordinates of second msisdn into feature dict
                features["lat2"] = lat2
                features["long2"] = long2

                # Checks for exact match in coordinates
                if lat == lat2 and long == long2:
                    # Write matched coordinates into feature dict
                    features["lat2"] = lat2
                    features["long2"] = long2
                    features["location_equals"] += 1
                counter += 1
    # Divides incremental features by counter to normalize output data
    features["location_equals"] /= float(counter)
    return features


def get_person_data(df):
    """
    Return pairs matched by highest probability with p >= 0.5

    Parameters
    ----------
    df : Dataframe
        Dataframe with predicted target

    Returns
    -------
    Dataframe with candidate msisdn pairs
    """
    person_data = []
    for i, a in enumerate(sorted(df["a"].unique())):
    subset = unlabeled_data[unlabeled_data["a"]
                            == a].sort_values(["proba"], ascending=False)
    if subset["proba"].values[0] >= 0.5:
        b = subset["b"].values[0]
        person_data.append(dict(
            a=a
            b=b
        ))
    else:
        pass

    person_df = pd.DataFrame.from_records(person_data)
    return person_df

    person_df.to_csv("person.txt")


def get_test_data(raw_test):
    """
    Get features for test records

    Parameters
    ----------
    raw_test: dataframe
        Raw test dataframe

    Returns
    -------
    Test Dataframe with extracted features
    """
    test_data = []
    # Iterates over test records
    for i, row in test.iterrows():
        # gets features for corresponding msisdn pair
        record = get_mutual_data(row["a"], row["b"])
        test_data.append(record)

    test_df = pd.DataFrame.from_records(test_data)
    return test_df


def get_unlabeled_data(df, numbers_sample):
    """
    Match each number against rest numbers, and extract features for each pair

    Parameters
    ----------
    df: dataframe
        Input data
    numbers_sample : List[int]
        List of sample numbers to process

    Returns
    -------
    Dataframe with features for unlabeled id pairs

    """
    data = []
    counter = 0
    for a in numbers_sample:
        rest = [value for value in numbers_sample if value != a]
    for b in rest:
        record = get_mutual_data(df, a, b)
        data.append(record)
    counter += 1
    print("phone processed, {} phones left".format(
        len(numbers_sample) - counter))

    unlabeled_df = pd.DataFrame.from_records(data)
    return unlabeled_df
