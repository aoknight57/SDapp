import os
cwd = os.getcwd()
CIK = '1467858'
form = '4'

#To-do
#1. fix the page break problem in the outstanding equity parser 
#2. Rewrite the loops to run through the indices one time and shuffle
#	out the hits for the desired for each form to a list of lists
#	and then write each to a file
#

target = open(cwd + '/' + "storage/" + str(CIK) + '/' + str(CIK) + 'form' + str(form) + '.txt')
for line in target:
	

	namestart = line.find('/', len("edgar/data/"))
	print namestart
	print line[namestart + 1:len(line)]
	print line[0:namestart]
	print line[len("edgar/data/"):namestart]
	# accstart = line.find('/', len("edgar/data/"))
	# foldstart = line.find('-')
	# identstart = line.find('-', foldstart + 1)
	# identend = line.find('.')
	# accession = line[accstart+1:foldstart]
	# folder = line[foldstart+1:identstart]
	# identifier = line[identstart+1:identend]
#	print folder + '/' + accession + identifier

#ftpbasedirectory = '/edgar/data/' + str(CIK) 
#print os.getcwd() + "/" + "storage/" + str(CIK) + '/' + str(form)+ '/' + folder + "-" + accession + identifier + ".xml"
#print ftpbasedirectory + "/" + folder + '/' + accession + identifier