import json


# Form 4 direct ownership, this could be replaced by a tailored call for only
# direct ownership entries from the DB

def xnreader(filename):
	target = open(filename)
	content = json.load(target)
	return  content

def keyattribs(entry):
	attribs = []
	try: 
		if entry[15] == 'A':
			attribs.append(entry[13])
		if entry[15] == 'D':
			attribs.append(-entry[13])
		if entry[15] != 'A' and entry[15] != 'D':
			attribs.append('A/D Coding Error')
		attribs.append(entry[19])
		attribs.append(entry[11])
		# attribs.append(entry[15])
		attribs.append(entry[22])
		attribs.append(entry[0])
		attribs.append(entry[1])
		attribs.append(entry[2])

	except:
		attribs.append('Error')
	return attribs

def ConvertListByForm(listbyxn):
	ListByForm = []
	XnList = []
	lastfilename = 'Dummy filename'
	for entry in listbyxn:
		if entry[20] == 'D':
			if entry[23] != lastfilename:
				ListByForm.append(XnList)
				XnList = []
				XnList.append(keyattribs(entry))
			if entry[23] == lastfilename:
				XnList.append(keyattribs(entry))
			lastfilename = entry[23]
	ListByForm.append(XnList)
	ListByForm.pop(0)
	return ListByForm

def threadconverter(listbyform):

	ThreadsList = []

	for form in listbyform:
		formthreads = []
		thread = []
		lastremaining = -1000000
		for entry in form:
			# print "Look here"
			if entry[1] != 'AttributeError' and entry[0] != 'AttributeError':
				if entry[1]-entry[0] == lastremaining:
					thread.append(entry)
				if entry[1]-entry[0] != lastremaining:
					formthreads.append(thread)
					thread = []
					thread.append(entry)
				lastremaining = entry[1]
		formthreads.append(thread)
		formthreads.pop(0)
		ThreadsList.append(formthreads)

	return ThreadsList


form4Xns = xnreader('NonDerivXn4File.txt')
form4AXns = xnreader('NonDerivXn4AFile.txt')

Form4s = ConvertListByForm(form4Xns)
Form4As = ConvertListByForm(form4AXns)



#print 'Form4s', Form4s
#print 'Form4As', Form4As



Form4Threads = threadconverter(Form4s)

# for form in Form4Threads:
# 	for thread in form:
# 		for entry in thread:
# 			print entry
print ""
print ""
Form4AThreads = threadconverter(Form4As)

# for form in Form4As:
# 	for entry in form:
# 		print entry


# for form in Form4AThreads:
# 	for thread in form:
# 		for entry in thread:
# 			print entry
# for entry in Form4As:


Form4AIndices = []
Form4AResults = []
for form in Form4As:
	Form4AIndices.append(form[0][4] + '-' + form[0][5] + '-' + form[0][6])
	Form4AResults.append("")
Form4Indices = []
for form in Form4s:
	Form4Indices.append(form[0][4] + '-' + form[0][5] + '-' + form[0][6])

Form4ADict = dict(zip(Form4AIndices, Form4As))
# print Form4ADict

Form4Dict = dict(zip(Form4Indices, Form4s))
# print Form4Dict

Form4AResultsDict = dict(zip(Form4AIndices, Form4AResults))
Form4AThreadMatches = dict(zip(Form4AIndices, []))
Form4ThreadsDict = dict(zip(Form4Indices, Form4Threads))
Form4AThreadsDict = dict(zip(Form4AIndices, Form4AThreads))
# print Form4AResultsDict

for key in Form4AIndices:
	Threads4A = Form4AThreadsDict[key]
	try: 
		Transactions4 = Form4Dict[key]
	except:	
		Transactions4 = "Form 4A Key Error"
	balances4 = []
	for xn in Transactions4:
		try:
			balances4.append(xn[1] - xn[0])
		except:
			balances4.append('Error')
	threadmatches = []
	for thread4A in Threads4A:
		threadmatch = [i for i, x in enumerate(balances4) if x == thread4A[0][1] - thread4A[0][0]]
		if threadmatch == []:
			threadmatch = 'None'
		threadmatches.append(threadmatch)


	Form4AThreadMatches[key] = threadmatches
# print "Form4AThreadMatches", Form4AThreadMatches
# print len(Form4AThreadMatches)
# print len(Form4AThreads)
# print len(Form4As)

# print Form4AThreads

Form4AXnMatches = []
for formkey in Form4AThreadMatches:
	LastMatch = -1
	print "Form4AThreadMatches[formkey]", formkey, Form4AThreadMatches[formkey]
	# for ThreadMatch in Form4AThreadMatches[formkey]:
		# print 'ThreadMatch[0]', ThreadMatch[0]
		# print 'Form4AThreadsDict[formkey]', Form4AThreadsDict[formkey]
	for thread in Form4AThreadsDict[formkey]:
		print 'thread', thread
		print 'Form4AThreadMatches[formkey]', Form4AThreadMatches[formkey]
		
		ThreadMatch = Form4AThreadMatches[formkey][Form4AThreadsDict[formkey].index(thread)]
		print "threadmatch", ThreadMatch
		xncounter = 0
		# print "thread", thread
		for transaction in thread:
			# print thread
			# print 'transaction', transaction
			# print 'ThreadMatch', ThreadMatch
			try:
				XnMatchInfo = []
				XnMatchInfo.append(formkey)
				XnMatchInfo.append(transaction[3])
				if xncounter + int(ThreadMatch[0]) <= LastMatch:
				 	XnMatchInfo.append('earlier 4/A xn match supersedes')

				if xncounter + int(ThreadMatch[0]) > LastMatch:
					XnMatchInfo.append(xncounter + int(ThreadMatch[0]))
					LastMatch = xncounter + int(ThreadMatch[0])
				xncounter += 1
				Form4AXnMatches.append(XnMatchInfo)
			except:
				Form4AXnMatches.append(str(transaction) + 'ThreadMatch Indices: ' + str(ThreadMatch) + "; Form 4A Logic Matching Error, either no valid thread match or the valid thread match was used by an earlier transaction")


for transactionmatch in Form4AXnMatches:
	print transactionmatch
print len(Form4AXnMatches)

target = open("Form4AMatchIndex.txt", 'w')
json.dump(Form4AXnMatches, target)
target.close()

# threadmatches = []
# for form in Form4AThreads:
# 	threadinsertions = []
# 	threadterminations = []
# 	for thread in form:
# 		if 

# 		if thread[0][1] - thread[0][1] == 

# Form 4 shares remaining [start, after 1, after 2, ...]



# for entry in form4AXns:
# 	print "Orig Form 4 Date", entry[0]
# 	print "Xn Date", entry[11]
# 	print "Shares in Transaction", entry[13]
# 	print "Acquisition or Disposition?", entry[15]
# 	print "Shares Owned Following Transaction", entry[19]
# 	print "Nonderivative Transaction Number (on that Form 4)", entry[22]
# 	