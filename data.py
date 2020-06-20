import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import sys
import yfinance as yf
from pprint import pprint
from datetime import datetime
from utils import *

class Portfolio:
	'''
	constructs class representing a portfolio of securities and associated returns

	attributes:
		nassets (int):
		period (str):
		returns (pandas df):
		sec (pandas df)
		fields (list)
	'''

	def __init__(self,name,assets,returns,period,index_by_date=True):
		'''
		args:
			assets (list):
			returns (pandas df):
			period (str):
			sec (pandas df):
			fields (list):	
			index_by_date (bool):
		'''
		self.name = name
		self.nassets = len(assets)
		self.period = period
		self.returns = returns
		self.assets = assets
		for asset in assets:
			setattr(self, asset, yf.Ticker(asset).history(period=period))
		self.fields = list(returns.columns)
		self.dates = list(returns.index)
		self.ndates = len(self.dates)

	def plot(self, assets,field,start,end,plot_type=None):

		assert(field in self.fields), "the field you have chosen is not available for analysis."

		fig, ax = plt.subplots()

		for asset in assets:
			assert(asset in self.assets or asset == 'returns'), "the asset you have chosen is not in the portfolio."

			data = getattr(self, asset)
		
			col_data = data[field].tolist()

			if plot_type == 'pct_change':
				col_data = percent_change(col_data)

			start_date, start_idx = nearest_date(start, self.dates)
			end_date, end_idx = nearest_date(end, self.dates)
			if asset != 'returns':
				ax.plot(self.dates[start_idx:end_idx],col_data[start_idx:end_idx],label=f'{asset}',linewidth=0.5)
			else:
				ax.plot(self.dates[start_idx:end_idx],col_data[start_idx:end_idx],label=f'{self.name}',linewidth=0.5)
		ax.xaxis.set_major_locator(mdates.YearLocator(3))
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
		ax.xaxis.set_minor_locator(mdates.YearLocator(3))
		ax.xaxis.set_minor_formatter(mdates.DateFormatter('%Y'))
		ax.legend()
		ax.set_xlabel('Date')
		if plot_type == 'pct_change':
			ax.set_ylabel('Percent change in USD (%)')
		else:
			ax.set_ylabel('Price per share (USD)')

		return ax 


# stock_list = ['AXP', 'AAPL', 'BA', 'CAT', 'CSCO', 'CVX', 'XOM', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', \
# 'KO', 'JPM', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UNH', 'RTX', 'VZ', 'V', 'WBA', \
# 'WMT', 'DIS', 'DOW']

stock_list = ['AXP', 'AAPL', 'BA']


dowjones = Portfolio('^DJIA',stock_list,yf.Ticker('^DJI').history('max'),period='max')

ax1 = dowjones.plot(['returns'], 'Open', '1990-01-01', '2010-03-01')

plt.show()


