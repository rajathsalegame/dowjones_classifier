from data import Portfolio, Dataset
from utils import *
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


def main():

	stock_list = ['AXP', 'AAPL', 'BA', 'CAT', 'CSCO', 'CVX', 'XOM', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', \
	'KO', 'JPM', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UNH', 'RTX', 'VZ', 'V', 'WBA', \
	'WMT', 'DIS']


	start = '1990-01-01'
	end = '2020-01-01'
	dowjones = Portfolio('^DJI',stock_list,yf.Ticker('^DJI').history(start=start,end=end),start=start,end=end)
	ax = dowjones.price_plot(stock_list,'Open',start,end)
	plt.show()

	# feature_names = stock_list
	# target_name = 'returns'
	# periods = [10, 20]

	# data = Dataset(dowjones, 'Open', feature_names, periods, target_name)


	# corr_matrix = data.corr_plot(feature_names, periods)
	# plt.show()

	# df = data.statistics(feature_names,periods)
	# print(df)
if __name__ == '__main__':
	main()