# To do:
# 1. Fix the failure to detect some of the FB stock awards
# 2. Figure out how to handle the circumstances where the header is garbled
# 	 and the columns are out of order -- need to detect this error and try to
#	 fix it (start with evaluating cell formats for clues)
# 3. Rewrite FTP script to pull in the quarterly indices (ftp://ftp.sec.gov/edgar/full-index/2014/QTR1/)
# note this regarding the html parser: https://github.com/pydata/pandas/issues/4683


import os

print os.getcwd()

def coolfunction():
	return 1, 2, 3

print coolfunction()[0]


