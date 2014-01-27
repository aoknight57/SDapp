def filemapper():
	import os
	xmldirectory = []
	i = 0
	for root, dirs, files in os.walk ("/Users/David/882095"):
		for file in files:
			if file.endswith('.xml'):
				i = i + 1
				xmldirectory.append(os.path.join(root, file))
	return xmldirectory

print "How long is the returned directory list?"
print(len(filemapper()))
