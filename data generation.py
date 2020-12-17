import pandas_datareader as web


stocks = []
f = open("symbols.txt", "r")
for line in f:
    stocks.append(line.strip())
    
f.close()

web.DataReader(stocks, "yahoo", start="2000-1-1", end="2019-12-31")["Adj Close"].to_csv("prices.csv")