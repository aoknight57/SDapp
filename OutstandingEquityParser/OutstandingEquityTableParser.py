from HTMLParser import HTMLParser
import os
#_______________________

MainFolderLocation = os.getcwd() + "/"
#_______________________
def scanner(originalstring, findstring):
	indices = []
	startposition = 0
	while True:
		i = originalstring.find(findstring, startposition)
		if i == -1: break
		indices.append(i)
		startposition = i + 1
	return indices
#iterlimitscanner is not in use, but I leave it here because it can be used
#if we need to parse by counting the first X occurrences of a p 

def iterlimitscanner(originalstring, findstring, iterlimit):
	indices = []
	startposition = 0
	counter = 0
	while True:
		i = originalstring.find(findstring, startposition)
		if i == -1: break
		counter += 1
		indices.append(i)
		if counter == iterlimit: break
		startposition = i + 1
	return indices

def isnumber(teststring):
	try: 
		float(teststring)
		return True
	except ValueError:
		return False
#this function lists the urls of the .txt files in a master directory
#it will sift through multiple levels of folders
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
#Below is the HTML Parser.  This is kind of magical to me I mostly set this up
#by searching about it, so I don't fully understand how it works.  
class MyHTMLParser(HTMLParser):
	#defines the variables we need
	def __init__(self):
		HTMLParser.__init__(self)
		self.rowstorage = []
		self.row = 0
		self.column = 0
		self.cell = ""
		self.datastorage = []

#	def handle_starttag(self, tag, attrs):
#		pass
	#this looks for new rows in the html and then moves us down one row in the 
	#list of lists
	def handle_endtag(self, tag):
		if tag == 'tr':
			self.row += 1
			self.datastorage.append(self.rowstorage)
#			print len(self.rowstorage)
			self.rowstorage = []
	#this looks for the next cell in the row in the html and then moves us down
	#one row in the list of lists
		if tag == 'td':
#			self.column = self.column + 1
			if self.cell == "":
				self.rowstorage.append("")
			else:
				self.rowstorage.append(self.cell)
			self.cell = ""
#this appends data into the list
	def handle_data(self, data):
		#This was pulling out placeholders, but including placeholders may be 
		#useful for lining up like data on columns]
		if data != None and data != '$':
			self.cell += data.strip()

#This function isn't in use but it is designed as a building block for data 
#organization. It copies a table and the sifts through the table looking for a
#desired value and changes values in the copied table 
#def emptycellreplacer(self):
#	emptycellindex = self
#	rowcount = 0
#	columncount = 0
#	for row in self:
#		for cell in row:
#			if cell == "":
#				emptycellindex[rowcount][columncount] = "Empty"
#				print emptycellindex
#			columncount += 1
#		rowcount += 1
#		columncount = 0
#	print emptycellindex

def indexvalueremover(self,index):
	rowcount = 0
	for row in self:
		row[index] = 0
	return self

#This thing searches for columns in the list of lists that are empty
#def emptycolumnpurger(self):
#	emptycellindex = self
#	emptycellindex.pop(0)
#	rowcount = 0
#	columncount = 0
#	for item in emptycellindex[1]:
#		print "Item: ", item
#		print all(row[columncount] == "" for row in emptycellindex)

#This function is fed rows and returns the quality of their match with the 
#heading columns
def headingfinder(lineforeval, headingwords, lengthofheadingwords):
	matchqualityvalue = 0.0
	charsinlineforeval = 0.0
	matchnumerator = 0.0
	for evallineitem in lineforeval:
		for headingword in headingwords: 
			if lineforeval[lineforeval.index(evallineitem)].\
			lower().find(headingword) != -1:
				matchnumerator += len(headingword)
		charsinlineforeval += len(evallineitem)
	matchqualityvalue = (matchnumerator / (max(lengthofheadingwords, \
											   charsinlineforeval)))
	return matchqualityvalue	

def columnmatcher(self, columns, selftableheadingline):
	rankofheadings = []
	for collistrow in columns:
		ranktracker = []	
		#now we have selected a category
#loops through each item to be detected by the column list
		for heading in self[selftableheadingline]:
			wordmatchcounter = 0.0
			#now we have selected a category for testing
#loops through each word comprising a part of the a detection item
			for collistitem in collistrow: 
				#now we have selected a word in the test category
				if self[selftableheadingline][self[selftableheadingline].\
				index(heading)].lower().find(collistitem) != -1:
					wordmatchcounter += len(collistitem)
#adds to the ranktracker for each heading the score of the match
#The denominator standardizes the scoring by dividing the sum of characters
#in each matching word by the greater of 1) the test category length and 2) the
#lenghth of heading being tested -- the idea is to reduce impact of a match
#when the size of test category tested heading is large (so we need more hits
#for success).  Length of heading is adjusted to remove spaces, so that lengths 
#will be apples-to-apples.
			ranktracker.append(wordmatchcounter / (max(len(str(collistrow)), \
							   len(''.join(heading.split())))))
#			print 'evaluatorscore', wordmatchcounter / (max(len(detectitem), 
#			len(heading)))
		rankofheadings.append(ranktracker)
#	print "collistrow: ", collistrow
#	print "heading    : ", heading
#	print rankofheadings
#	print self[selftableheadingline]
	

	return rankofheadings

def ranksorter(self, hurdle):
	BestIndexList = []
	BestScoreList = []
	if self == [[], [], [], [], [], [], [], [], [], []]:
		return "Error, nothing to evaluate", -1
	for columnranks in self:
		BestScore = max(columnranks)
		BestIndex = columnranks.index(BestScore)
		if BestScore > hurdle:
			BestScoreList.append(BestScore)
			BestIndexList.append(BestIndex)
			self = indexvalueremover(self,BestIndex)

		else: 
			BestScoreList.append("None")
			BestIndexList.append("None")
	return BestIndexList, len(BestIndexList) - BestIndexList.count("None")

def columnlist():
	Col0 = "name".split()
	Col1 = "number of securities underlying unexercised options # exercisable".split()
	Col2 = "number of securities underlying unexercised options # unexercisable".split()
	Col3 = "equity incentive plan awards: number of securities underlying unexercised unearned options #".split()
	Col4 = "option exercise price $".split()
	Col5 = "option expiration date".split()
	Col6 = "number of shares or units of stock that have not vested #".split()
	Col7 = "market value of shares or units of stock that have not vested #".split()
	Col8 = "equity incentive plan awards: number of unearned shares, units or other rights that have not vested #".split()
	Col9 = "equity incentive plan awards: market or payout value of unearned shares, units or other rights that have not vested $".split()
	ColList = [Col0, Col1, Col2, Col3, Col4, Col5, Col6, Col7, Col8, Col9]
	flatcollist = [headerword 
					for headertitle in ColList 
						for headerword in headertitle]
	collistlength = 0
	for item in flatcollist:
		collistlength += len(item)	


	return ColList, flatcollist, collistlength	

def columnorderdetector(self):
	
	headercolumnlist = columnlist()
	nestedcollist = headercolumnlist[0]
	
	SignificanceHurdle = .3
	selftableheadingline = 2
	IgnoreCol0 = "grant date".split()
#Loops through items in categories in the column list to generate a good heading
	righttableheading = []
	howmanyindexmatches = 0
	for x in range(0,min(4, len(self))):
		headingmatrix = columnmatcher(self, nestedcollist, x)
		y = ranksorter(headingmatrix, SignificanceHurdle)
		if y[1] > howmanyindexmatches:
			righttableheading = [y[0], y[1], x, len(self[x])]

# If no good heading was found, we try to detect if there was a unreadable 
# heading row that matches the contents of the headings we want.  If so, we try 
# to continue with the SEC prescribed heading order.  
	if righttableheading != []:
		if righttableheading[0][0] == 'None':
			righttableheading[0][0] = 0
	if righttableheading == []:

		flatcollist = headercolumnlist[1]
		collistlength = headercolumnlist[2]


		wordmatchqualrow = []
		for i in range(min(15, len(self))):
			wordmatchqualrow.append(headingfinder(self[i], flatcollist, \
									collistlength))
		if wordmatchqualrow == []:
			wordmatchqualrow = [0]
		if max(wordmatchqualrow) > SignificanceHurdle:
			statutoryheading = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
			righttableheading = [statutoryheading, 
								 len(statutoryheading) - statutoryheading.count("None"),
								 wordmatchqualrow.index(max(wordmatchqualrow)),
								 len(statutoryheading)]


	if righttableheading == []:
		return ["No Match Error, Can't Match Columns at Significance Hurdle", 
				"No Match Error", 0, "No Match Error", [None, None]]

# This creates a list of the weighted average index position of solely an option
# or stock transaction -- basically if we have only one transaction of the two,
# are the columns towards the left or right of the cell.  

	optionindexsum = 0.0
	optionindexcount = 0.0
	stockindexsum = 0.0
	stockindexcount = 0.0
	for x in range(0, 6):
		if righttableheading[0][x] != "None":
			optionindexsum += righttableheading[0][x] 
			optionindexcount += 1

	if righttableheading[0][0] != "None":
			stockindexsum += righttableheading[0][0] 
			stockindexcount += 1

	for x in range(6, 10):
		if righttableheading[0][x] != "None":
			stockindexsum += righttableheading[0][x] 
			stockindexcount += 1

	indexweightings = [optionindexsum / optionindexcount / righttableheading[3],
					   stockindexsum / stockindexcount / righttableheading[3]]
	if optionindexcount < 2:
		indexweightings[0] = None
	if stockindexcount < 2:
		indexweightings[1] = None
	righttableheading.append(indexweightings)

# This returns a tuple of 0) The index key, 1) the number of matches in the key,
# 2) the row of the table, 3) the length of the header row, and column index weights
	return righttableheading
#This works, but is not in use.  
#def EmptyRowRemover(self):
#	for line in self:
#		if all(cell is '' for cell in line):
#			self.pop(self.index(line))
def ExplicitTotalRemover(self, headingrowindex):
	for line in self:
		if any((cell == 'Total' and self.index(line) > headingrowindex) \
		for cell in line):
			self.pop(self.index(line))
	return self
def FootnoteRemover(self):
	for line in self:
		for cell in line:
			if len(cell) < 5 and cell.find('(') != -1 and cell.find(')') != -1:
				self[self.index(line)][line.index(cell)] = ""
	return self
def ConvertNumbersToFloats(self):
	for line in self:
		for cell in line:
			try:
				self[self.index(line)][line.index(cell)] = \
				float(cell.replace(',', ''))
			except ValueError:
				pass
	return self


def ReturnName(self):
	a = False
	#function checks for numbers, if none
	#it then checks to see if length, presence of "total", lack of slashes
	#indicate it is likely a name
	try:
		float(self)
	except ValueError:
		
		if (len(self) > 7 or "total" in self.lower())  and '/' not in self:
			a = True
	return a

def MissingNameAdder(self):
	rangeofnamesearch = 4
	bestnamesofar = ""
	bestindexsofar = 0
	for line in self:
		for x in range(0, min(rangeofnamesearch, len(line))):
			adjustedrange = min(rangeofnamesearch, len(line))
			if ReturnName(line[adjustedrange - 1 - x]):
				 bestnamesofar = line[adjustedrange - 1 - x]
				 bestindexsofar = adjustedrange - 1 - x
		if line != []:
			self[self.index(line)][bestindexsofar] = bestnamesofar	
		else:
			self[self.index(line)] = ""
	return self

def RowClassifier(self):
	itemsperline = []
	indexweight = []
	for line in self:
		itemsperline.append(len(line) - line.count(""))
		indexsum = 0.0
		for cell in line:
			if cell != "":
				indexsum += line.index(cell)
		if len(line) > line.count(""):
			indexweight.append( indexsum / (len(line) - \
								line.count("")) / len(line))
		else:
#		if len(line) == line.count(""):
			indexweight.append("n/a")
	return itemsperline, indexweight
#Under construction
def CellClassifier(self):
	celltype = ""
	slashcounter = 0
	isfloat = ""
	try:
		float(self)
		isfloat = "float"
		celltype = "float"
	except ValueError:
		isfloat = "notfloat"
	if isfloat == "notfloat":
		for char in xrange(len(self)):
			if self.find('/', char) == char:
				slashcounter += 1
		if slashcounter == 2 and len(self) < 15 and len(self) > 5:
			celltype = "date"
		if slashcounter > 2:
			celltype = "too many slashes"
		if slashcounter == 1 and 'n' in self.lower() and 'a' in self.lower():
			celltype = "n/a"
		if len(self) > 7 and slashcounter == 0:
			celltype = "name"
	return celltype

def CellTypes(self):
	tabletypes = []
	for line in self:
		linetypes = []
		for cell in line:
			linetypes.append(CellClassifier(cell)) 
		tabletypes.append(linetypes)
	return tabletypes

def sideofsearch(self, headingweightings, lineweighting):

	searchside = ""
# This is detecting a heading with nothing in it
	if headingweightings[0] == None and headingweightings[1] == None:
		searchside = "error bc/ heading is empty"
# This detects a heading with no option categories
	if headingweightings[0] == None and headingweightings[1] != None:
		searchside = "Right"
# This detects a heading with no stock categories
	if headingweightings[0] != None and headingweightings[1] == None:
		searchside = "Left"
# If we have both stock and options headings, this figures out what the average 
# is closer to
	if headingweightings[0] != None and headingweightings[1] != None:
		if lineweighting > ((headingweightings[0] + headingweightings[1]) / 2):
			searchside = "Right"
		else:
			searchside = "Left"
	return searchside

def SweepClassifier(self, headingweightings, lineweightings, lineindexcounts):
	rowdirections = []
	if headingweightings == [None, None]:
		for line in self:
			rowdirections.append("Error, no heading detected")
		return rowdirections
	for line in self:
		sweepside = ""
		if lineindexcounts[self.index(line)] > 9:
			sweepside = "Both"
		if 2 < lineindexcounts[self.index(line)] < 10:
			sweepside = sideofsearch(line, headingweightings, \
									 lineweightings[self.index(line)])
		if lineindexcounts[self.index(line)] < 3:
			sweepside = "too little data"
		rowdirections.append(sweepside)
	return rowdirections

def CellGrab(self, lineindexcount, headingindex, headingrowlength, \
			 headingindexvalue, lineformats, headingformats):
	queryindices = []
	itemmatch = ""

#	I tried to pull cells the way I would decide what cell belonged in a table
#	if I were looking a table which was lined up in a vertically uneven way.
# 	This string dictates where the function will look for responsive cells.
#	It points first at the proportional location of the searched row in 
#	comparison to the heading's position in the heading row (e.g. a heading 
#	halfway through the heading row would result in starting the search halfway
#	through the searched row.  Then it tries to find the first cell near there
#	that is formatted correctly.  Basically it looks at the target cell, then 
#	wags right and then left to find the thing and stops at the closest cell to
# 	the target, kind of like looking for something with a flashlight.) 
	firstqueryindex = max(0, min(len(self)-1, int(float(headingindex[\
		headingindexvalue]) * float(len(self)) / float(headingrowlength))))
	queryindices = [firstqueryindex, 
					max(0, min(len(self)-1, firstqueryindex + 1)), 
					max(0, min(len(self)-1, firstqueryindex - 1)), 
					max(0, min(len(self)-1, firstqueryindex + 2)), 
					max(0, min(len(self)-1, firstqueryindex - 2)), 
					max(0, min(len(self)-1, firstqueryindex + 3)), 
					max(0, min(len(self)-1, firstqueryindex - 3))]
	#print queryindices

	for x in range(len(queryindices)):
#		print "test self query indices[x]", self[queryindices[x]]
#		print "test self", self
		if self[queryindices[x]] != "" and \
		   (lineformats[queryindices[x]] == headingformats[headingindexvalue]\
		   or lineformats[queryindices[x]] == "n/a"):
			#print "confirm self query indices[x], x iteration", self[queryindices[x]], x

			itemmatch = self[queryindices[x]]
			self[queryindices[x]] = ""
			return itemmatch, self
	return "", self

# The right and left here are named this way because usually the equity info is
# on the right and the option info is on the left.   

def AllSweep(self, lineindexcount, headingindex, headingrowlength, lineformats,\
			 headingformats):
	resultrow = []
	for x in range(0, len(headingindex)):
		if headingindex[x] != "None":
			cellgrabfindings = CellGrab(self, lineindexcount, headingindex, \
										headingrowlength, x, lineformats, \
										headingformats)
			resultrow.append(cellgrabfindings[0])
			self = cellgrabfindings[1]
		if headingindex[x] == "None":
			resultrow.append("")
	return resultrow, self

#Built Left sweep off of right sweep
#def LeftSweep

#def FullSweep
#righttableheading = [y[0], y[1], x, len(self[x])]
def RowParser(self, headingindex, startrow, headingrowlength, \
			  sweeprowdirections, lineindexcounts, tableformats, \
			  headingformats):
#	print "here is the self", self
	resulttable = []
	rightheadings = [headingindex[0], 
					 headingindex[6], 
					 headingindex[7], 
					 headingindex[8], 
					 headingindex[9]]

	leftheadings = [headingindex[0], 
					headingindex[1], 
					headingindex[2], 
					headingindex[3], 
					headingindex[4], 
					headingindex[5]]
#To explain the below, this program runs separate loops for rows where there
#are only cells with only option or equity values.  This is designed to aid
#in keeping extraneous values out of the results.  Note that there are three
#IF loops below.  These are not necessary, because the only differences are the
#input heading indices.  However, I broke them out to make it easier to tell
#the program to pull different categories differently.  (e.g. we could easily 
#set up new functions to read from right to left, instead of left to right if
#we decide that will be useful). 
	for x in range(startrow + 1, len(self)):
		#print "here is the self again", self[x]
		resultrow = []
		if sweeprowdirections[x] == "Both":
			bothsweepresults = AllSweep(self[x], lineindexcounts[x], \
										headingindex, headingrowlength, \
										tableformats[x], headingformats)
			resultrow = bothsweepresults[0]
			self[x] = bothsweepresults[1]

		if sweeprowdirections[x] == "Right":
			rightsweepresults = AllSweep(self[x], lineindexcounts[x], \
								rightheadings, headingrowlength, \
								tableformats[x], headingformats)
			resultrow = [rightsweepresults[0][0], 
						  "", "", "", "", "",
						  rightsweepresults[0][1],
						  rightsweepresults[0][2],
						  rightsweepresults[0][3],
						  rightsweepresults[0][4]]
			self[x] = rightsweepresults[1]

		if sweeprowdirections[x] == "Left":
			leftsweepresults = AllSweep(self[x], lineindexcounts[x], \
										leftheadings, headingrowlength, \
										tableformats[x], headingformats)
			resultrow = [leftsweepresults[0][0], 
						 leftsweepresults[0][1],
						 leftsweepresults[0][2],
						 leftsweepresults[0][3],
						 leftsweepresults[0][4],
						 leftsweepresults[0][5],
						 "","","",""]
			self[x] = leftsweepresults[1]

		if sweeprowdirections[x] != "Both" and sweeprowdirections[x] != "Right"\
		and sweeprowdirections[x] != "Left":
			resultrow.append("Empty")
		resulttable.append(resultrow)
	return resulttable

# Error correction this function takes information on related columns.
# e.g. last cell and second to last cell must coexist, therefore,
# if the last cell and third to last cell are filled and the second
# to last row is empty, makes sense to assume the parser mistakenly 
# pulled the second to last value as the third to last -- this function
# corrects that problem


def BadRowStripper(matrix, properlength, minimumvalues):
	newmatrix = []
	for row in matrix:
		if len(row) == properlength and \
		row.count('') <= properlength - minimumvalues:
			newmatrix.append(row)
		if len(row) != properlength:
			print "Row is wrong length, so removed  : ", row
		if row.count('') > properlength - minimumvalues:
			print "Row has too few values so removed: ", row
	return newmatrix


def PairErrorCorrect(matrix, dominantcol, dominantpartner, mistakencol):
	for row in matrix:
		if len(row) == 10:
			if row[dominantcol] != '' and \
			row[dominantpartner] == '' and \
			row[mistakencol] != '':
				row[dominantpartner], row[mistakencol] = row[mistakencol], row[dominantpartner]
				print "Fixed row order for: ", row
	return matrix


#
# Main program starts here
#
CIKs = []
TablesFromFiles = []
rawfilemap = rawfilemapper()
headercolumnlist = columnlist()
nestedcollist = headercolumnlist[0]
flatcollist = headercolumnlist[1]
collistlength = headercolumnlist[2]

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
		parser = MyHTMLParser()
		parser.feed(table)
		parsedtable = parser.datastorage
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
	for table in parsedfiletables:
		for i in range(min(5, len(table))):
			wordmatchqualrow.append(headingfinder(table[i], flatcollist, \
									collistlength))
		if wordmatchqualrow == []:
			wordmatchqualrow = [0]
		wordmatchqualtable.append(wordmatchqualrow)
		wordmatchqualrow = []
	for i in range(len(tablecounts)):
		tablecounts[i] += max(wordmatchqualtable[i])*(2000)


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
		if isnumber(lowerfilestring[i:i+1]):
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
#	print "------------- NEW FILE -------------"
	f = open(htmlfile, 'r')
	parser = MyHTMLParser()
	parser.feed(f.read())
	parsematrix = parser.datastorage
	c = columnorderdetector(parsematrix)
# This specification should go somewhere else, but I'm not sure where to put it 
# without overcomplicating this script
	headingformats = ['name', 'float', 'float', 
					'float', 'float', 'date', 
					'float', 'float', 'float',
					'float']
	parsematrix = FootnoteRemover(parsematrix)
	parsematrix = ConvertNumbersToFloats(parsematrix)
	a = ExplicitTotalRemover(parsematrix, c[2])
	parsematrix = MissingNameAdder(parsematrix)

	numberandindexoflines = RowClassifier(parsematrix)	
	thetabletypes = CellTypes(parsematrix)
	SweepClassification = SweepClassifier(parsematrix, c[4], \
										  numberandindexoflines[1], \
										  numberandindexoflines[0])
	rowparseresults = RowParser(parsematrix, c[0], c[2], c[3], \
								SweepClassification, numberandindexoflines[0], \
								thetabletypes, headingformats)
	rowparseresults = BadRowStripper(rowparseresults, 10, 3)
	rowparseresults = PairErrorCorrect(rowparseresults, 9, 8, 7)
	rowparseresults = PairErrorCorrect(rowparseresults, 6, 7, 8)

	CIK = htmlfile[len(htmlfile)-14:len(htmlfile)-4]
	outputtarget = open((MainFolderLocation + "Output/" + "file" + \
						str(filecount) + CIK + ".txt"), 'w')
	outputtarget.truncate()
	filecount += 1
# Below is where the outputs are written into the output files
	
	print>>outputtarget, CIK
	print>>outputtarget, "Headings Corresponding to List Entries"
	for i in range(len(nestedcollist)):
		columnforprint = " ".join(nestedcollist[i])
		print>>outputtarget, columnforprint
	print>>outputtarget, c[0]
	if c[0] == "No Match Error, Can't Match Columns at Significance Hurdle":
		print>>outputtarget, ("\n\n\n" +
							  "On account of an error finding column matches, "+
							  "diagnostic results will be provided below.")
		print>>outputtarget, "\n\n\n\n\n\n\n\n\n\n"
		print>>outputtarget, "parsematrix:"
		print>>outputtarget, parsematrix
		print>>outputtarget, "\n\n\n\n\n"
		print>>outputtarget, "HTMLParser Data Storage"
		print>>outputtarget, parser.datastorage
	print>>outputtarget, " "
	for i in range(len(rowparseresults)):
		if rowparseresults[i] != ['Empty']:
			print>>outputtarget, rowparseresults[i]
	outputtarget.close()

#	print rowparseresults