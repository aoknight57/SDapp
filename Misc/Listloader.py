import json

def xnreader(filename):
	target = open(filename)
	content = json.load(target)
	return  content


results = xnreader('DerivXn4AFile.txt')
# for line in results:
	# print line

print results
print "sample entry"
print results[1]