def filemapper():
	import os
	xmldirectory = []
	for root, dirs, files in os.walk ("/Users/David/SDapp/AutomatedFTP/storage/882095/4/"):
		for file in files:
			if file.endswith('.xml'):
#				if os.path.join(root, file).find("0001179110") == -1:
#					print os.path.join(root, file)
				xmldirectory.append(os.path.join(root, file))
	return xmldirectory

print "How long is the returned directory list?"
print(len(filemapper()))

