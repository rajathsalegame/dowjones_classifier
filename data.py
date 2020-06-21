import numpy as np 
import matplotlib.pyplot as plt
import os
import pandas as pd
import yfinance as yf
from datetime import datetime
from scipy import stats
import seaborn as sns
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

			dates = list(df.index)

			if plot_type == 'pct_change':
				col_data = percent_change(col_data)

			start_date, start_idx = nearest_date(start, dates)
			end_date, end_idx = nearest_date(end, dates)
			if asset != 'returns':
				ax.plot(dates[start_idx:end_idx], col_data[start_idx:end_idx],label=f'{asset}',linewidth=0.5)
			else:
				ax.plot(dates[start_idx:end_idx],col_data[start_idx:end_idx],label=f'{self.name}',linewidth=0.5)

		ax.legend()
		ax.set_xlabel('Date')
		ax.set_title(f'{data_type} Share Prices in USD vs. Time')
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

		return np.array([int(data[i+1] / data[i] - 1 >= 0) if data[i+1] != 0 and data[i] != 0 else 0 for i in range(len(data)-1)])

class Dataset:
	'''
	base class for data that will be loaded into the models and used for analysis

	designed to be flexible with respect to feature selection, return periods, target selection, and number of classes

	default behavior turns off numpy mode; can be turned on to save memory in case of large datsets and when ready to train on model 
	'''
	def __init__(self, pfolio_obj, data_type, feature_names, periods, target_name, numpy_mode=False):
		self.df = generate_df(pfolio_obj, data_type, feature_names, periods, target_name)
		self.data_type = data_type
		self.n_samples = len(self.df.index)
		self.n_features = len(self.df.columns)
		self.n_classes = len(np.unique(self.df[target_name].to_numpy()))
		self.data = self.df.drop(target_name,axis=1)
		self.target = self.df[target_name]
		self.features = list(itertools.product(feature_names, periods))

		if numpy_mode:
			self.data = self.data.to_numpy()
			self.target = self.target.to_numpy()
	
	def numpy_mode(self):
		self.data = self.data.to_numpy()
		self.target = self.data.to_numpy()

		# to save memory in case of extremely large matrices
		del self.df 

	def statistics(self,features, periods, ret_type='pandas'):
		''' 
		returns pandas df or dict of desired summary statistics for given features using pandas and scipy.stats module
		'''

		feats = list(itertools.product(features, periods))
		df_stats = self.df[feats].describe()

		df_stats.loc['var'] = self.data.var()
		df_stats.loc['kurtosis'] = self.data.kurtosis()
		df_stats.loc['skewness'] = self.data.skew()
		df_stats = df_stats.reindex(['count', 'mean', 'std', 'var', 'kurtosis', 'skewness', 'min', '25%', '50%', '75%', 'max'])
		
		if ret_type =='pandas':
			return df_stats
		else:
			return df_stats.to_dict()


	def corr_plot(self,features,periods):

		corr_df = self.data.corr()

		cmap=sns.diverging_palette(5, 250, as_cmap=True)

		corr_df.style.background_gradient(cmap, axis=1)\
    	.set_properties(**{'max-width': '80px', 'font-size': '10pt'})\
	    .set_caption("Hover to magify")\
	    .set_precision(2)\
	    .set_table_styles(magnify())

		return sns.heatmap(corr_df,xticklabels=corr_df.columns,yticklabels=corr_df.columns,annot=True)
		
	def whiten(self):
		'''

		'''
		pass

	def one_hot_encode(self):
		pass




