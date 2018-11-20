#!usr/bin/python
# coding:utf-8

from matplotlib.dates import DateFormatter
from matplotlib.dates import DayLocator
from matplotlib.dates import MonthLocator
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.finance import candlestick_ochl

import sys
from datetime import date
import matplotlib.pyplot as plt

today = date.today()
start = (today.year-1, today.month, today.day)
# 创建定位器
alldays = DayLocator()
months = MonthLocator()
month_formatter = DateFormatter("%b %Y") #创建格式化日期

symbol = "DISH"

if len(sys.argv) == 2:
    symbol = sys.argv[1]
quotes = quotes_historical_yahoo_ochl(symbol,start,today)

# 创建一个matplotlib的figure,这是一个绘图组件的顶层容器
fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(month_formatter)
candlestick_ochl(ax, quotes=quotes)
fig.autofmt_xdate()
plt.show()



