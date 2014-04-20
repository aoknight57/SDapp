import csv
import json

def csvconvert(InputFileName, OutputFileName):
	print "Converting", InputFileName, "to", OutputFileName
	with open(InputFileName) as sourcefile:
		jsonstring = sourcefile.read()
		targetlist = json.loads(jsonstring)

	with open(OutputFileName, 'w') as csvfile:
	    listwriter = csv.writer(csvfile, delimiter=',', quotechar='"')

	    for row in targetlist:
	    	listwriter.writerow(row)


csvconvert('NonDerivXn4AFile.txt', 'NonDerivXn4AFile.csv')
csvconvert('Form4AMatchIndex.txt', 'Form4AMatchIndex.csv')

csvconvert('Form4MatchForms.txt', 'Form4MatchForms.csv')