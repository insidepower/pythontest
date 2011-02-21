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
./get_adb_files.py 1 10 -c \"echo Probe-ttprb00017-%08d.haha-bin.gz\"
'''

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	parser = OptionParser(usage)   #when --help is used or when wrong opt
 	parser.add_option("-c", "--adb_cmd", dest="adb_cmd",
            help="adb command to be used")  # default action="store", options.filename
	#parser.add_option("-l", "--list-file",
	#		action="store_true", dest="list_file",
	#		help="list all changed files")  # set options.list_file=True
	#parse_args(arg) arg (default) = sys.argv[1:]
	return parser.parse_args()  #options.filename, options.verbose..

#----------------- main() ----------------#
def main():
	adb_cmd = None
	(options, args) = parseCmd()
	#print execBash('echo "testing"')
	#print execBash('echo "testing"')[0]
	if len(args)!=2:
		print usage
		sys.exit(2)
	
	if options.adb_cmd:
		print "options.adb_cmd: ", options.adb_cmd
		adb_cmd = options.adb_cmd
	else:
		adb_cmd = "adb pull /system/conti/dcm/data/Probe-ttprb00017-%08d.bin.gz"
		#adb_cmd = "echo Probe-ttprb00017-%08d.bin.gz"

	print "adb_cmd: ", adb_cmd
	start = int(args[0])
	end = int(args[1])
	print "start-sequence: ", start, "; end-sequence: ", end
	while(end >= start):
		sh_adb_cmd = adb_cmd % end
		#print "sh_adb_cmd: ", sh_adb_cmd
		execBash(sh_adb_cmd, False, True)
		end -= 1
	

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()

#----------------- reference() ----------------#
#print ("\033[1;31mWarning!! command (%s) not ended properly."
#		"exit status = %d\033[0m" %(cmd, p.returncode))

