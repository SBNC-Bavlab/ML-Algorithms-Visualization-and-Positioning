# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 16:25:08 2018

@author: ASUS
"""
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from numpy import array
import graphviz

df = pd.read_csv("data/mangal.txt", names=["Temperature", "Outlook", "Humidity", "Windy", "Play Golf?"], delimiter = " ")

df_new = df[:]
dictionaries = []
for col in range(df.shape[1] - 1):
    le = LabelEncoder()
    df_new[df.columns[col]] = le.fit_transform(df[df.columns[col]])
    dictionary = {i: val for i, val in enumerate(le.classes_.tolist())}
    dictionaries.append(dictionary)
    
X = df_new.values[:, 0:4]
Y = df_new.values[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.4, random_state = 100)
                             
clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100)
clf_gini.fit(X_train, y_train)
y_pred = clf_gini.predict(X_test)
print("Accuracy is %", accuracy_score(y_test,y_pred)*100)
graph = export_graphviz(clf_gini, out_file = None)
print(graphviz.Source(graph))