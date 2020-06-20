import numpy as np 
import matplotlib.pyplot as plt
import os
import pandas as pd
import yfinance as yf
from datetime import datetime
from scipy import stats
from utils import *

class Portfolio:
	'''
	constructs class representing a portfolio of securities and associated returns

	attributes:
		nassets (int):
		period (str):
		returns (pandas df):
		sec (pandas df)
		data_types (list)
	'''

	def __init__(self,name,assets,returns,start,end):
		'''
		args:
			assets (list):
			returns (pandas df):
			period (str):
			sec (pandas df):
			data_types (list):	
			index_by_date (bool):
		'''
		self.name = name
		self.nassets = len(assets)
		self.returns = returns
		self.assets = assets
		for asset in assets:
			setattr(self, asset, yf.Ticker(asset).history(start=start,end=end))
		self.data_types = list(returns.columns)
		self.dates = list(returns.index)
		self.ndates = len(self.dates)

	def price_plot(self, assets,data_type,start,end,plot_type=None):
		'''
		args:
			TODO, same as above pretty much

		return:
			ax object for plotting
		'''

		assert(data_type in self.data_types), "the data_type you have chosen is not available for analysis."

		fig, ax = plt.subplots()

		for asset in assets:
			assert(asset in self.assets or asset == 'returns'), "the asset you have chosen is not in the portfolio."

			df = getattr(self, asset)
		
			col_data = df[data_type].tolist()

			if plot_type == 'pct_change':
				col_data = percent_change(col_data)

			start_date, start_idx = nearest_date(start, self.dates)
			end_date, end_idx = nearest_date(end, self.dates)
			if asset != 'returns':
				ax.plot(self.dates[start_idx:end_idx],col_data[start_idx:end_idx],label=f'{asset}',linewidth=0.5)
			else:
				ax.plot(self.dates[start_idx:end_idx],col_data[start_idx:end_idx],label=f'{self.name}',linewidth=0.5)

		ax.legend()
		ax.set_xlabel('Date')
		if plot_type == 'pct_change':
			ax.set_ylabel('Percent change in USD (%)')
		else:
			ax.set_ylabel('Price per share (USD)')

		return ax 

	def gen_returns(self, asset, data_type, period):
		'''
		generates np.array of price process of given asset over the defined number of periods for the given data type

		args:
			asset (str): the asset (in this case a stock) for which price process is constructed
			data type (str): denotes data type of prices (open, high, low, close)
		
		return:
			np.array of dates and corresponding return over num_periods
		'''

		df = getattr(self, asset)
		data = df[data_type].to_numpy()

		return np.array([data[i] / data[i - period] - 1 if data[i] != 0 and data[i - period] != 0 else 0 for i in range(period, len(data)) ])

	def gen_classes(self, asset, data_type):
		'''
		generates binary classes based on underlying portfolio's movement from day before (increase from day before = 1, decrease from day before = 0)

		args:
			asset (str): the asset for which classes are constructed
			data type (str): data type of prices

		return:
			np.array of 1s and 0s
		'''
		df = getattr(self, asset)
		data = df[data_type].to_numpy()

		df = getattr(self, asset)
		data = df[data_type].to_numpy()

		return np.array([int(data[i] / data[i - 1] - 1 >= 0) if data[i] != 0 and data[i - 1] != 0 else 0 for i in range(1,len(data)) if data[i - 1] != 0])

class Dataset:
	'''
	base class for data that will be loaded into the models and used for analysis

	designed to be flexible with respect to feature selection, return periods, target selection, and number of classes

	default behavior turns off numpy mode to save memory in case of large datsets...can be turned on by accessing class method
	'''
	def __init__(self, pfolio_obj, data_type, feature_names, periods, target_name, numpy_mode=False):
		self.df = generate_df(pfolio_obj, data_type, feature_names, periods, target_name)
		self.data_type = data_type
		self.n_samples = len(self.df.index)
		self.n_features = len(self.df.columns)
		self.n_classes = len(np.unique(self.df[target_name].to_numpy()))
		self.data = self.df.drop(target_name,axis=1)
		self.target = self.df[target_name]

		if numpy_mode:
			self.data = self.data.to_numpy()
			self.target = self.target.to_numpy()
	
	def numpy_mode(self):
		self.data = self.data.to_numpy()
		self.target = self.data.to_numpy()

	def statistics(self,features = 'all', ret_type='pandas'):
		''' 
		returns pandas df or dict of desired summary statistics for given features using pandas and scipy.stats module
		'''

		if features == 'all':
			df_stats = self.data.describe()
		else:
			df_stats = self.df[feature_names].describe()

		df_stats.loc['var'] = self.data.var()
		df_stats.loc['kurtosis'] = self.data.kurtosis()
		df_stats.loc['skewness'] = self.data.skew()
		df_stats = df_stats.reindex(['count', 'mean', 'std', 'var', 'kurtosis', 'skewness', 'min', '25%', '50%', '75%', 'max'])
		
		if ret_type =='pandas':
			return df_stats
		else:
			return df_stats.to_dict()


	def correlation(self):
		pass

	def whiten(self):
		'''

		'''
		pass

	def one_hot_encode(self):
		pass




