from HTMLParser import HTMLParser
import os

# the short explanation of how the TableParse class works is that it reads each
# character in a string of an html table and detects: start tags (with 
# colspans/rowspans which are basically just merged cells), end tags, and data. 
# The parse adds in cells to 'unmerge' cells to make the columns/rows line up
# correctly.
# We define and apply later functions to 'unmerge' the 'merged' cells.  

class TableParse(HTMLParser):
    def __init__(self):
    	HTMLParser.__init__(self)
    	self.spans = []
    	self.row = 0
    	self.column = 0
    	self.urrow = []
    	self.urtable = []
    	self.cell = ''

    # This next part detects colspans and rowspans
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
        	self.column = 0
        	self.row += 1
        if tag == 'td':
        	self.column += 1
	        # below adds colspans, rowspans or both
	        for attr in attrs:
	        	self.cellrs = 0
	        	self.cellrsrange = 0
	        	self.cellcsrange = 0
	        	self.cellcs = 0
	        	if attr[0] == 'rowspan':
	        		self.spans.append(['r', 
	        						   self.column, 
	        						   self.row, 
	        						   int(attr[1])])
	        		self.cellrs += 1
	        		self.cellrsrange = int(attr[1])
	        	if attr[0] == 'colspan':
	        		self.spans.append(['c', 
	        						   self.column, 
	        						   self.row, 
	        						   int(attr[1])])
	        		self.cellcs += 1
	        		self.cellcsrange = int(attr[1])

	        	# if there is a colspan and a rowspan, this creates a box in
	        	# html; this fills in more colspans to complete the box
	        	if self.cellrs != 0 and self.cellcs != 0:
	        		for x in range(1,self.cellrsrange):
	        			self.spans.append(['c', 
	        							   self.column, 
	        							   self.row + x, 
	        							   self.cellcsrange])

	        # this adds a spacer if there is a rowspan running through
	        for span in self.spans:
	        	if span[0] == 'r':
	        		if self.column == span[1] and \
	        		   self.row > span[2] and \
	        		   self.row < span[2] + span[3]:
	        			# self.urrow.append('<rowspan>')
	        			self.urrow.append(span[4])
	        			self.column += 1

    # this next part assembles a table as it hits end tags and inserts data 
    # into any spans that were detected
    def handle_endtag(self, tag):
        if tag == 'tr':
        	self.urtable.append(self.urrow)
        	self.urrow = []
        if tag == 'td':
        	if self.cell == '':
        		self.urrow.append('')
        	else:
        		self.urrow.append(self.cell)
        	# this inserts the data into a colspan/rowspan record
        	for span in self.spans:        		
	        	if span[1] == self.column and \
	        	   span[2] == self.row:
	        		if self.cell == '':
	        			span.append('')
	        		else:
		        		span.append(self.cell)
		    # Below adds a spacer if there is a colspan at this spot 
	        for span in self.spans:
	        	if span[0] == 'c' and \
	        	   self.row == span[2] and \
	        	   self.column == span[1]:
        			for x in range(1, span[3]):
	        			# self.urrow.append('<colspan>')
	        			self.urrow.append(span[4])
	        			self.column += 1
	        self.cell = ''
	# Here is how, char by char each cell is compiled
    def handle_data(self, data):
        if data != None:# and data != '$':
        	self.cell += data.strip()

# This class is useful for storing and retrieving data tied to coordinates in
# a more natural form sthan a list of three items
class makecoord(object):
	def __init__(self, data, x, y):
		self.data = data
		self.x = x
		self.y = y
	def __repr__(self):
		return str(self.data) + ' ' + str(self.x) + ' ' + str(self.y)
	def __str__(self):
		return str(self.data) + ' ' + str(self.x) + ' ' + str(self.y)



def isfloat(data):
	try:
		a = float(data)
		a = True
		
	except:
		a = False

	return a

def numformat(table):
	newtable = []
	for row in table:
		newrow = []
		for cell in row:
			if isfloat(cell.replace(',','').\
							replace('(','-').\
							replace(')','')):
				newrow.append(float(cell.replace(',','').\
										 replace('(','-').\
										 replace(')','')))
			elif cell=='$':
				newrow.append('')
			else:
				newrow.append(cell)
		newtable.append(newrow)
	return newtable

def findtitlerows(table):
	rowstrlengths = []
	strlengths = 0
	floatpenalty = 20 #this is an arbitrary value which reflects that
	# it is unlikely that a title row will include many floats
	titlerowminscore = 0
	for row in table:

		for cell in row:
			if not isfloat(cell):
				strlengths += len(cell)
			if isfloat(cell):
				strlengths -= floatpenalty
		rowstrlengths.append(strlengths)
		strlengths = 0
	lasttitlerow = 0
	for index in range(6):
		if rowstrlengths[index] > titlerowminscore:
			lasttitlerow = index	
	return lasttitlerow

def jointitlerows(table, lasttitlerow):
	titlerows = []
	for x in range(lasttitlerow+1):
		titlerows.append(table[x])


	titlelist = [''.join(x) for x in zip(*titlerows)]
	return titlelist

def columnlist():
	# ------ Options below ----------------------------
	Col0 = "name".split()
	Col1 = "number of securities underlying unexercised options # exercisable".split()
	Col2 = "number of securities underlying unexercised options # unexercisable".split()
	Col3 = "equity incentive plan awards: number of securities underlying unexercised unearned options #".split()
	Col4 = "option exercise price $".split()
	Col5 = "option expiration date".split() 
	# ------ Shares below -----------------------------
	Col6 = "number of shares or units of stock that have not vested #".split()
	Col7 = "market value of shares or units of stock that have not vested #".split()
	# ------ Incentive plan awards below --------------
	Col8 = "equity incentive plan awards: number of unearned shares, units or other rights that have not vested #".split()
	Col9 = "equity incentive plan awards: market or payout value of unearned shares, units or other rights that have not vested $".split()
	ColList = [Col0, Col1, Col2, Col3, Col4, Col5, Col6, Col7, Col8, Col9]
	return ColList

def scanner(originalstring, findstring):
	indices = []
	startposition = 0
	while True:
		i = originalstring.find(findstring, startposition)
		if i == -1: break
		indices.append(i)
		startposition = i + 1
	return indices

def targetcategorymatch(targetcategory, title):
	targetcategorymatch = 0
	targetcategorylength = ''.join(targetcategory)
	for word in targetcategory:
		targetcategorymatch += len(scanner(title.lower(), word))*len(word)
		# Below is ugly but necessary magic built in to avoid positive result
		# when searching for 'exercisable' if the scanner finds the word 
		# 'unexercisable.' This is unfortunately necessary because two of the
		# target categories are different by only two characters 
		# ('unexercisable' v. 'exercisable').  
		if word == 'exercisable':
			targetcategorymatch -= len(scanner(title.lower(), 'unexercisable'))*len('unexercisable')
	return round(float(targetcategorymatch)/max(float(1),float(len(targetcategorylength))),4) #match quality

def matchmatrixbuilder(targetcategories, proxytitles):
	targetcategoriesmatchmatrix = []
	for targetcategory in targetcategories:
		# Each time the below loop runs, it determines how well all titles from the 
		# proxy match the idealized category names and it appends this to a matrix
		# of matches.  
		targetcategorymatches = []
		for title in proxytitles:
			targetcategorymatches.append(targetcategorymatch(targetcategory, title))
		targetcategoriesmatchmatrix.append(targetcategorymatches)
	return targetcategoriesmatchmatrix

def matchindexbuilder(matchmatrix):
	matchindiceslist = []
	for row in matchmatrix:
		match = max(row)
		matchindices = []
		for x in range(len(row)):
			if row[x] == match:
				matchindices.append(x)
		matchindiceslist.append(matchindices)

	return matchindiceslist

# This is some hairy python, but what it does is loop through the data associated
#  with each match that has a tie for the quality of its match
# (these are probably copies which result from unmerging cells)
# the tiebreaker breaks the tie based on which index column has the most nonempty data values.
# The tactic of picking the column with the most 
# matches is not arbitrary, because the similar columns should be near copies
# with certain numbers omitted in any cells that were never merged.  Therefore
# the largest column of data should have all relevant data.  
# ex.
# | match1| match2|     | match1| match2|
# |      $| 100.22| --> |       | 100.22|  
# |       | 123.55| --> | 123.55| 123.55|
# The below function will pick match2 because it is most populated.   

def tiebreakermatchbuilder(matchindiceslist, table):
	flipdata = map(list, zip(*table))
	bestindices = []
	for matchindices in matchindiceslist:
		if len(matchindices) > 1:
			matchindexscores = {}
			for index in matchindices:
				count = sum(1 for something in flipdata[index] if something)
				matchindexscores[index] = count
			bestmatch = max(key for key, score in matchindexscores.iteritems())
			bestindices.append(bestmatch)
		else:
			bestindices.append(matchindices[0])
	return bestindices

def fillinmissingnames(bestindices, table, lasttitlerow):	
	nameindex = bestindices[0]

	for row in table:
		if row[0] == '' and table.index(row) > lasttitlerow + 1:
			row[0] = lastrow[0] 
		lastrow = row
	for row in table:
		if 'total' in row[0].lower() and len(row[0]) < 10:
			row[0] = ''
	return table

def splitindicesbytype(bestindices):
	optionindices = bestindices[:6]
	equityindices = [bestindices[0]] + bestindices[6:8]
	incentiveplanindices = [bestindices[0]] + bestindices[8:]
	return optionindices, equityindices, incentiveplanindices

def extractbalancesbytype(optionindices, equityindices, incentiveplanindices, datatable):
	fileroptionbalances = []
	filerequitybalances = []
	filerincentiveplanbalances = []
	for row in datatable:
		if not any(row[optionindex] == '' for optionindex in optionindices):
			fileroptionbalances.append([row[optionindex] for optionindex in optionindices])
		if not any(row[equityindex] == '' for equityindex in equityindices):
			filerequitybalances.append([row[equityindex] for equityindex in equityindices])
		if not any(row[incentiveplanindex] == '' for incentiveplanindex in incentiveplanindices):
			filerincentiveplanbalances.append([row[incentiveplanindex] for incentiveplanindex in incentiveplanindices])	
	return fileroptionbalances, filerequitybalances, filerincentiveplanbalances

def tabletobalances(filename):
	htmlfile = open(filename, 'r')
	parser = TableParse()
	parser.feed(htmlfile.read())
	htmlfile.close()

	newtable = parser.urtable
	y = []
	for row in newtable:
		y.append(len(row))


	# below creates float values, where possible, 
	formattedtable = numformat(newtable)
	# Lets find the table heading
	lasttitlerow = findtitlerows(formattedtable)
	proxytitles = jointitlerows(formattedtable, lasttitlerow)
	# print proxytitles
	# print columnlist()
	targetcategories = columnlist()
	targetcategoriesmatchmatrix = []

	#Below loops build a matrix of matches for each category
	matchmatrix = matchmatrixbuilder(targetcategories, proxytitles)
	# for row in matchmatrix:
		# print row
	# print len(matchmatrix[1])

	matchindiceslist = matchindexbuilder(matchmatrix)
	# is there a tie?
	bestindices = tiebreakermatchbuilder(matchindiceslist, formattedtable)
	# fill in omitted names of individuals reported based on preceding lines
	tablewithnames = fillinmissingnames(bestindices, formattedtable, lasttitlerow)
	# print bestindices

	optionindices, equityindices, incentiveplanindices = splitindicesbytype(bestindices)

	fileroptionbalances = [] 
	filerequitybalances = []
	filerincentiveplanbalances = []
	datatable = tablewithnames[lasttitlerow + 1:]
	# for row in datatable:
		# print row
	fileroptionbalances, filerequitybalances, filerincentiveplanbalances = extractbalancesbytype(optionindices, equityindices, incentiveplanindices, datatable)

	print '--------------'
	for row in fileroptionbalances:
		print row
	print '--------------'
	for row in filerequitybalances:
		print row
	print '--------------'
	for row in filerincentiveplanbalances:
		print row





tabletobalances('file10000051143.txt')
