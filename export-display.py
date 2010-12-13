#!/usr/bin/python
'''
usage : 
'''
import optparse
import subprocess
import re
import os
import sys
from optparse import OptionParser
from execBash import execBash

#----------------- global variable ----------------#

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = "usage: %prog [options] <startBranch>..<endBranch> <branch1> <branch2> [<branch3>]"
	parser = OptionParser(usage)   #when --help is used or when wrong opt
	parser.add_option("-l", "--list-file",
			action="store_true", dest="list_file",
			help="list all changed files")  # set options.verbose=True
	#parse_args(arg) arg (default) = sys.argv[1:]
	return parser.parse_args()  #options.filename, options.verbose..

#----------------- main() ----------------#
def main():
	(options, args) = parseCmd()
	for i in range(50):
		execBash('DISPLAY=localhost:%d'% (i,))
		if execBash('xclock')[1]==0:
			print("export DISPLAY=localhost:%d" % i)
			execBash ('export DISPLAY=localhost:%d' % i)
			sys.exit(0)

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()
