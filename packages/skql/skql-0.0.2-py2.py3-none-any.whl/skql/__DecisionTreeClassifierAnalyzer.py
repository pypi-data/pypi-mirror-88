# -*- coding: utf-8 -*-
"""
Created on Sun Dec 09 14:02:03 2020


This module takes a sklearn based DecisionTreeClassifier model object and returns a string
which is explains the decision points taken by an entry passed through the model.

@author: Aditya Kumar
adityakumar3008@gmail.com
https://www.linkedin.com/in/nullp0inter/
"""

import pandas as pd
import numpy as np

__all__ = ["DecisionTreeClassifierAnalyzer"]

class DecisionTreeClassifierAnalyzer:

    def __init__(self, tree):
        self.tree = tree
        print("Classes of the tree are: ")
        print(tree.classes_)

    def fit(self, data_df, cols, id_col_name= "", score_col_name= "", actual_col_name = "" ):
        node_indicator = self.tree.decision_path(data_df[cols])
        n_nodes = self.tree.tree_.node_count
        feature = self.tree.tree_.feature
        threshold = self.tree.tree_.threshold
        leave_id = self.tree.apply(data_df[cols])
        number_of_rows = data_df.shape[0]
        
        for i in range(0, number_of_rows):
            sample_id = i
            node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                                node_indicator.indptr[sample_id + 1]]
            print("===================================================")
            if id_col_name != "" :
                print("ID is: " +str(data_df.loc[[sample_id], [id_col_name]].values))
            if score_col_name != "" :
                print("The probability value returned by the model: " +str(data_df.loc[[sample_id], [score_col_name]].values))
            if actual_col_name !="" :
                print("The Actual class of the entry is: " +str(data_df.loc[[sample_id], [actual_col_name]].values))
            print()
            print("The decision sequence is: ")
            print()
            for node_id in node_index:
                if leave_id[sample_id] == node_id:
                    continue

                if (data_df[cols].values[sample_id, feature[node_id]] <= threshold[node_id]):
                    threshold_sign = "<="
                else:
                    threshold_sign = ">"

                print("& (%s= %s) %s %s)"
                    % (
                        cols[feature[node_id]],
                        data_df[cols].values[sample_id, feature[node_id]],
                        threshold_sign,
                        threshold[node_id]))
            print()
            
            print("===================================================")