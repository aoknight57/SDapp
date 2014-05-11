from HTMLParser import HTMLParser
import os

MainFolderLocation = os.getcwd() + "/"
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
        	self.cellrs = 0
        	self.cellrsrange = 0
        	self.cellcsrange = 0
        	self.cellcs = 0	        
	        for attr in attrs:
	        	if attr[0].lower() == 'rowspan':
	        		self.spans.append(['r', 
	        						   self.column, 
	        						   self.row, 
	        						   int(attr[1])])
	        		self.cellrs += 1
	        		self.cellrsrange = int(attr[1])
	        	if attr[0].lower() == 'colspan':
	        		self.spans.append(['c', 
	        						   self.column, 
	        						   self.row, 
	        						   int(attr[1])])
	        		self.cellcs += 1
	        		self.cellcsrange = int(attr[1])

	        	# if there is a colspan and a rowspan, this creates a box in
	        	# html; this fills in more rowspans to complete the box
	        	if self.cellrs == 1 and self.cellcs == 1:
	        		for x in range(1, self.cellcsrange):
	        			self.spans.append(['r', 
	        							   self.column + x, 
	        							   self.row, 
	        							   self.cellrsrange])
	        		cellcs = 0
	        		cellrs = 0

	       
	        # self.spans.sort(key=lambda x: x[1])
	        # this adds a spacer if there is a rowspan running through
	        # for span in self.spans:
	        # 	if span[0] == 'r':
	        # 		if self.column == span[1] and \
	        # 		   self.row > span[2] and \
	        # 		   self.row < span[2] + span[3]:
	        # 			# self.urrow.append('<rowspan>')
	        # 			# try:
        	# 			self.urrow.append('')
	        # 			# except:
	        # 			# 	self.urrow.append('span data error')
	        # 			self.column += 1


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
	        	if span[0] == 'r':
	        		if self.column == span[1] and \
	        		   self.row > span[2] and \
	        		   self.row < span[2] + span[3]:
	        			# self.urrow.append('<rowspan>')
	        			# try:
        				self.urrow.insert(self.column-1,'')
	        			# except:
	        			# 	self.urrow.append('span data error')
	        			self.column += 1
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
	for index in range(min(6, len(rowstrlengths))):
		if rowstrlengths[index] > titlerowminscore:
			lasttitlerow = index	
	return lasttitlerow

def jointitlerows(table, lasttitlerow):
	titlerows = []
	for x in range(min(lasttitlerow+1, len(table))):
		row = []
		for cell in table[x]:
			row.append(str(cell))
		titlerows.append(row)


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
		if row == []:
			break
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
		if len(matchindices) > 1 and len(flipdata) != 0:
			matchindexscores = {}
			for index in matchindices:
				count = sum(1 for something in flipdata[index] if something)
				
				matchindexscores[index] = count
			bestmatch = max(key for key, score in matchindexscores.iteritems())
			bestindices.append(bestmatch)
		else:
			bestindices.append(matchindices[0])
	if len(bestindices) < 10:
		for x in range(10-len(bestindices)):
			bestindices.append(0)
	return bestindices

def fillinmissingnames(bestindices, table, lasttitlerow):	
	# try: 
	nameindex = bestindices[0]
	# except: 
		# return table
	for row in table:
		if row == []:
			break
		if row[nameindex] == '' and table.index(row) > lasttitlerow + 1:
			row[nameindex] = lastrow[nameindex] 
		lastrow = row
	for row in table:
		if row == []:
			break
		if 'total' in str(row[nameindex]).lower() and len(row[nameindex]) < 10:
			row[nameindex] = ''
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
		if row == []:
			break
		if row[optionindices[0]] != '' and row[optionindices[4]] != '' and row[optionindices[5]] != '':
		
			if len(str(row[optionindices[1]])) < 14 and len(str(row[optionindices[2]])) < 14 and len(str(row[optionindices[3]])) < 14 and len(str(row[optionindices[4]])) < 14:
				fileroptionbalances.append([row[optionindex] for optionindex in optionindices])
		if not any(row[equityindex] == '' for equityindex in equityindices):
			if len(str(row[equityindices[1]])) < 14 and len(str(row[equityindices[2]])) < 14:
				filerequitybalances.append([row[equityindex] for equityindex in equityindices])
		if not any(row[incentiveplanindex] == '' for incentiveplanindex in incentiveplanindices):
			if len(str(row[incentiveplanindices[1]])) < 14 and len(str(row[incentiveplanindices[2]])) < 14:
				filerincentiveplanbalances.append([row[incentiveplanindex] for incentiveplanindex in incentiveplanindices])	
	return fileroptionbalances, filerequitybalances, filerincentiveplanbalances

def breakglass(formattedtable, lasttitlerow):
	bestindices = [0, 1, 2, 0, 3, 4, 5, 6, 7, 8]
	for row in formattedtable:
		for cell in row:
			if cell < 0 and cell > -20:
				cell = ''
	
	newtable = formattedtable[lasttitlerow + 1:]
	lasttitlerow = -1
	formattedtable = newtable
	newtable = []
	for row in formattedtable:
		if not all(x == '' for x in row):
			newtable.append(row)
	formattedtable = newtable
	flipdata = map(list, zip(*formattedtable))
	newtable = []
	for row in flipdata:
		if not all(x == '' for x in row):
			newtable.append(row) 
	# print flipdata
	# print emptyindices
	formattedtable = map(list, zip(*newtable))
	return formattedtable, lasttitlerow, bestindices


def tabletobalances(filename):
	htmlfile = open(filename, 'r')
	parser = TableParse()
	parser.feed(htmlfile.read())
	htmlfile.close()

	newtable = parser.urtable
	badrowremover = []
	for row in newtable:
		if row != []:
			badrowremover.append(row)
	maxrowlen = 0

	# repairs poorly formed html tables by filling unfinished rows with blanks
	for row in badrowremover:
		if len(row) > maxrowlen:
			maxrowlen = len(row)
	for row in badrowremover:
		if len(row) < maxrowlen:
			for x in range(maxrowlen-len(row)):
				row.append('')
	y = []
	for row in newtable:
		y.append(len(row))


	# below creates float values, where possible, 
	formattedtable = numformat(badrowremover)
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
	# In case of disaster [Ford's proxy statements, which are unparseable]
	if bestindices == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
		formattedtable, lasttitlerow, bestindices = breakglass(formattedtable, lasttitlerow)
		



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
	
	print '--------------------------------------------------------'
	for row in tablewithnames:
		print row, len(row)
	print '--------------'
	print bestindices
	print '--------------'
	for row in fileroptionbalances:
		print row
	print '--------------'
	for row in filerequitybalances:
		print row
	print '--------------'
	for row in filerincentiveplanbalances:
		print row
	return fileroptionbalances, filerequitybalances, filerincentiveplanbalances, tablewithnames


def filemapper():
	import os
	htmldirectory = []
	for root, dirs, files in os.walk (MainFolderLocation + "ScriptTables"):
		for file in files:
			if file.endswith('.txt'):
				htmldirectory.append(os.path.join(root, file))
	return htmldirectory

def rawfilemapper():
	import os
	rawfiledirectory = []
	for root, dirs, files in os.walk (MainFolderLocation + "testrawtext"):
		for file in files:
			if file.endswith('.txt'):
				rawfiledirectory.append(os.path.join(root, file))
	return rawfiledirectory


CIKs = []
TablesFromFiles = []
rawfilemap = rawfilemapper()
for rawfile in rawfilemap:
	f = open(rawfile, 'r')
	filestring = f.read()
	lowerfilestring = filestring.lower()
	tablestarts = scanner(lowerfilestring, "<table")
	tableends = scanner(lowerfilestring, "</table>")
#	print len(tablestarts)
	rawfiletables = []
	for i in range(len(tablestarts)):
		rawfiletables.append(filestring[\
			tablestarts[i]:(tableends[i]+len("</table>"))])
#	print tables
	parsedfiletables = []
	for table in rawfiletables:
		parser = TableParse()
		parser.feed(table)
		parsedtable = parser.urtable
		parsedfiletables.append(parsedtable) 

	tabletitlefinder = scanner(lowerfilestring, "outstanding equity awards")
#	print tabletitlefinder
	

	tablecounts = []
	for table in rawfiletables:
		matchcount = 0.0
		for titlelocation in tabletitlefinder:
			if abs(tablestarts[rawfiletables.index(table)] - titlelocation) \
			< 1000:
				matchcount += 1000

		tablecounts.append(matchcount)
	wordmatchqualtable = []
	wordmatchqualrow = []
	tablematchquality = []
	for table in parsedfiletables:
		lasttitlerow = findtitlerows(table)
		proxytitles = jointitlerows(table, lasttitlerow)
		# print proxytitles
		# print columnlist()
		targetcategories = columnlist()
		targetcategoriesmatchmatrix = []

		#Below loops build a matrix of matches for each category
		matchmatrix = matchmatrixbuilder(targetcategories, proxytitles)
		# print table
		# print proxytitles
		# print matchmatrix
		tablechoicescores = []
		for row in matchmatrix:
			# print row
			try:
				tablechoicescores.append(max(row))
			except:
				tablechoicescores.append(0)
		maxrow = 0
		for row in table:
			if len(row) > maxrow:
				maxrow = len(row)
		tablelen = len(table)
		if tablelen < 4:
			tablechoicescores.append(-20)
		if maxrow < 8:
			tablechoicescores.append(-20)

		wordmatchqualtable.append(sum(tablechoicescores))
	# print wordmatchqualtable
	# print len(wordmatchqualtable)
	# print tablecounts
	# print len(tablecounts)
	for i in range(len(tablecounts)):
		tablecounts[i] += wordmatchqualtable[i]*(200)


#	print tablecounts

	for cell in tablecounts:
		bestmatchscore = max(tablecounts)
		bestmatchindex = tablecounts.index(bestmatchscore)
#	print bestmatchscore
#	print bestmatchindex
#	print len(tablecounts)
#	print len(rawfiletables)
#	print rawfiletables[bestmatchindex]
#	print rawfiletables[bestmatchindex]

	CIKfindstart = lowerfilestring.find("central index key")
#	print "CIK Findstart", CIKfindstart
	searchrange = 28
	numcount = 0
	for i in range(CIKfindstart, CIKfindstart + searchrange):
		if isfloat(lowerfilestring[i:i+1]):
			numcount += 1

#	print "numcount", numcount
	CIK = lowerfilestring[(CIKfindstart + searchrange - numcount):\
						  (CIKfindstart + searchrange - numcount + 10)]
	CIKs.append(CIK)
	TablesFromFiles.append([rawfiletables[bestmatchindex], CIK])
#	print lowerfilestring.find()
#print TablesFromFiles[2][0]
filecount = 1
for item in TablesFromFiles:
	target = open((MainFolderLocation + "ScriptTables/" + "file" + \
				  str(filecount) + item[1] + ".txt"), 'w')
	target.truncate()
	filecount += 1
	print>>target, TablesFromFiles[TablesFromFiles.index(item)][0]
	target.close()

htmlmap = filemapper()

for htmlfile in htmlmap:
	print htmlfile
	fileroptionbalances, filerequitybalances, filerincentiveplanbalances, tablewithnames = tabletobalances(htmlfile)
	CIK = htmlfile[len(htmlfile)-14:len(htmlfile)-4]
	print CIK
	target = open(MainFolderLocation + 'Output/CIK' + CIK + '.txt', 'w')
	print>>target, 'CIK:', CIK
	print>>target, 'Proxy Outstanding Equity Parser Results'
	print>>target, '--------------------------------------------------------'
	# for row in tablewithnames:
	# 	print>>target, row
	# print>>target, '--------------'
	print>>target, "Option Balances:"
	print>>target, "1. name"
	print>>target, "2. number of securities underlying unexercised options # exercisable"
	print>>target, "3. number of securities underlying unexercised options # unexercisable" 
	print>>target, "4. equity incentive plan awards: number of securities underlying unexercised unearned options #"
	print>>target, "5. option exercise price $"
	print>>target, "6. option expiration date"
	for row in fileroptionbalances:
		print>>target, row
	print>>target, '--------------'
	print>>target, "Equity Balances:"
	print>>target, "1. name"
	print>>target, "2. number of shares or units of stock that have not vested #"
	print>>target, "3. market value of shares or units of stock that have not vested #"
	for row in filerequitybalances:
		print>>target, row
	print>>target, '--------------'
	print>>target, "Incentive Plan Balances:"
	print>>target, "1. name"
	print>>target, "2. equity incentive plan awards: number of unearned shares, units or other rights that have not vested #"
	print>>target, "3. equity incentive plan awards: market or payout value of unearned shares, units or other rights that have not vested $"
	for row in filerincentiveplanbalances:
		print>>target, row
	

# Below is for testing the parser on a simple table
# htmlfile = open('basictable.html', 'r')
# parser = TableParse()
# parser.feed(htmlfile.read())
# htmlfile.close()

# newtable = parser.urtable
# for row in newtable:
# 	print len(row), row 
