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
#import re

#----------------- global variable ----------------#
file_compare_count = 0

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

#----------------- execBash() ----------------#
def execBash(cmd):
	#print cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read()
	#print out
	return out


#----------------- main() ----------------#
def main():
	(options, args) = parseCmd()
	print "start"
	reg_obj = re.compile(r"(.*: )*([0-9a-z]{40})")
	match_id = []
	line_to_del = []
	content = []

	## -- open file -- ##
	f = open(args[0])
	for i, line in enumerate(f):
		#content.append(line[:-1])
		## last char is newline, exclude it
		#print ("%s" % (line[:-1],))
		proj_name = reg_obj.match(line)
		if proj_name:
			commit_id = proj_name.group(2)
			if commit_id in match_id:
				## second match, i.e. commit has been logged, proceed to delete this line
				line_to_del.append(i)
				line_to_del.append(match_id[match_id.index(commit_id)+1])
			else:
				match_id.append(commit_id)
				match_id.append(i)
	f.close()
	
	f = open(args[0])
	for i, line in enumerate(f):
		if i not in line_to_del:
			content.append(line[:-1])
		#pass
		#print num
		#del content[num]
	f.close()

	for line in content:
		#pass
		print line

	f = open("/home/uidc1325/Desktop/uncommited.log", "w")
	f.writelines("\n".join(content))
	f.close()

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()
