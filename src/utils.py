import numpy as np 
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
from datetime import datetime
import itertools

'''
TODO: brush up docstrings

'''

# function to find min and argmin of nearest date_index nearest to specified date and its index
def nearest_date(date,date_list):

	min_val = min(date_list, key=lambda x: abs(x - datetime.strptime(date, '%Y-%m-%d')))

	return min_val, date_list.index(min_val)

# function that returns list of percent changes (relative to the previous period) of asset prices 
def percent_change(lst):
	return [100*(lst[i+1] - lst[i]) / lst[i] for i in range(len(lst) - 1)]

def generate_df(pfolio_obj, data_type, feature_names, periods, horizon, target_name,task_type):
	''' 
	generates cleaned up pandas dataframe
	'''

	df = pd.DataFrame()

	for (feat, period) in list(itertools.product(feature_names, periods)):
		feat_df = getattr(pfolio_obj, feat)
		df[(feat, period)] = pd.Series(data=pfolio_obj.gen_bwd_returns(feat, data_type, period), index=feat_df.index[period:])

	df[target_name] = pd.DataFrame(data=pfolio_obj.gen_fwd_returns(target_name, data_type, horizon, task_type), index=pfolio_obj.dates[:-horizon], columns=[target_name])

	# prune to make sure there are no NaNs for backward returns
	df = df.loc[df.index[max(periods)]:]
	# prune to make sure there are no NaNs for forward returns
	df = df.loc[:df.index[-(horizon + 1)]]
	return df

def magnify():
    return [dict(selector="th",
                 props=[("font-size", "7pt")]),
            dict(selector="td",
                 props=[('padding', "0em 0em")]),
            dict(selector="th:hover",
                 props=[("font-size", "12pt")]),
            dict(selector="tr:hover td:hover",
                 props=[('max-width', '200px'),
                        ('font-size', '12pt')])
			]




