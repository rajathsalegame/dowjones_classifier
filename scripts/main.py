from data import Portfolio, Dataset
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pda


def main():
	'''
	playground for testing out code! 

	'''

	stock_list = ['AAPL']

	start = '1990-01-01'
	end = '2020-01-01'
	dowjones = Portfolio('^DJI',stock_list,yf.Ticker('^DJI').history(start=start,end=end),start=start,end=end)
	ax = dowjones.price_plot(stock_list,'Open',start,end)
	plt.show()

	params = {'pfolio_obj': dowjones, 'data_type': 'Close', 'feature_names': stock_list, 'periods': [10, 20], 'horizon': 3, 'target_name': 'returns', 'task_type': 'classification'}

	# feature_names = stock_list
	# target_name = 'returns'
	# periods = [10, 20]

	data = Dataset(**params)
	print(data.df.tail())

	# corr_matrix = data.corr_plot(feature_names, periods)
	# plt.show()

	# df = data.statistics(feature_names,periods)
	# print(df)


if __name__ == '__main__':
	main()