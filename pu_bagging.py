import numy as np

from random import sample
from sklearn.tree import DecisionTreeClassifier


def pu_bagging(positive_df, unlabeled_df, num_estimators=1000):
    """
    Perform PU bagging on supplied positive andd unlabeled data

    Parameters
    ----------
    positive_df : dataframe
        Dataframe of positively labeled examples
    unlabeled_df : dataframe
        Dataframe of unlabeled examples
    num_estimators : int
        Number of estimators

    Returns
    -------
    List of class probabilities for unlabeled examples
    """
    num_positive = positive_df.shape[0]
    num_unlabeled = unlabeled_df.shape[0]

    K = num_positive
    # Keeping track of positive and unlabeled indices
    train_label = np.zeros(shape=(num_positive+K, ))
    train_label[:num_positive] = 1.0

    # How many times the record was OOB
    num_oob = np.zeros(shape=(num_unlabeled, ))
    # Sum of the record's OOB score
    sum_oob = np.zeros(shape=(num_unlabeled, 2))

    for i in range(num_estimators):
        # Get a bootstrap sample of unlabeled points for this round
        bs = np.random.choice(np.arange(num_unlabeled), replace=True, size=K)

        # Find the OOB data points for this round
        idx_oob = sorted(set(range(num_unlabeled)) - set(np.unique(bs)))

        # Get the training data (ALL positives and the bootstrap
        # sample of unlabeled points) and build the tree
        data = np.concatenate(
            (positive_df.values, unlabeled_data.values[bs, :]), axis=0)
        model = DecisionTreeClassifier(
            max_depth=None,
            max_features=None,
            criterion='gini',
            class_weight='balanced'
        )
        model.fit(data, train_label)
        # Record the OOB scores from this round
        sum_oob[idx_oob] += model.predict_proba(unlabeled_data.values[idx_oob])
        num_oob[idx_oob] += 1
    # Final scores
    predict_proba = sum_oob[:, 1] / num_oob
    return predict_proba
