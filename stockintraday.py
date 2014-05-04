import requests
import datetime

def stamptotime(stamp):
	time = datetime.datetime.fromtimestamp(stamp)
	tzadj = datetime.timedelta(hours=1)
	st = tzadj + time
	return st.strftime('%Y-%m-%d %H:%M:%S')

def isfloat(data):
	try:
		a = float(data)
		a = True
	except:
		a = False
	return a

def csvscraper(url):
	# values:Timestamp,close,high,low,open,volume,date/time 

	IDprices = []
	response = requests.get(url)
	
	responsetext = response.text.encode('ascii')
	linelist = responsetext.rstrip().rsplit('\n')
	# linelist.pop(0)
	for line in linelist:
		IDprices.append(line.rsplit(','))
	linesfordeletion = []
	for line in IDprices:
		if isfloat(line[0]):
			line.append(stamptotime(float(line[0])))
		else:
			linesfordeletion.append(IDprices.index(line))
	print linesfordeletion
	for entry in linesfordeletion:
		IDprices.pop(0)

	# prints special dividends:
	for line in IDprices:
		print line
	return IDprices


a = 1399037403
b = 1399060800
# st = datetime.datetime.fromtimestamp(a).strftime('%Y-%m-%d %H:%M:%S')


print stamptotime(a)
print stamptotime(b)
st = stamptotime(a)


tickers = ['GOOGL', 'AAPL']

for ticker in tickers:
	url = 'http://chartapi.finance.yahoo.com/instrument/1.0/%s/chartdata;type=quote;range=1d/csv' % ticker
	print url
	print ticker
	tickerdata = csvscraper(url)
	target = open(ticker+'stockintraday.txt', 'w')
	for row in tickerdata:
		print>>target, row
	target.close()

print 'done'