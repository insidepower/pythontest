#!/usr/bin/env python
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
usage = \
'''usage: ./get_adb_files.py <start-sequence> <end-sequence>

example: 
./get_adb_files.py 1 10
'''

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = "usage: %prog [options] <startBranch>..<endBranch> <branch1> <branch2> [<branch3>]"
	parser = OptionParser(usage)   #when --help is used or when wrong opt
 	parser.add_option("-f", "--file", dest="filename",
            help="read data from FILENAME")  # default action="store", options.filename
	parser.add_option("-l", "--list-file",
			action="store_true", dest="list_file",
			help="list all changed files")  # set options.list_file=True
	#parse_args(arg) arg (default) = sys.argv[1:]
	return parser.parse_args()  #options.filename, options.verbose..

#----------------- main() ----------------#
def main():
	(options, args) = parseCmd()
	print execBash('echo "testing"')
	print execBash('echo "testing"')[0]

	if options.filename:
		print "-f from user: ", options.filename

	if len(args):
		## note ./app_name --option1 xxx-option-value arg0 arg1
		print "args: ", args

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()

#----------------- reference() ----------------#
#print ("\033[1;31mWarning!! command (%s) not ended properly."
#		"exit status = %d\033[0m" %(cmd, p.returncode))

