# To do:
# 1. Fix the failure to detect some of the FB stock awards
# 2. Figure out how to handle the circumstances where the header is garbled
# 	 and the columns are out of order -- need to detect this error and try to
#	 fix it (start with evaluating cell formats for clues)


import os

print os.getcwd()

def coolfunction():
	return 1, 2, 3

print coolfunction()[0]


