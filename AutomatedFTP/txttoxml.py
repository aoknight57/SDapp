

### The commented code is here to permit the code to be run as a standalone script
import os
#form = 4
#cwd = os.getcwd()
#CIKs = []
#	with open("CIKs.txt") as infile:
#		for line in infile:
#			CIKs.append(line.strip())
#	print "Using CIKs:", CIKs


def filingdatepull(filestring):
	try:
		snippetstart = filestring.find('<SEC-DOCUMENT>')
		snippet = filestring[snippetstart:snippetstart + 100]
		datestart = snippet.find(':')
		datestring = snippet[datestart+1:datestart+10]
		return datestring + '!'
	except:
		return "error!"



def processxml(cwd, formdir, CIKs):
	for CIK in CIKs:
		directory = cwd + '/' + "storage/" + str(CIK) + '/' + str(formdir) + '/'
		filingdaterecord = open(cwd + '/' + "storage/" + str(CIK) + '/' + formdir + 'filingdates.txt', 'a')
		for filename in os.listdir(directory):
			if filename.endswith(".txt"):
				

				target = open(directory + filename, 'r')
				targetstring = target.read()
				target.close()
				print>>filingdaterecord, filingdatepull(targetstring) + filename + ':' + CIK + ';' 
				startxml = targetstring.find('<XML>') + 5
				endxml = targetstring.find('</XML>')
				if startxml != -1 and endxml != -1:
					# filelength = len(targetstring)
					target = open(directory + filename, 'w')
					targetstring = targetstring[startxml:endxml].strip('\n')
					target.write(targetstring)
					target.close()


					os.rename(directory + filename, directory + filename[:len(filename)-4] + '.xml')
		filingdaterecord.close()
#				target = open(directory + filename, 'r+')
#				targetstring = target.read()
#				if targetstring.find("</ownershipD") != -1:
#					target.seek(targetstring.find("</ownershipD"))
#					target.write("</ownershipDocument>")
#				target.close()





