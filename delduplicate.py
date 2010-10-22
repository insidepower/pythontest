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
	print cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read()
	#print out
	return out


#----------------- main() ----------------#
def main():
	(options, args) = parseCmd()
	print "start"
	reg_obj = re.compile(r"(.*: )*([0-9a-z]{40})")
	reg_obj2 = re.compile(r"project (.*)/")
	match_id = []
	match_id_line = []
	line_to_del = set()
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
				line_to_del.add(i)
				line_to_del.add(match_id_line[match_id.index(commit_id)])
			else:
				match_id.append(commit_id)
				match_id_line.append(i)
	f.close()
	
	f = open(args[0])
	for i, line in enumerate(f):
		if i not in line_to_del:
			content.append(line[:-1])
		#pass
		#print num
		#del content[num]
	f.close()

	line_to_del = set()
	for i, line in enumerate(content):
		if line == "project commitlog/":
			line_to_del.add(i)
			for m, delline in enumerate(content[i+1:]):
				if delline != "":
					#print "nonbreaking:", delline
					line_to_del.add(i+1+m)
					#print line_to_del
				else:
					#print "breaking: ", delline
					break

		if line == " ============================================================= ":
			line_to_del.add(i)
			for m, delline in enumerate(content[i:]):
				if delline == "":
					line_to_del.add(m)
				else:
					break

		#if reg_obj2.match(line) and content[i+1]=="":
		#	line_to_del.add(i)
		#	line_to_del.add(i+1)

	content2 = []
	for i, line in enumerate(content):
		if i not in line_to_del:
			content2.append(line)

	committer = []
	for i, line in enumerate(content2):
		proj_name = reg_obj2.match(line)
		current_dir = os.getcwd()
		if proj_name:
			my_proj_name = proj_name.group(1)
			committer.append(str("project " +my_proj_name+"/"))
			os.chdir(my_proj_name)
			print execBash("echo 'now at' `pwd`")
			for line2 in content2[i+1:]:
				if line2 != "":
					print "line2 =", line2
					author = execBash("git log %s -n1 --pretty=%%an" % line2[:39])[:-1]
					committer.append(str(author+" - "+line2))
				else:
					break
			os.chdir(current_dir)
			committer.append(str(""))

	#for i, line in enumerate(content):
	#	if reg_obj2.match(line) and content[i+1]=="":
	#		del content[i]
	#		del content[i+1]

	f = open("/home/uidc1325/Desktop/uncommited.log", "w")
	#f.writelines("\n".join(content2))
	f.writelines("\n".join(committer))
	f.close()

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()
