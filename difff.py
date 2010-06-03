#!/usr/bin/python
'''
usage : difff.py [-l] <startBranch>..<endBranch> <branch1_toCompare> <branch2_tc> [<branch3_tc>]
e.g.    difff.py autolinq-2.1_base.. autolinq-2.0 autolinq-2.1_base autolinq-2.1_merge
e.g.    difff.py -l autolinq-2.1_base..
e.g.    difff.py autolinq-2.1_base.. autolinq-2.0 autolinq-2.1_merge
'''
import optparse
import subprocess
import re
import os
import sys
from optparse import OptionParser
#import re

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = "usage: %prog [options] <startBranch>..<endBranch> <branch1> <branch2> [<branch3>]"
	parser = OptionParser(usage)   #when --help is used or when wrong opt
	parser = OptionParser()
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

#----------------- processFile() ----------------#
def processFile(line, args):
	# extract the file from the branch specified in args[1]
	temp_file1 = "difff_%s" % args[1]
	temp_file2 = "difff_%s" % args[2]
	cmd_git_show="git show %s:%s > %s 2>/dev/null" % (args[1], line, temp_file1)
	execBash(cmd_git_show)
	cmd_git_show="git show %s:%s > %s 2>/dev/null" % (args[2], line, temp_file2)
	execBash(cmd_git_show)
	if len(args)==4:
		temp_file3 = "difff_%s" % args[3]
		cmd_git_show="git show %s:%s > %s 2>/dev/null" % (args[3], line, temp_file3)
		execBash(cmd_git_show)
		# bcompare a b c show the pane in: (a c b)
		cmd_bcompare="bcompare %s %s %s" % (temp_file1, temp_file3, temp_file2)
	else:
		cmd_bcompare="bcompare %s %s" % (temp_file1, temp_file2)

	## execute the command
	print ("%s: %s " % (line, cmd_bcompare))
	execBash(cmd_bcompare)

#----------------- list_file() ----------------#
def list_file(lines):
	reg_obj2 = re.compile(" *([.a-zA-Z0-9-_/]*) *(.*[0-9]*) ([-+]*)")
	reg_obj_minus = re.compile(r"[-]+$")
	reg_obj_plus = re.compile(r"[+]+$")
	files_new=[]
	files_deleted=[]
	files_changed=[]
	for line in lines:
		## look for --- or +++ or both
		result = reg_obj2.match(line)
		if result:
			print result.group(2)
			if result.group(3):		# if - or + or both detected
				print result.group(2)
				if reg_obj_plus.match(result.group(3)):
					files_new.append(result.group(1))
					print ("%d" % len(files_new))
					#print ("newly added %s" % (result,))
				elif reg_obj_minus.match(result.group(3)):
					files_deleted.append(result.group(1))
					#print ("newly deleted %s" % (result,))
				else:
					files_changed.append(result.group(1))
					#print ("file changes %s" % (result,))

	print "newly added files:"
	for file in files_new:
		print ("\t %s" % (file,))

	print "newly deleted files:"
	for file in files_deleted:
		print ("\t %s" % (file,))

	print "changed files:"
	for file in files_changed:
		print ("\t %s" % (file,))

#----------------- main() ----------------#
def main():
	file_to_add=""
	## parse command line options and arguments
	(options, args) = parseCmd()
	cmd="git diff %s --stat" % (args[0])
	#print options
	#print args

	## split the output into lines
	lines = execBash(cmd).splitlines()

	## iterate the output
	for line in lines:
		reg_obj = re.compile(r" *([.a-zA-Z0-9-_/]*)");
		result = reg_obj.match(line)
		#print result.group()  #for all match

		## list the changed file
		if options.list_file:
			list_file(lines)
			sys.exit(0)

		## check to make sure it is file, then process it
		if os.path.isfile(result.group(1)):
			#print result.group(1)
			processFile(result.group(1), args)
		else:
			print ("WARN!! %s (not file)" % (result.group(1),))

		## delete created files
		for my_branch in args[1:]:
			temp_file="difff_%s" % (my_branch)
			if os.path.isfile(temp_file):
				os.remove(temp_file)

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()
