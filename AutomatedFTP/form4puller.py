from ftplib import FTP
import os
# This pulls all the GILD Form 4s.  It wouldn't be too hard to generalize
# it to any ticker.  Word to the wise, it takes about 10 minutes to run on my
# machine.  Also, it spits errors into the terminal but this could be changed.
ftpbasedirectory = "/edgar/data/882095"

try:
	ftp = FTP('ftp.sec.gov') 
	ftp.login('anonymous', #'ENTEREMAILADDRESS')
	print "Connected"
except:
	print "Cannot Connect"

# note that you must strip the leading zeroes on the CIK
ftp.cwd(ftpbasedirectory)
print "now in /edgar/data/882095 directory" 
baselevellist = []
ftp.retrlines('nlst', baselevellist.append)
print "Single level directory now generated"

basefolderdirectory = []
for entry in baselevellist:
	if len(entry) == 2:
		basefolderdirectory.append(entry)
print "Yearly folder list now generated"

print "Now going to go one level deeper and start saving files..."
nesteddirectory = []

for entry in basefolderdirectory:
	nesteddirectoryrow = []
	print "building subdirectory ", entry
	ftp.cwd(ftpbasedirectory + "/" + entry)
	ftp.retrlines('nlst', nesteddirectoryrow.append)
	nesteddirectory.append(nesteddirectoryrow)
	for folder in nesteddirectoryrow:
		if folder.find("0001179110") != -1:
			try:
				ftp.cwd(ftpbasedirectory + "/" + entry + "/" + folder)
				local_filename = os.getcwd() + "/form4pullerstorage/" + entry + "-" + folder + ".xml"
				target = open(local_filename, 'wb')
				ftp.retrbinary('RETR %s' % "edgar.xml", target.write)
				target.close
			except: 
				print "Can't get file in ", folder

print "Done with second level directory and file download"

print "Now building full directory record from the subdirectories"
directory = []
for row in nesteddirectory:
	for entry in row:
		folder = basefolderdirectory[nesteddirectory.index(row)]
		directory.append(folder + "/" + entry)

print "Full directory built"
target = open((os.getcwd() + "/form4index882095.txt"), 'w')
target.truncate()
selectdirectory = []
for entry in directory:
	if entry.find("0001179110") != -1:
		print>>target, entry
		selectdirectory.append(entry)
print "Directory entries with specified entries written"

target.close()
ftp.close()
