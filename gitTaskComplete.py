#!/usr/bin/python
# git config user.name
# git log --author="Khian Nam"
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

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	parser = OptionParser()
	parser.add_option("-t", "--set-duration",dest="duration",
			help="set the duration for the commits to be considered (default is 1 hour)")
	parser.add_option("-n", "--set-author",dest="author",
			help="set the author name for the commits to be considered")
	parser.add_option("-s", "--seach-commit-msg",dest="searchstr",
			help="search for a string pattern in commit message")
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
	commit_msg=""

	## set the duration for the commits to be considered
	duration="1 hour"
	if options.duration:
		duration=options.duration

	## set the author name
	author=(re.match(r"[^\n]*", execBash("git config user.name"))).group()
	if options.author:
		author=options.author

	## look for sub-project which is most likely commited by user recently
	cmd='repo forall -p -c git log --since="%s" --author="%s" --pretty=oneline' % (duration, author)
	if options.searchstr:
		cmd=cmd + ' -S"%s"' % (options.searchstr)

	print("recursive searching for each sub-projects for commits since last %s from %s" %(duration, author))
	log_result=execBash(cmd).splitlines()
	#print log_result
	for i, line in enumerate(log_result):
		#print line
		proj_name=re.match(r"project (.*)/", line)
		if proj_name:
			prompt_msg = "add %s: log=%s (y/n)? " %(proj_name.group(1), log_result[i+1])
			shouldAdd=raw_input(prompt_msg)
			if 'y' == shouldAdd:
				commit_msg += "%s: %s\n" %(proj_name.group(1), log_result[i+1])
				#print("commit_msg=%s" %(commit_msg))
			#print proj_name.group()
			#print log_result[i+1]

	## ready to commit
	if commit_msg:
		first_line_summary=re.match(r".*?: [0-9a-z]{40} (.*)", commit_msg)
		#print ("match %s " %(first_line_summary.group(1)))
		shouldUse=raw_input("\nuse line below as the 1st line summary:\n%s (y/n)? " %first_line_summary.group(1))

		if "y"==shouldUse:
			commit_msg_format = "%s\n\n%s" %(first_line_summary.group(1), commit_msg)
			cmd = "git commit -am '%s'" % (commit_msg_format)
		elif "n"==shouldUse:
			user_oneline_summary=raw_input("Please input your first line summary below:\n")
			cmd = "git commit -am '%s\n\n%s'" %(user_oneline_summary, commit_msg)

		msg_ready="%s\ncommit message:\n%s \n%s\nReady to commit: (y/n)? " %("-"*80 ,commit_msg_format, "-"*80)
		readyToCommit=raw_input(msg_ready)
		if "y"==readyToCommit:
			out=execBash(cmd)
			print out
			#out=execBash("git log -n1")
			#print("show the last commit")
			#print out

	print "End of application. Have a nice day!"

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()

