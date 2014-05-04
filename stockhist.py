import requests
import datetime

# This requires requests, which can be installed via pip using "pip install
# requests" (http://docs.python-requests.org/en/latest/user/install/#install 
# for info)

SpecialDistThreshold = .2 #for both splits and special dividends
NoiseThreshold = .002



def yahoodatetuple(dateobject):
	mindex = dateobject.month - 1
	dindex = dateobject.day
	yindex = dateobject.year

	return mindex, dindex, yindex

def csvscraper(url):
	# ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close', 
	# 'Dividend/Special Distribution/Stock Split']

	IDprices = []
	response = requests.get(url)
	
	responsetext = response.text.encode('ascii')
	linelist = responsetext.rstrip().rsplit('\n')
	linelist.pop(0)
	for line in linelist:
		IDprices.append(line.rsplit(','))

	lastadjust = 1
	

	# Adds in splits and dividends:
	for line in IDprices:
		cumulativeadjust = float(line[4])/float(line[6])
		line.append(round(cumulativeadjust, 2))
		if cumulativeadjust - lastadjust > SpecialDistThreshold:
			line.append(0)
			line.append(round(cumulativeadjust - lastadjust, 2))
		elif cumulativeadjust - lastadjust > NoiseThreshold:
			line.append(round(cumulativeadjust - lastadjust, 6))
			line.append(0)
		else:
			line.append(0)
			line.append(0)

		lastadjust = cumulativeadjust
	# prints special dividends:
	print "Let's print the lines with dividends and splits (check the last entry for shares created per share in the split and the second to last entry for dividends):"
	for line in IDprices:
		if line[8] != 0 or line[9] != 0:
			print line

	return IDprices

urlbase = 'http://ichart.yahoo.com/table.csv?s='

tickers = ["AAPL", "GOOGL"]


today = datetime.date.today()
startday = datetime.date(today.year - 10, today.month, today.day + 1)

print "Today:", today
print "First day of series (10 years):", startday

startdaytuple = yahoodatetuple(startday)
todaytuple = yahoodatetuple(today)

alltickersdata = []

for ticker in tickers:
	csvurl = urlbase + ticker + '&a=%s&b=%s&c=%s' % startdaytuple +'&d=%s&e=%s&f=%s&g=d&ignore=.csv' % todaytuple
	print csvurl
	print ticker
	tickerdata = csvscraper(csvurl)
	alltickersdata.append(tickerdata)
	target = open(ticker+'stockhist.txt', 'w')
	for row in tickerdata:
		print>>target, row
	target.close()


