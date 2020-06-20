from data import Portfolio, Dataset
from utils import *
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


def main():

	stock_list = ['AXP', 'AAPL', 'BA', 'CAT', 'CSCO', 'CVX', 'XOM', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', \
	'KO', 'JPM', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UNH', 'RTX', 'VZ', 'V', 'WBA', \
	'WMT', 'DIS', 'DOW']


	start = '2000-01-01'
	end = '2019-06-18'
	dowjones = Portfolio('^DJIA',stock_list,yf.Ticker('^DJI').history(start=start,end=end),start=start,end=end)

	ax1 = dowjones.price_plot(['returns'], 'Open', '1970-01-01', '2010-03-01')
	plt.show()

	feature_names = ['AAPL', 'BA', 'MMM', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UNH', 'RTX', 'VZ', 'V', 'WBA', 'WMT', 'DIS', 'DOW']
	target_name = 'returns'
	periods = [10, 20]

	data = Dataset(dowjones, 'Open', feature_names, periods, target_name)
	print(data.df)


if __name__ == '__main__':
	main()