# Dow Jones Classifier
A pseudo-replication of Krauss et al., 2016's paper about statistical arbitrage on the S&amp;P500-here, we apply similar methodologies to the Dow Jones.

### Implemented:

- Portfolio class for generic portfolio with returns and assets in the form of pandas dataframe
- Custom plotting functions / multiperiod return for Portfolio class
- Dataset class for preprocessing/statistics/analysis before feeding into ML algorithm
- Utility functions for general purpose use
- Preliminary scratchwork of XGBoost binary classifier on Dow Jones data from 1990 with ROC of 0.85

### To do:

- Generalization of Dataset class to handle multiple classification/regression tasks with custom target definition
- More functions for pre-ML analysis
- Reorganize modules (?) (perhaps Portfolio and Dataset classes can be merged)
- Clean up code / add better docstrings...
- More sophisticated models/more organized writeup

### Notes:

The conda environment used to develop this project can be found in `requirements.txt`. To install from this list, do the following:

```bash
conda create -n yourenv pip
pip install -r requirements.txt
```

If, for whatever bizarre reason, you want to use this highly, highly (I repeat, highly) experimental and non-error safe code, simply navigate to the directory you wish and do the following in your terminal (if you're using bash):

```bash
git clone https://github.com/rajathsalegame/dowjones_classifier.git
export PYTHONPATH=$(pwd)/src:$PYTHONPATH
```

This is just a temporary and probably highly unoptimal solution; if I think it's interesting and fun to develop this further, I might try and develop this into a more rigorous software package.

