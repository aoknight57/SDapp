import json

def xnreader(filename):
	target = open(filename)
	content = json.load(target)
	convcontent = []
	for row in content:
		convrow = []
		for item in row:
			convitem = item

			if isinstance(convitem, unicode):
				convitem = convitem.encode('ASCII', 'ignore')
			# 	print type(convitem)
			# print convitem
			# print type(convitem)
			convrow.append(convitem)

		convcontent.append(convrow)
	

	return convcontent

