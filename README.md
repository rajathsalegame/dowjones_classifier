# Dow Jones Classifier
A pseudo-replication of Krauss et al., 2016's paper about statistical arbitrage on the S&amp;P500. 

IMPLEMENTED:

-Portfolio class for generic portfolio with returns and assets in the form of pandas dataframe
-Custom plotting functions / multiperiod return for Portfolio class
-Dataset class for preprocessing/statistics/analysis before feeding into ML algorithm
-Utility functions for general purpose use
-Preliminary scratchwork of XGBoost binary classifier on Dow Jones data from 1990 with ROC of 0.85

TODO:

-Generalization of Dataset class to handle multiple classification/regression tasks with custom target definition
-More functions for pre-ML analysis
-Reorganize modules (?) (perhaps Portfolio and Dataset classes can be merged)
-Clean up code / add better docstrings...
-More sophisticated models/more organized writeup
