#!/usr/bin/python
# this file is to be placed at .repo/repo/subcmds/compl.py
'''
usage :
repo compl --author "Xinyu Chen" --since "2 years ago"
repo compl --since "2 years ago"     ### note: default --author=current git author
repo compl --grep="wrapper around" --author "Niko Catania" --since="2 years"
repo compl --grep="wrapper around" --author "Niko Catania" --since="2 years" -x "-n 1"
repo compl     ### note: default --since=1 hour, default --author=current git author
'''
import optparse
import subprocess
import re
import os
import sys
from optparse import OptionParser
from command import Command
#import re

#----------------- global variable ----------------#


class Compl(Command):
	helpSummary = """mark a task as complete and get name of anroid
				     projects changed related to the task"""
	helpUsage = ""

#----------------- parseCmd() ----------------#
## parse the command line arguments
	#def parseCmd():
  	def _Options(self, parser):
		def cmd(option, opt_str, value, parser):
			setattr(parser.values, option.dest, list(parser.rargs))
			while parser.rargs:
				del parser.rargs[0]
		#parser = OptionParser()
		parser.add_option("--since", "--set-duration",dest="duration",
				help="set the duration for the commits to be "
						"considered (default is 1 hour)")
		parser.add_option("--author", "--set-author",dest="author",
				help="set the author name for the commits to be considered")
		parser.add_option("--grep", "--seach-commit-msg",dest="searchstr",
				help="search for a string pattern in commit message")
		parser.add_option("-x", "--extra-parameter",dest="extra_params",
				help="use extra parameter to fine tune the search. "
					  "both parameter and value must be inside single quote "
					  "e.g. '-n 1' to search for just one commit")
		#parse_args(arg) arg (default) = sys.argv[1:]
		#return parser.parse_args()  #options.filename, options.verbose..

#----------------- execBash() ----------------#
	def execBash(self, cmd):
		#print cmd
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		#(stdoutdata, stderrdata) = p.communicate()
		stdoutdata = p.communicate()[0]
		p.poll()
		if p.returncode != 0:
			print ("\033[1;31mWarning!! command not ended properly."
					"exit status = %d\033[0m" %(p.returncode))
		#out = p.stdout.read()
		#print out
		return stdoutdata

#----------------- main() ----------------#
	def Execute(self, options, args):
		#(options, args) = parseCmd()
		commit_msg=""

		## set the duration for the commits to be considered
		duration="1 hour"
		if options.duration:
			duration=options.duration

		## set the author name
		current_user=self.execBash("git config user.name")
		author=(re.match(r"[^\n]*", current_user)).group()
		if options.author:
			author=options.author

		cmd=('repo forall -p -c git log --since="%s" --author="%s" --pretty=oneline'
				% (duration, author))
		if options.searchstr:
			cmd=cmd + ' --grep="%s"' % (options.searchstr)

		if options.extra_params:
			cmd=cmd + ' %s' %(options.extra_params)

		## look for sub-project which is most likely commited by user recently
		print("recursive searching for each sub-projects for commits "
				"since last %s from %s" %(duration, author))
		print cmd
		log_result=self.execBash(cmd).splitlines()
		#print log_result
		for i, line in enumerate(log_result):
			#print line
			proj_name=re.match(r"project (.*)/", line)
			if proj_name:
				## recursively get all commits from one project
				for commit_id in log_result[i+1:]:
					## check if there is anymore commit under the same project
					if (re.match(r"[0-9a-z]{40}", commit_id)):
						prompt_msg = ("\033[1;34madd %s: log=%s \033[0m(y/n)? "
										%(proj_name.group(1), commit_id[:120]))
						shouldAdd=raw_input(prompt_msg)
						if 'y' == shouldAdd:
							commit_msg += ("%s: %s\n"
									%(proj_name.group(1), commit_id[:120]))
							#print("commit_msg=%s" %(commit_msg))
							#print proj_name.group()
							#print log_result[i+1]
					else:
						## no more commits under this project
						break

		## ready to commit
		if commit_msg:
			first_line_summary=re.match(r".*?: [0-9a-z]{40} (.*)", commit_msg)
			#print ("match %s " %(first_line_summary.group(1)))
			shouldUse=raw_input("\nuse line below as the 1st line "
								"summary:\n%s (y/n)? " %first_line_summary.group(1))

			if "y"==shouldUse:
				commit_msg_format = "%s\n\n%s" %(first_line_summary.group(1), commit_msg)
			else:
				line1_msg=raw_input("Please input your first line summary below:\n")
				commit_msg_format = "%s\n\n%s" % (line1_msg, commit_msg)

			# get the list of files changes too
			#files_changes=('files changes to be added:\n\033[1;32m%s\033[0m'
			#				% self.execBash("git ls-files -m"))
			git_status = subprocess.Popen("git status", shell=True,
											stdout=subprocess.PIPE).stdout.read()
			git_status='git status: \n' + git_status
			cmd = "git commit -am '%s'" % (commit_msg_format)
			msg_ready=("%s\ncommit message:\n%s \n%s\n%s\nReady to commit: (y/n)? "
							#%("-"*120 ,commit_msg_format, "-"*120, files_changes))
							%("-"*120 ,commit_msg_format, "-"*120, git_status))
			readyToCommit=raw_input(msg_ready)
			if "y"==readyToCommit:
				out=self.execBash(cmd)
				print out
				#out=execBash("git log -n1")
				#print("show the last commit")
				#print out

		print "End of application. Have a nice day!"

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
#if __name__ == '__main__':
#	main()

