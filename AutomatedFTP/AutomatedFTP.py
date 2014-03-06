import os
from ftplib import FTP
import txttoxml

cwd = os.getcwd()

# Notes:
#
# 1. If you want to stop this program, be mindful of the implications of
#	 stopping a download in progress.  The best thing to do is to figure out
#	 what could have been downloading and delete it.  Partially downloaded
#	 files may raise unexpected exceptions or cause us to fail to capture data.  
#
# 2. If you get a 550 error from ftplib, record the error and send it to me.
#	 Unfortunately, sometimes these errors are an issue with the server on the
#	 other side. Because of how this script runs, if you get this error, you
#	 may find blank files in the form 4 storage sections.  Check for these 
#	 occassionally.  Also, if you get such an error/find empty storage files
#	 delete the empty files and re-run the program.  Definitely let me know
#	 if you get the error twice in a row, since that indicates a problem on our
#	 side.   
#
# 3. If you use this version of the program to start building indices on your 
#	 local drive, use only one CIK.  As you get more indices, each CIK adds
#	 a linear, but meaningful amount of processing time.  Therefore, it is most
#	 efficient to use only CIK one while building an index and add the other
#	 CIKs later.  Greater efficiency is on my to-do list.  
#
# 4. I don't know if there are any bad things that could happen if you open
#	 form 4s as they download, because they get converted and renamed; not sure
#	 if that could cause a problem.  Also, this program may not be windows
#	 friendly with the way the renaming works.  I don't think it will cause a
#	 problem on a windows machine, but if you try and it does, let me know.  

def inputq(questionstring, responses):
	answer = ''
	while not any(x == answer for x in responses):
		print questionstring, "(y/n)",
		answer = raw_input()
	return answer

def isfloat(data):
	try:
		a = float(data)
		a = True
	except:
		a = False
	return a

#
# Note: when downloading indices it is important to use the right procedure.
# download the .idx directly from the SEC as a .txt
# Otherwise you may confuse python's attempts to find by line
print "Welcome to the automated ftp script"
# quitbranch = inputq("Would you like to use the ftp script?", ['y', 'n'])
# if quitbranch == "n":
# 	print "Exiting"
# 	exit(0)
# print "still here"

if not(os.path.isfile('emailaddress.txt')):
	print "Let's start with locally storing your email address as an ftp password (you won't be logged in yet)."
	target = open(cwd + '/' + 'emailaddress.txt', 'w')
	print "Created an email address storage file in", cwd + '/' + 'emailaddress.txt'
	print "What is your email address? (for anonymous ftp password)"
	email = raw_input()
	print>>target, email
	target.close()
	print ''

indexdownload = inputq("Would you like to download some source indices not yet stored on this computer?", ['y', 'n'])
if indexdownload == 'y':
	print "Okay, we won't download these files just yet, but they will be a part of the ftp package"
	downloadchoice = inputq("Would you like to cap how many new indices you download at 10? (if not this could take a while, once we get past the first few years, 10 indices can be in the neighborhood of 400 mb)", ['y', 'n'])
	if downloadchoice == 'y':
		downloadcap = 10
	if downloadchoice == 'n':
		downloadcap = 10000000
if indexdownload == "n":
	print "On to the next question"
print " "
indexupdate = inputq("Would you like to replace the most recent quarterly source index and look for a newer one? (don't do this until you have downloaded all past source indices)", ['y', 'n'])
if indexupdate == 'y':
	print "Okay, we won't download this file just yet, but it will be a part of the ftp package"
if indexupdate == "n":
	print "On to the next question"
print " "
initializing = inputq("Would you like to do an initializing download?", ['y', 'n'])
if initializing == 'y':
	print "Okay, we will do an initializing download"
	update = 'n'
if initializing == "n":
	print "On to the next question" 
	update = inputq("Would you like to do an update download?", ['y', 'n'])
	if update == 'y':
		print "Okay, we will do an update download"
		print "What is the date of the update? (YYYYMMDD)"
		date = raw_input()
	if update == "n":
		print "On to the next question"



qindexfilelist = []
qindexdirectory = cwd + '/QFilingIndices/'

if not(os.path.exists(qindexdirectory)):
	os.makedirs(qindexdirectory)
	print "Created a directory: ", qindexdirectory

for filename in os.listdir(qindexdirectory):
	if filename.endswith('.txt'):
		qindexfilelist.append(qindexdirectory + filename)

dindexdirectory = cwd + '/DFilingIndices/'
if not(os.path.exists(dindexdirectory)):
	os.makedirs(dindexdirectory)
	print "Created a directory: ", dindexdirectory




print "What form would you like to use?"
print "Also, just press enter for form 4" 
form = raw_input()
if form == "":
	form = 4 
print "We'll work with form", form

formdir = form
if form == '4/A':
	formdir = '4A'



if initializing == 'y':
	CIKsInit = []
	# This only runs if there is no CIKsInit.txt file; if none exists,
	# it creates this file and populates it with '882095'
	if not(os.path.isfile('CIKsInit.txt')):
		target = open(cwd + '/' + 'CIKsInit.txt', 'w')
		print>>target, '882095'
		target.close()

	with open("CIKsInit.txt") as infile:
		for line in infile:
			CIKsInit.append(line.strip())
	print "Using initialization CIKs:", CIKsInit
	print " "
	# Makes the storage directories if they are missing/not yet created
	for CIK in CIKsInit:
		directory = "storage/" + str(CIK) + '/' + str(formdir)
		if not(os.path.exists(directory)):
			os.makedirs(directory)
			print "Created a directory: ", directory




if update == 'y':
	CIKsUpdate = []
	# This only runs if there is no CIKsUpdate.txt file; if none exists,
	# it creates this file and populates it with '882095'
	if not(os.path.isfile('CIKsUpdate.txt')):
		target = open(cwd + '/' + 'CIKsUpdate.txt', 'w')
		print>>target, '882095'
		target.close()

	with open("CIKsUpdate.txt") as infile:
		for line in infile:
			CIKsUpdate.append(line.strip())
	print "Using update CIKs:", CIKsUpdate
	print " "
	# Makes the storage directories if they are missing/not yet created
	for CIK in CIKsUpdate:
		directory = "storage/" + str(CIK) + '/' + str(formdir)
		if not(os.path.exists(directory)):
			os.makedirs(directory)
			print "Created a directory: ", directory




print "Okay, let's download the files we need from the SEC site."
#print "This script will rebuild its index of files for each CIK."
#print "If any source forms on the new index have not yet been downloaded,"
#print "the script will attempt to download those forms."
#print "The first several times you run this script, it will be fast, but"
#print "Over time it will slow down substantially, because the indices will"
#print "become larger and related files will become more numerous"

runftp = inputq("Would you like to continue?", ['y', 'n'])
if runftp == 'y':
	print "Okay, let's get started"
if runftp == "n":
	print "Okay, quitting"
	exit(0)


if runftp == 'y':
	print "Logging on to the SEC site for index download"
	try:
		target = open(cwd + '/' + 'emailaddress.txt')
		email = target.read()
		email = email.strip()
		target.close()
		ftp = FTP('ftp.sec.gov') 
		ftp.login('anonymous', email)
		print "Connected"
	except:
		print "Cannot connect, quitting"
		exit(0)

qindexbasepath = "/edgar/full-index"

if indexupdate == 'y':
	mostrecentindex = max(qindexfilelist)
	
	templength = len(mostrecentindex)
	mostrecentindex = mostrecentindex[templength - 10: templength]
	
	latestyear = mostrecentindex[:4]
	latestquarter = 'QTR' + mostrecentindex[5]
	try:
		ftp.cwd(qindexbasepath + "/" + latestyear + "/" + latestquarter)
		local_filename = os.getcwd() + "/QFilingIndices/" + latestyear + "Q" + latestquarter[3] + ".txt"
		target = open(local_filename, 'wb')
		ftp.retrbinary('RETR %s' % "form.idx", target.write) 
		target.close

	except: 
		print "Can't get file for ", mostrecentindex

	if latestquarter == "QTR4":
		checkyear = str(int(latestyear) + 1)
		checkquarter = 'QTR1'
	if latestquarter != "QTR4":
		checkyear = latestyear
		checkquarter = 'QTR' + str(int(latestquarter[3]) + 1)
	print checkyear, checkquarter
	try:
		ftp.cwd(qindexbasepath + "/" + checkyear + "/" + checkquarter)
		local_filename = os.getcwd() + "/QFilingIndices/" + checkyear + "Q" + checkquarter[3] + ".txt"
		target = open(local_filename, 'wb')
		ftp.retrbinary('RETR %s' % "form.idx", target.write) 
		target.close

	except: 
		print "No index for a newer quarter"




download = 0
if indexdownload == 'y':
	
	ftp.cwd(qindexbasepath)
	print "now in /edgar/full-index directory" 
	indexyearlist = []
	ftp.retrlines('nlst', indexyearlist.append)
	print "Single level index directory now generated"
	templist = []
	for entry in indexyearlist:
		if len(entry) < 5 and isfloat(entry):
			templist.append(entry)
	indexyearlist = templist
	print "Now going to go one level deeper and begin to save any missing indices..."
	fullqindexdirectory = []
	downloadcounter = 1
	for year in indexyearlist:
		quarterlist = []
		# print "building subdirectory ", year
		
		ftp.cwd(qindexbasepath + "/" + year)
		ftp.retrlines('nlst', quarterlist.append)
		fullqindexdirectory.append(quarterlist)


		templist = []
		for quarter in quarterlist:
			if len(quarter) < 5 and quarter.startswith('QTR'):
				templist.append(quarter)
		quarterlist = templist	

		
		for quarter in quarterlist:
			
			if not any(existingindex.find(year + 'Q' + quarter[3] + '.txt') != -1 for existingindex in qindexfilelist):
				print '\t' + str(downloadcounter) + ". Trying to download:", year + 'Q' + quarter[3], "..."				
				downloadcounter += 1
				try:
					ftp.cwd(qindexbasepath + "/" + year + "/" + quarter)
					local_filename = os.getcwd() + "/QFilingIndices/" + year + "Q" + quarter[3] + ".txt"
					target = open(local_filename, 'wb')
					ftp.retrbinary('RETR %s' % "form.idx", target.write)
					target.close()
					download += 1
					print '\t\tdone'
				except: 
					print "Can't get file in ", year + ' ' +  quarter

			if download > downloadcap-1:
				break
		if download > downloadcap-1:
			break
	print "Done with index file download attempt"

dindexbasepath = "/edgar/daily-index"
if update == 'y':
	print "Downloading daily index..."
	try:
		ftp.cwd(dindexbasepath)
		local_filename = os.getcwd() + "/DFilingIndices/" + date + ".txt"
		target = open(local_filename, 'wb')
		ftp.retrbinary('RETR %s' % ("form." + date + ".idx"), target.write)
		target.close()
		
		print '\t\tdone'
	except: 
		print "Can't get file in ", date

ftp.close()
qindexfilelist = []
for filename in os.listdir(qindexdirectory):
	if filename.endswith('.txt'):
		qindexfilelist.append(qindexdirectory + filename)


print "Now lets generate the list of forms we need from the indices we have."


#	print "\t Working on:", CIK

if initializing == 'y':
	for CIK in CIKsInit:
		target = open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' + str(formdir) + '.txt', 'w')	
		target.close()
	#	formfilelist = []
		
		i = 0
	LastCIK = '911911911911911911911911911'
	for index in qindexfilelist:

		with open(index) as infile:
			for line in infile:
				if line.find(' ' + str(LastCIK) + ' ') != -1 and line.find(str(form)+'  ') == 0:
					
					formfilename = line[line.find("edgar/data/"):len(line)]
					formfilename = formfilename.rstrip()
					print>>target, formfilename

				elif line.find(str(form)+'  ') == 0:
					for CIK in CIKsInit:
						if line.find(' ' + str(CIK) + ' ') != -1:
							target.close()
							target = open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' + str(formdir) + '.txt', 'a')
							LastCIK = CIK
							formfilename = line[line.find("edgar/data/"):len(line)]
							formfilename = formfilename.rstrip()
							print>>target, formfilename
	#					formfilelist.append(formfilename)
		
		target.close()
		LastCIK = '911911911911911911911911911'

if update == 'y':
	for CIK in CIKsUpdate:
		target = open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' + str(formdir) + 'update.txt', 'w')	
		target.close()
	#	formfilelist = []
		
		i = 0
	LastCIK = '911911911911911911911911911'
	with open(os.getcwd() + "/DFilingIndices/" + date + ".txt") as infile:
		for line in infile:
			if line.find(' ' + str(LastCIK) + ' ') != -1 and line.find(str(form)+'  ') == 0:
				
				formfilename = line[line.find("edgar/data/"):len(line)]
				formfilename = formfilename.rstrip()
				print>>target, formfilename

			elif line.find(str(form)+'  ') == 0:
				for CIK in CIKsUpdate:
					if line.find(' ' + str(CIK) + ' ') != -1:
						target.close()
						target = open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' + str(formdir) + 'update.txt', 'a')
						LastCIK = CIK
						formfilename = line[line.find("edgar/data/"):len(line)]
						formfilename = formfilename.rstrip()
						print>>target, formfilename
#					formfilelist.append(formfilename)
	
	target.close()
	LastCIK = '911911911911911911911911911'
	for CIK in CIKsUpdate:
		with open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' + str(formdir) + 'update.txt') as sourcefile:
			target = open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' + str(formdir) + '.txt', 'a+')
			targetstring = target.read()
			for line in sourcefile:
				if targetstring.find(line.strip()) == -1:
					print>>target, line.strip()
			target.close()
		
if initializing == 'y' or update == 'y':
	print "Logging in to the SEC site to download source files"
	# The purpose of logging in and out twice is because it seems like the SEC ftp 
	# site stops responding wait too long in between requests.  There is a 
	# significant amount of processing time involved in getting from the raw index 
	# lists to indices for each CIK
	try:
		target = open(cwd + '/' + 'emailaddress.txt')
		email = target.read()
		email = email.strip()
		target.close()
		ftp = FTP('ftp.sec.gov') 
		ftp.login('anonymous', email)
		print "Connected"
	except:
		print "Cannot connect, quitting"
		exit(0)

if initializing == 'y':

	for CIK in CIKsInit:
		ftpbasedirectory = '/edgar/data/' + str(CIK)

		

		existingfilestring = os.listdir(cwd + '/' + "storage/" + str(CIK) + '/' + str(formdir) + '/')
		
		tempfilestring = []

		for item in existingfilestring:
			if item.endswith('.xml') or item.endswith('.txt'):
				reformatlocation = item.find('-')
				tempfilestring.append(item[:reformatlocation] + '/' + item[reformatlocation + 1:len(item)-4])
		existingfilestring = tempfilestring
		

		
		#print ftpbasedirectory
		#ftp.cwd(ftpbasedirectory)

		with open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' + str(formdir) + '.txt') as sourcefile:
			print "CIK loop", CIK
			
			for line in sourcefile:

				
				if not any(line.find(existingfile) != -1 for existingfile in existingfilestring):
					
					try:
						
						namestart = line.find('/', len("edgar/data/"))
						filerCIK = line[len("edgar/data/"):namestart]
						#print line[0:namestart]
						#workingdirectory = ('/' + line[0:namestart]).strip()
						#ftp.cwd(workingdirectory)
						filepath = line.strip()
						endline = filepath.find('.txt')
						filename = filepath[namestart + 1:endline+1]
						local_filename = os.getcwd() + "/" + "storage/" + str(CIK) + '/' + str(formdir) + '/' + filerCIK + '-' + filename + "txt"
						target = open(local_filename, 'wb')
						
						ftp.retrbinary('RETR ' + filepath, target.write)
						target.close()
					except: 
						print "Can't get file in:", line


if update == 'y':

	for CIK in CIKsUpdate:
		ftpbasedirectory = '/edgar/data/' + str(CIK)

		

		existingfilestring = os.listdir(cwd + '/' + "storage/" + str(CIK) + '/' + str(formdir) + '/')
		
		tempfilestring = []

		for item in existingfilestring:
			if item.endswith('.xml') or item.endswith('.txt'):
				reformatlocation = item.find('-')
				tempfilestring.append(item[:reformatlocation] + '/' + item[reformatlocation + 1:len(item)-4])
		existingfilestring = tempfilestring
		

		
		#print ftpbasedirectory
		#ftp.cwd(ftpbasedirectory)

		with open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' + str(formdir) + 'update.txt') as sourcefile:
			print "CIK loop", CIK
			
			for line in sourcefile:

				
				if not any(line.find(existingfile) != -1 for existingfile in existingfilestring):
					
					try:
						
						namestart = line.find('/', len("edgar/data/"))
						filerCIK = line[len("edgar/data/"):namestart]
						#print line[0:namestart]
						#workingdirectory = ('/' + line[0:namestart]).strip()
						#ftp.cwd(workingdirectory)
						filepath = line.strip()
						endline = filepath.find('.txt')
						filename = filepath[namestart + 1:endline+1]
						local_filename = os.getcwd() + "/" + "storage/" + str(CIK) + '/' + str(formdir) + '/' + filerCIK + '-' + filename + "txt"
						target = open(local_filename, 'wb')
						
						ftp.retrbinary('RETR ' + filepath, target.write)
						target.close()
					except: 
						print "Can't get file in:", line

print "done"

# This block rearranges the index filepaths to the form the SEC uses for .xml filing
# It is different in a nontrivial way because the sec stores the .xml files in nested folders.  
#				accstart = line.find('/', len("edgar/data/"))
			# 	foldstart = line.find('-')
			# 	identstart = line.find('-', foldstart + 1)
			# 	identend = line.find('.')
			# 	accession = line[accstart+1:foldstart]
			# 	yearfolder = line[foldstart+1:identstart]
			# 	identifier = line[identstart+1:identend]


			# 	ftp.cwd(ftpbasedirectory + "/" + yearfolder + '/' + accession + yearfolder + identifier)
			# 	cwddirectory = []
			# 	ftp.retrlines('nlst', cwddirectory.append)
			# 	for y in cwddirectory:
			# 		if y.find('.xml') != -1:
			# 			local_filename = os.getcwd() + "/" + "storage/" + str(CIK) + '/' + str(form)+ '/' + yearfolder + "-" + accession + identifier + ".xml"
			# 			target = open(local_filename, 'wb')
			# 			ftp.retrbinary('RETR %s' % str(y), target.write)
			# 	target.close
			# except: 
			# 	print "Can't get file in ", ftpbasedirectory + "/" + yearfolder + '/' + accession + yearfolder + identifier

ftp.close()
print "FTP connection closed"
if initializing == 'y':
	txttoxml.processxml(cwd, formdir, CIKsInit)
	print "Saved files converted from .txt to .xml"
if update == 'y':
	txttoxml.processxml(cwd, formdir, CIKsUpdate)
	print "Saved files converted from .txt to .xml"


