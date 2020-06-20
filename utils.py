import numpy as np 
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime

# function to find min and argmin of nearest date_index nearest to specified date and its index
def nearest_date(date,date_list):

	min_val = min(date_list, key=lambda x: abs(x - datetime.strptime(date, '%Y-%m-%d')))

	return min_val, date_list.index(min_val)

# function that returns list of percent changes of asset prices 
def percent_change(lst):
	return [100*(lst[i+1] - lst[i]) / lst[i] for i in range(len(lst) - 1)]

