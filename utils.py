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

def generate_df(pfolio_obj, data_type, feature_names, periods,target_name,thresh=0.25):
	''' 
	generates cleaned up pandas dataframe
	'''

	df = pd.DataFrame()

	for (feat, period) in list(itertools.product(feature_names, periods)):
		feat_df = getattr(pfolio_obj, feat)
		df[(feat, period)] = pd.Series(data=pfolio_obj.gen_returns(feat, data_type, period), index=feat_df.index[period:])

	df[target_name] = pd.DataFrame(data=pfolio_obj.gen_classes(target_name, data_type), index=pfolio_obj.dates[1:], columns=[target_name])

	# # drop columns where there are more than 25% values missing
	# df = df.dropna(axis='columns',thresh=0.25*len(df.index))

	# # drop rows for which there are any values missing
	# df = df.dropna(how='any')

	df = df.loc[df.index[max(periods)]:]

	df = df.dropna(axis='columns',thresh=0.25*len(df.index))

	return df




