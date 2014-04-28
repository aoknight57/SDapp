import os
import datetime
import sys

cwd = os.getcwd()

def isint(data):
	try:
		a = int(data)
		a = True
	except:
		a = False
	return a

def filewalkdictionary(subfolder, filesuffix):
	filedictionary = {}
	for root, dirs, filenames in os.walk(cwd + '/storage/'):
		for filename in filenames:
			if filename.endswith('.xml'):
				basefilename = filename[:len(filename)-4]
				filedictionary[basefilename] = [os.path.split(root)[1], 
												root, 
												os.path.join(root, filename)]
	return filedictionary


def exciser(string, startstring, endstring):
	return string[string.find(startstring) + len(startstring):\
				  string.find(endstring,string.find(startstring))]



def indexfilelister(indexfilelist, CIKs):
	IndexFileList = []

	forms = ['4    ', '4/A  ', '3    ', '3/A  ', '5    ', '5/A  ']
	formdirs = ['4', '4A', '3', '3A', '5', '5A']
	i = 0
	LastCIK = '911911911911911911911911911'
	LastForm = '911911911911911911911911911'
	for index in indexfilelist:
		print index
		with open(index) as infile:
			for line in infile:
				if line.find(' ' + LastCIK + '  ') != -1 and \
				line[:5] == LastForm:
					basefilename = exciser(line, 'edgar/data/' + LastCIK + '/', '.txt')
					IndexFileList.append(LastCIK + '-' + basefilename) 
					i += 1
				elif any(line[:5] == form for form in forms):
					LastForm = line[:5]

					for CIK in CIKs:
						if line.find(' ' + CIK + '  ') != -1:
							LastCIK = CIK
							basefilename = exciser(line, 'edgar/data/' + CIK + '/', '.txt')
							IndexFileList.append(CIK + '-' + basefilename) 
	print "Main loop true:", i, 'times'
	return IndexFileList	

def matcher(StorageFileDict, IndexFileList):
	StorageFileMatches = []
	StorageFileMisses = []
	for filename in IndexFileList:
		if StorageFileDict.get(str(filename), 'no match') is 'no match':
			StorageFileMisses.append(filename)
		else:
			StorageFileMatches.append(filename)	
	return StorageFileMatches, StorageFileMisses


qdirectorycontents = os.listdir(cwd + '/QFilingIndices/')
fullqindexfilelist = [item for item in qdirectorycontents
						   if item.endswith('txt')]

qindexfilelist = [cwd + '/QFilingIndices/' + item for item in fullqindexfilelist 
												  if int(item[:4]) > 2004]



ddirectorycontents = os.listdir(cwd + '/DFilingIndices/')
dindexfilelist = [cwd + '/DFilingIndices/' + item for item in ddirectorycontents 
												  if item.endswith('txt')]


subfolders = os.listdir(cwd + '/storage/')
CIKs = [item for item in subfolders if isint(item)]


StorageFileDict = filewalkdictionary('/storage/', '.xml')

print "StorageFileDict length", len(StorageFileDict)
print "[StorageFileDict is", float(sys.getsizeof(StorageFileDict)) / 1024, " kb]"
print "[This number may be wrong]"

IndexFileList = indexfilelister(qindexfilelist, CIKs)

print "IndexFileList length", len(IndexFileList)
print "IndexFileList is", float(sys.getsizeof(IndexFileList)) / 1024, " kb"


Matchresults = matcher(StorageFileDict, IndexFileList)

StorageFileMatches = Matchresults[0]
StorageFileMisses = Matchresults[1]

print StorageFileMisses
print "StorageFileMisses length", len(StorageFileMisses)
print "StorageFileMatches length", len(StorageFileMatches)
print "Matches / IndexFiles", float(len(StorageFileMatches)) / float(len(IndexFileList))

zerofiles = []
for filename in StorageFileDict:
	result = StorageFileDict[filename]
	path = result[2]
	if os.path.getsize(path) < 500:
		zerofiles.append(path)


print "There are", len(zerofiles), "comparatively empty files:"
print zerofiles

print "Reviewed", len(CIKs), "CIKs:", CIKs

