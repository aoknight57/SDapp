
import xmltolist4
import xmlmanager

print "test"

#Here the program begins
print "Welcome to the nonderivative transaction parser"
ndxnlist = []
dxnlist = []
xmlfiledirectory = xmlmanager.filemapper()
#Here is the magic where we call the xnparser, 
i = 0
ndxncounter = 0
dxncounter = 0
bothcounter = 0
eithercounter = 0
notcounter = 0
#nullxnlist = ([], [])
for xmlfile in xmlfiledirectory: 
	newxnlist = xmltolist4.form4testandparse(xmlfile)
	ndxnlist += newxnlist[0]
	dxnlist	+= newxnlist[1]
	if newxnlist[0] != []:
		ndxncounter += 1
	if newxnlist[1] != []:
		dxncounter += 1
	if (newxnlist[0] != []) and (newxnlist[1] != []):
		bothcounter += 1
	if (newxnlist[0] != []) or (newxnlist[1] != []):
		eithercounter += 1
	if (newxnlist[0] == []) and (newxnlist[1] == []):
		notcounter += 1
		#newerrorchecker = xmltolist4.xnparse(xmlfile)
		#nullxnlist += newerrorchecker
		#if newerrorchecker[0] != [] or newerrorchecker[1] != []:
		#	print xmlfile

	i += 1

print "how many times did the for loop run?"
print i
print "bothcounter", bothcounter
print "eithercounter", eithercounter
print "notcounter", notcounter
#print "nullxnlist", nullxnlist
print "how many times did we add to the deriv and nonderiv xn lists, respectively"
print ndxncounter, dxncounter
print "So what did the parser give us, let's print an indication"
print "Here is the length of the non-derivative transaction list: ",
print len(ndxnlist)
print "Here is the length of the derivative transaction list: ",
print len(dxnlist)
print ndxnlist[1][2]
print "Let's save John C. Martin's entries, his CIK is: 0001190578"
#NonDeriv xn file for John C. Martin
i = 0
j = 0
JohnCMartinNDXlist = []
target = open("NonDerivXnFile.txt", 'w')
target.truncate()
#
print>>target, """Derivative Transcation List Key:
NonDerivXn[0] = Period Of Report
NonDerivXn[1] = Issuer CIK
NonDerivXn[2] = Reporting Owner CIK
NonDerivXn[3] = Reporting Owner Name
NonDerivXn[4] = Is the Reporting Owner a Director?
NonDerivXn[5] = Is the Reporting Owner an Officer?
NonDerivXn[6] = Is the Reporting Owner a Ten Percent Owner?
NonDerivXn[7] = Is the Reporting Owner Something Else?
NonDerivXn[8] = Reporting Owner Officer Title
NonDerivXn[9] = Security Title
NonDerivXn[10] = Transaction Date
NonDerivXn[11] = Transaction Code
NonDerivXn[12] = Shares in Transaction
NonDerivXn[13] = Transaction Price Per Share
NonDerivXn[14] = Transaction Acquired/Disposed Code
NonDerivXn[15] = Shares Owned Following Transaction
NonDerivXn[16] = Direct Or Indirect Ownership
NonDerivXn[17] = 1 if a "10b5-1" footnote is present
NonDerivXn[18] = Nonderivative Transaction Number (on that Form 4)

"""
#
for entry in ndxnlist:
	i += 1
	
	if entry[2] == '0001190578':
		j += 1
		print>>target, entry
print i
print j
target.close()

#Deriv xn file for John C. Martin
i = 0
j = 0
JohnCMartinDXlist = []
target = open("DerivXnFile.txt", 'w')
target.truncate()
print>>target, """Derivative Transcation List Key:
DerivXn[0] = Period Of Report
DerivXn[1] = Issuer CIK
DerivXn[2] = Reporting Owner CIK
DerivXn[3] = Reporting Owner Name
DerivXn[4] = Is the Reporting Owner a Director?
DerivXn[5] = Is the Reporting Owner an Officer?
DerivXn[6] = Is the Reporting Owner a Ten Percent Owner?
DerivXn[7] = Is the Reporting Owner Something Else?
DerivXn[8] = Reporting Owner Officer Title
DerivXn[9] = Security Title
DerivXn[10] = Transaction Date
DerivXn[11] = Transaction Code
DerivXn[12] = Shares in Transaction
DerivXn[13] = Transaction Price Per Share
DerivXn[14] = Transaction Acquired/Disposed Code
DerivXn[15] = Expiration Date
DerivXn[16] = Underlying Security Title
DerivXn[17] = Underlying Security Shares
DerivXn[18] = Shares Owned Following Transaction
DerivXn[19] = Direct Or Indirect Ownership
DerivXn[20] = 1 if a "10b5-1" footnote is present
DerivXn[21] = Derivative Transaction Number (on that Form 4)

"""
for entry in dxnlist:
	i += 1
	
	if entry[2] == '0001190578':
		j += 1
		print>>target, entry
print i
print j
target.close()
print "Done with the program"


# In case you have a hard time starting up the program, here is what 
# the output looks like:

#[['2014-01-02', '0000882095', '0001190578', 'MARTIN JOHN C',
# 'Common Stock', '2014-01-02', 'M', 140625, 8.005, 'A', 4197746],
# ['2014-01-02', '0000882095', '0001190578', 'MARTIN JOHN C',
# 'Common Stock', '2014-01-02', 'S', 140625, 75.0235, 'D',
# 4057121]]

#This drops the code into lists of lists (it looks like
#sometimes people call these 2d lists)
#5 minutes of research indicates that this may be fairly 
#Straightforward to put into mysql, but I have not learned
#much about it yet, so I don't know if that will be done
#as easily as I just said it.  