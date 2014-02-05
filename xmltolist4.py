#This is a new function in this version. textattribute() handles attribute exceptions, 
#which we need when a tag is missing (e.g. there is no value in the expiration
#date of an option tranche.  I don't try to analyze here and just note errors)
def textattribute(function):
	try: 
		a = function.text
	except AttributeError:
		a = 'AttributeError'

	return a

def floattextattribute(function):
	try:
		a = float(function.text)
	except AttributeError:
		a = 'AttributeError'

	return a

		
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET


def xnparse(xmlfilename):
	#print "Parsing: ", xmlfilename

	#print "Type the filename of the file you want to parse (must be in the same directory as this script):"
	#filetoread = raw_input("> ")
	#The two lines below will just open the file and print it as text if you want to add them back
	#txt_again = open(filetoread)
	#print txt_again.read()
	#The below line pulls in the element tree functions in python and renames it ET
	
	#Below pulls the tree as an object (I think)
	tree = ET.parse(xmlfilename)
	#Below pulls the root element of the parsed string
	root = tree.getroot()
	#The root object has child nodes 
	#below nested loops iterate to find the non-derivative and then derivative transactions ("NonDerivXns")
	#First it defines the list then it constructs each transaction in order then it adds them to the list


	#One open question is: what about the footnotes? should we try to pull those in now or wait until later? 

	# So first, make an empty list (which will be a list of transaction data lists, that is a 2d list)
	NonDerivXns = []
	#10b5-1 note detector (in the whole Form 4)
	footnotenames = []
	for fnotes in root.findall('footnotes'):
		for fnote in fnotes.findall('footnote'):
			if '10b5-1' in fnote.text:
				footnotenames.append(fnote.get('id'))

	#Now iterate over each non-deriv transaction
	for child in root.findall('nonDerivativeTable'):
		#print "Found a child"
		
	#This finds each transaction, making a list of its attributes
		for  child2 in child.findall('nonDerivativeTransaction'):
			#print "Found a grandchild"
			NonDerivXn = ['err', 'err', 'err', 'err', 'err',
					   'err', 'err', 'err', 'err', 'err',
					   'err', 'err', 'err', 'err', 'err',
					   'err', 'err', 0]
			NonDerivXn[0] = textattribute(root.find('periodOfReport'))
			NonDerivXn[1] = textattribute(root.find('issuer/issuerCik'))
			NonDerivXn[2] = textattribute(root.find('reportingOwner/reportingOwnerId/rptOwnerCik'))
			NonDerivXn[3] = textattribute(root.find('reportingOwner/reportingOwnerId/rptOwnerName'))
			NonDerivXn[4] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/isDirector'))
			NonDerivXn[5] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/isOfficer'))
			NonDerivXn[6] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/isTenPercentOwner'))
			NonDerivXn[7] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/isOther'))
			NonDerivXn[8] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/officerTitle'))
			NonDerivXn[9] = textattribute(child2.find('securityTitle/value'))
			NonDerivXn[10] = textattribute(child2.find('transactionDate/value'))
			NonDerivXn[11] = textattribute(child2.find('transactionCoding/transactionCode'))
			NonDerivXn[12] = floattextattribute(child2.find('transactionAmounts/transactionShares/value'))
			NonDerivXn[13] = floattextattribute(child2.find('transactionAmounts/transactionPricePerShare/value'))
			NonDerivXn[14] = textattribute(child2.find('transactionAmounts/transactionAcquiredDisposedCode/value'))
			NonDerivXn[15] = floattextattribute(child2.find('postTransactionAmounts/sharesOwnedFollowingTransaction/value'))
			NonDerivXn[16] = textattribute(child2.find('ownershipNature/directOrIndirectOwnership/value'))
			#10b5-1 transaction finder
			for fnotereturn in child2.iter('footnoteId'):
				fnotenumber = fnotereturn.get('id')
				for fnotenumber in footnotenames:
					NonDerivXn[17] = 1
			#print NonDerivXn
			NonDerivXns.append(NonDerivXn)

	DerivXns = []

	#Now iterate over each deriv transaction
	for child in root.findall('derivativeTable'):
	#	print "Found a child"
		
	#This finds each transaction, making a list of its attributes
		for  child2 in child.findall('derivativeTransaction'):
	#		print "Found a grandchild"
			DerivXn = ['err', 'err', 'err', 'err', 'err',
					   'err', 'err', 'err', 'err', 'err',
					   'err', 'err', 'err', 'err', 'err',
					   'err', 'err', 'err', 'err', 'err',
					   0]
			DerivXn[0] = textattribute(root.find('periodOfReport'))
			DerivXn[1] = textattribute(root.find('issuer/issuerCik'))
			DerivXn[2] = textattribute(root.find('reportingOwner/reportingOwnerId/rptOwnerCik'))
			DerivXn[3] = textattribute(root.find('reportingOwner/reportingOwnerId/rptOwnerName'))
			DerivXn[4] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/isDirector'))
			DerivXn[5] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/isOfficer'))
			DerivXn[6] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/isTenPercentOwner'))
			DerivXn[7] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/isOther'))
			DerivXn[8] = textattribute(root.find('reportingOwner/reportingOwnerRelationship/officerTitle'))
			DerivXn[9] = textattribute(child2.find('securityTitle/value'))
			DerivXn[10] = textattribute(child2.find('transactionDate/value'))
			DerivXn[11] = textattribute(child2.find('transactionCoding/transactionCode'))
			DerivXn[12] = floattextattribute(child2.find('transactionAmounts/transactionShares/value'))
			DerivXn[13] = floattextattribute(child2.find('transactionAmounts/transactionPricePerShare/value'))
			DerivXn[14] = textattribute(child2.find('transactionAmounts/transactionAcquiredDisposedCode/value'))
			DerivXn[15] = textattribute(child2.find('expirationDate/value'))
			DerivXn[16] = textattribute(child2.find('underlyingSecurity/underlyingSecurityTitle/value'))
			DerivXn[17] = floattextattribute(child2.find('underlyingSecurity/underlyingSecurityShares/value'))
			DerivXn[18] = floattextattribute(child2.find('postTransactionAmounts/sharesOwnedFollowingTransaction/value'))
			DerivXn[19] = textattribute(child2.find('ownershipNature/directOrIndirectOwnership/value'))
			#10b5-1 transaction finder
			for fnotereturn in child2.iter('footnoteId'):
				fnotenumber = fnotereturn.get('id')
				for fnotenumber in footnotenames:
					DerivXn[20] = 1
			#print DerivXn
			DerivXns.append(DerivXn)

	#print "done with the function"
#This returns the two 2d lists as a tuple (so that we don't have to go 
# back and figure out which transactions were deriv/nonderiv)
	#print NonDerivXns, DerivXns
	return NonDerivXns, DerivXns

def form4testandparse(xmlfilename):
	results = ([], [])
	#Below pulls the tree as an object (I think)
	tree = ET.parse(xmlfilename)
	#Below pulls the root element of the parsed string
	root = tree.getroot()
	if textattribute(root.find('documentType')) == "4":
		#print "Found a Form 4"
		results = xnparse(xmlfilename)

	return results





