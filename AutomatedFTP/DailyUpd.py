import os
from ftplib import FTP
import txttoxml
import datetime

cwd = os.getcwd()
dindexbasepath = "/edgar/daily-index"


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

print "Nightly SEC download running..."

dindexdirectory = cwd + '/DFilingIndices/'

if not(os.path.isfile('emailaddress.txt')):
	print "No email address file exists, please run AutomatedFTP.py", 
	print "Since there is no stored email file, the script can't login."
	print "Quitting..."
	exit(0)

target = open(cwd + '/' + 'testfile.txt', 'w')
print>>target, 'test update text is here'
target.close()

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
forms = ['3', '3/A', '4', '4/A', '5', '5/A']
for form in forms:
	formdir = form
	if formdir == '3/A':
		formdir = '3A'
	if formdir == '4/A':
		formdir = '4A'
	if formdir == '5/A':
		formdir = '5A'
	for CIK in CIKsUpdate:
		directory = "storage/" + str(CIK) + '/' + str(formdir)
		if not(os.path.exists(directory)):
			os.makedirs(directory)
			print "Created a directory: ", directory



today = datetime.date.today()
date = today - datetime.timedelta(1)
print date
date = date.isoformat()
date = date[:4] + date[5:7] + date[8:10]

if not(os.path.isfile('UpdateLog.txt')):
	target = open(cwd + '/' + 'UpdateLog.txt', 'w')
	target.close()

target = open(cwd + '/' + 'UpdateLog.txt', 'r')
targetstring = target.read()
ftp = ftplogin()
if targetstring.find(date) == -1:
	print "Downloading daily index..."
	sourcename = "form." + date + ".idx"
	local_filename = os.getcwd() + "/DFilingIndices/" + date + ".txt"
	try:
		ftpdownload(dindexbasepath + '/' + sourcename, local_filename)
		target = open(cwd + '/' + 'UpdateLog.txt', 'a+')
		print>>target, sourcename, datetime.datetime.today()
		target.close()
	except:
		print "Could not download daily index"
		exit(0)

for form in forms:
	print "Form", form
	formdir = form
	if formdir == '3/A':
		formdir = '3A'
	if formdir == '4/A':
		formdir = '4A'
	if formdir == '5/A':
		formdir = '5A'
	for CIK in CIKsUpdate:
		target = open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + \
			'form' + str(formdir) + 'update.txt', 'w')	
		target.close()
		i = 0
	LastCIK = '911911911911911911911911911'
	with open(os.getcwd() + "/DFilingIndices/" + date + ".txt") as infile:
		for line in infile:
			if line.find(' ' + str(LastCIK) + ' ') != -1 and \
			line.find(str(form) + '  ') == 0:				
				formfilename = line[line.find("edgar/data/"):len(line)]
				formfilename = formfilename.rstrip()
				print>>target, formfilename
			elif line.find(str(form)+'  ') == 0:
				for CIK in CIKsUpdate:
					if line.find(' ' + str(CIK) + ' ') != -1:
						target.close()
						target = open(cwd + '/' + "storage/" + str(CIK) + '/' \
							+ str(CIK) + 'form' + str(formdir) + 'update.txt',\
							 'a')
						LastCIK = CIK
						formfilename = line[line.find("edgar/data/"):len(line)]
						formfilename = formfilename.rstrip()
						print>>target, formfilename
	
	target.close()
	LastCIK = '911911911911911911911911911'
	for CIK in CIKsUpdate:
		with open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' \
		+ str(formdir) + 'update.txt') as sourcefile:
			target = open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + \
				'form' + str(formdir) + '.txt', 'a+')
			targetstring = target.read()
			for line in sourcefile:
				if targetstring.find(line.strip()) == -1:
					print>>target, line.strip()
			target.close()

	for CIK in CIKsUpdate:
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

		with open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form'\
		+ str(formdir) + 'update.txt') as sourcefile:
			print "CIK loop", CIK
			for line in sourcefile:
				if not any(line.find(existingfile) != -1 for existingfile in \
				existingfilestring):
					namestart = line.find('/', len("edgar/data/"))
					filerCIK = line[len("edgar/data/"):namestart]
					filepath = line.strip()
					endline = filepath.find('.txt')
					filename = filepath[namestart + 1:endline+1]
					local_filename = os.getcwd() + "/" + "storage/" + str(CIK) \
					+ '/' + str(formdir) + '/' + filerCIK + '-' + filename + \
					"txt"
					ftpdownload(filepath, local_filename)

	txttoxml.processxml(cwd, formdir, CIKsUpdate)
print "done"
ftp.close()
print "FTP connection closed"




