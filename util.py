import xenaPython as xena
import numpy as np
import pandas as pd
import pickle
import graphviz
import pydotplus

from PIL import Image
from sklearn import tree
from sklearn.externals.six import StringIO


def retrieve_full_datasets(host, dataset_ids, n=None):
    """ 
    Retrieves a number of datasets

    Parameters: 
    arg1 (string): Name of the host for the datasets.
    arg2 (list): Id names of the datasets as found on Xena website
    arg3 (int): Number of samples to retrieve. Defaults to all.

    Returns: 
    list: The transposed datasets as shown on Xena in a pandas format 
    """

    panda_datasets = []
    for i in (dataset_ids):

        # getting the sample and feature names
        samples_names = xena.dataset_samples(host, i, n)
        features_names = xena.dataset_field(host, i)

        # retrieving the full dataset
        dataset = xena.dataset_fetch(host, i, samples_names, features_names)

        # transposing the data so it is in the "sample X features" format
        dataset = np.array(dataset)
        dataset = dataset.T
        print(dataset.shape)

        panda_dataset = pd.DataFrame(data=dataset,            # values
                                     index=samples_names,     # 1st column as index
                                     columns=features_names)  # 1st row as the column names

        panda_datasets.append(panda_dataset)

    return panda_datasets


def save_panda_datasets(datasets_pandas, dataset_ids):
    """ 
    Saves all the datasets to current directory for further use

    Parameters: 
    arg1 (list): Datasets in pandas format
    arg2 (list): Datasets ids as in Xena website
    """

    # saving each dataset with the
    for i in range(len(datasets_pandas)):
        filename = dataset_ids[i][:-4]
        datasets_pandas[i].to_csv(filename + ".csv")
        print("saved ", filename)


def add_cancer_type_column(dataset_ids, cancer_types):
    """ 
    Adds new column to datasets with cancer type and overides the old version to working dir

    Parameters: 
    arg1 (list): Datasets ids as on Xena website
    arg2 (list): cancer types as simple names
    """

    for i in range(len(dataset_ids)):
        filename = dataset_ids[i][:-4] + ".csv"
        dataset = pd.read_csv(filename)

        dataset['Cancer-Type'] = cancer_types[i]
        dataset.to_csv(filename, index=False)
        print("saved ", filename)


def merging_datasets(dataset_ids, name):
    """ 
    Merges the datasets saved to working dir and saves the result

    Parameters: 
    arg1 (list): Datasets ids as on Xena website
    arg2 (string): The name of the final merged dataset
    """
    datasets = []
    for i in range(len(dataset_ids)):
        filename = dataset_ids[i][:-4] + ".csv"
        dataset = pd.read_csv(filename)
        print(dataset.shape)
        datasets.append(dataset)

    merged_dataset = pd.concat(datasets)
    print(merged_dataset.shape)
    merged_dataset.to_csv(name, index=False)
    print("saved ", name)

    return merged_dataset


def get_common_samples(hub, dataset_list):
    """
    Get the names of the common samples across multiple datasets.

    :param (string) hub: The name of the hub of the datasets.
    :param (list) dtaset_list: A list of datasets.

    :return: A list of common samples.
    """
    s1 = set(xena.dataset_samples(hub, dataset_list[0], None))

    for i in dataset_list:
        s1 = s1.intersection(set(xena.dataset_samples(hub, i, None)))

    return list(s1)


def combine_dataset(hub,  primary, to_be_merged, n=None):
    """
    Merge a multiple datasets to a primary dataset based on the samples in the primary dataset.

    :param (string) hub: A string as the name of the hub for the datasets.
    :param (string) primary: A string as the name of the main dataset.
    :param (list) to_be_merged: A list of strings as the names of the datasets to be merged to the primary dataset.
    :param (int) n: Number of samples to extract from the datasets. Defaults to all.

    :return: A dataframe of with the input datasets combined along the sample name index axis.

    """

    d1_features = xena.dataset_field(hub, primary)

    d1_samples = get_common_samples(hub, [primary] + to_be_merged)
    print("Found", len(d1_samples), "common samples.")

    d1_samples = d1_samples[:n] if n is not None else d1_samples

    d1_data = xena.dataset_fetch(hub, primary, d1_samples, d1_features)

    d1_data = np.array(d1_data).T

    print("Shape of the primary dataset:", d1_data.shape)

    d1_panda = pd.DataFrame(
        data=d1_data, index=d1_samples, columns=d1_features)

    datasets = [d1_panda]

    for dset in to_be_merged:
        d2_features = xena.dataset_field(hub, dset)
        d2_data = xena.dataset_fetch(hub, dset, d1_samples, d2_features)

        d2_data = np.array(d2_data).T

        d2_panda = pd.DataFrame(
            data=d2_data, index=d1_samples, columns=d2_features)

        d1_panda = pd.merge(d1_panda, d2_panda,
                            left_index=True, right_index=True)

    return d1_panda


def plot_decision_tree(classifier, depth, name, feature_names, class_names):
    """
    Plot a decision tree using graphviz and pydotplus.

    :param (DecisionTreeClassifier) classifier: An sklearn trained decision tree.
    :param (int) depth: The max depth of the tree for the plot.
    :param (string) name: The name of the save file.
    :param (list) feature_names: A list of features used during training.
    :param (list) class_names: A list of classes used during classification.
    """

    dot_data = StringIO()
    
    tree.export_graphviz(classifier, max_depth=5, out_file=dot_data, feature_names=feature_names,
                         class_names=class_names, filled=True, rounded=True, special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

    graph.write_png(name+'.png')
