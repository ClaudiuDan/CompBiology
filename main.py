import util
import data

import xenaPython as xena

import pandas as pd

from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

import os

import time

os.environ['PATH'] = os.environ['PATH']+';'+os.environ['CONDA_PREFIX']+r"\\Library\bin\\graphviz"

DATA = data.data['RNA_expr_dis']

hub = DATA['hub']
cohort = DATA['cohort']
manual_datasets = DATA['dsets']

#print(xena.dataset_field(hub, manual_datasets[0])[:])
#print(xena.dataset_field(hub, manual_datasets[2])[:])

df = util.combine_dataset(hub, manual_datasets[0], manual_datasets[1:], 1000)

df = df.replace(to_replace='NaN', value=0)


training_features = xena.dataset_field(hub, manual_datasets[0])[:-2]
training_classes = DATA['target']

# df_copy = df
# print(df_copy[training_classes].drop_duplicates())

print("----------------------------------------")
print("Classifing:", training_classes)
print('Classes:', df[training_classes].unique())
print("----------------------------------------")

X = df[training_features]
y = df[training_classes]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)


clf = DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)



print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

util.plot_decision_tree(clf, 10, "Xena"+str(time.time()), list(
    X.columns), y.unique())
