import os
from ftplib import FTP
import txttoxml
import datetime

cwd = os.getcwd()

# Notes:
#
# 1. If you want to stop this program, be mindful of the implications of
#	 stopping a download in progress.  The best thing to do is to figure out
#	 what could have been downloading and delete them.  Partially downloaded
#	 files may raise unexpected exceptions or cause us to fail to capture data.  
#
# 2. If you have never run this script before, run AutomatedFTP.py through at
#    least once first.  It will prompt for and create any missing ancillary 
#    files.  
#
# 3. The process of generating an index of all necessary filings takes some
#	 time, so consider removing CIKs from the CIKsInit.txt file after they
#	 have been initialized.  
#
# 4. Ensure that you have the latest quarterly index before running this script
#	 or the initialization will work off of an incomplete starting list.  If
#	 you notice this mistake, let the initialization finish, use 
#	 AutomatedFTP.py to update the quarterly indices and then run it again.  
#	 Initialization will fill in only the missed files if it is run again.  


print cwd


def ftplogin():
	try:
		target = open(cwd + '/' + 'emailaddress.txt')
		email = target.read()
		email = email.strip()
		target.close()
		ftp = FTP('ftp.sec.gov') 
		ftp.login('anonymous', email)
		return ftp
		print "Connected"
	except:
		print "Cannot connect, quitting"
		exit(0)

def ftpdownload(filepath, local_filename):
	try:
		target = open(local_filename, 'wb')
		ftp.retrbinary('RETR %s' % filepath, target.write)
		target.close()
		
	except: 
		print "Can't get file in ", filepath

def isfloat(data):
	try:
		a = float(data)
		a = True
	except:
		a = False
	return a

print "Initializing download..."

qindexfilelist = []
qindexdirectory = cwd + '/QFilingIndices/'
for filename in os.listdir(qindexdirectory):
	if filename.endswith('.txt'):
		qindexfilelist.append(qindexdirectory + filename)


if not(os.path.isfile('emailaddress.txt')):
	print "No email address file exists, please run AutomatedFTP.py", 
	print "Since there is no stored email file, the script can't login."
	print "Quitting..."
	exit(0)

target = open(cwd + '/' + 'testfile.txt', 'w')
print>>target, 'test initialization text is here'
target.close()

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

if not(os.path.isfile('InitLog.txt')):
	target = open(cwd + '/' + 'InitLog.txt', 'w')
	target.close()

forms = ['3', '3/A', '4', '4/A', '5', '5/A']
for form in forms:
	formdir = form
	if formdir == '3/A':
		formdir = '3A'
	if formdir == '4/A':
		formdir = '4A'
	if formdir == '5/A':
		formdir = '5A'
	for CIK in CIKsInit:
		directory = "storage/" + str(CIK) + '/' + str(formdir)
		target = open(cwd + '/' + 'InitLog.txt', 'a+')
		print>>target, CIK, "Form", form, datetime.datetime.today()
		target.close()
		if not(os.path.exists(directory)):
			os.makedirs(directory)
			print "Created a directory: ", directory



for form in forms:
	print "Form", form
	formdir = form
	if formdir == '3/A':
		formdir = '3A'
	if formdir == '4/A':
		formdir = '4A'
	if formdir == '5/A':
		formdir = '5A'

	for CIK in CIKsInit:
		target = open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + \
			'form' + str(formdir) + '.txt', 'w')	
		target.close()		
		i = 0
	LastCIK = '911911911911911911911911911'
	for index in qindexfilelist:

		with open(index) as infile:
			for line in infile:
				if line.find(' ' + str(LastCIK) + ' ') != -1 and \
				line.find(str(form)+'  ') == 0:
					formfilename = line[line.find("edgar/data/"):len(line)]
					formfilename = formfilename.rstrip()
					print>>target, formfilename

				elif line.find(str(form)+'  ') == 0:
					for CIK in CIKsInit:
						if line.find(' ' + str(CIK) + ' ') != -1:
							target.close()
							target = open(cwd + '/' + "storage/" + str(CIK) + \
								'/' + str(CIK) + 'form' + str(formdir) + \
								'.txt', 'a')
							LastCIK = CIK
							formfilename = line[line.find("edgar/data/"):\
								len(line)]
							formfilename = formfilename.rstrip()
							print>>target, formfilename		
		target.close()
		LastCIK = '911911911911911911911911911'
	ftp = ftplogin()
	for CIK in CIKsInit:
		ftpbasedirectory = '/edgar/data/' + str(CIK)	
		existingfilestring = os.listdir(cwd + '/' + "storage/" + str(CIK) + '/'\
			+ str(formdir) + '/')		
		tempfilestring = []
		for item in existingfilestring:
			if item.endswith('.xml') or item.endswith('.txt'):
				reformatlocation = item.find('-')
				tempfilestring.append(item[:reformatlocation] + '/' + \
					item[reformatlocation + 1:len(item)-4])
		existingfilestring = tempfilestring
		
		with open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' +\
		str(formdir) + '.txt') as sourcefile:
			print "CIK loop", CIK
			for line in sourcefile:				
				if not any(line.find(existingfile) != -1 for existingfile in \
				existingfilestring):
					namestart = line.find('/', len("edgar/data/"))
					filerCIK = line[len("edgar/data/"):namestart]
					filepath = line.strip()					
					endline = filepath.find('.txt')
					filename = filepath[namestart + 1:endline+1]
					local_filename = (os.getcwd() + "/" + "storage/" + str(CIK)\
						+ '/' + str(formdir) + '/' + filerCIK + '-' + filename\
						+ "txt")
					ftpdownload(filepath, local_filename)
	ftp.close()
	txttoxml.processxml(cwd, formdir, CIKsInit)
	print "Saved files converted from .txt to .xml"


print "...done"

