#!/usr/bin/python
# this file is to be placed at .repo/repo/subcmds/commit.py
'''
usage :
repo commit --author "Xinyu Chen" --since "2 years ago"
repo commit --since "2 years ago"     ### note: default --author=current git author
repo commit --grep="wrapper around" --author "Niko Catania" --since="2 years"
repo commit --grep="wrapper around" --author "Niko Catania" --since="2 years" -x "-n 1"
repo commit     ### note: default --since=1 hour, default --author=current git author
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


class Commit(Command):
	helpSummary = """create commit log"""
	helpUsage = ""
	current_dir=""
	git_current_branch=""
	commit_file="commit.log"
	commit_dir="commitlog"

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
			print ("\033[1;31mWarning!! command (%s) not ended properly."
					"exit status = %d\033[0m" %(cmd, p.returncode))
		#out = p.stdout.read()
		#print out
		return (stdoutdata, p.returncode)

#----------------- get_server_update() ----------------#
	def get_server_update(self):
		out = self.execBash("cat .git/HEAD")[0]
		if out.startswith('ref: '):
			self.git_current_branch=out[5:-1]
		else:
			print("\033[1;31mWarning!! no branch detected on current HEAD. "
					"Have you checkout a branch in directory commitlog? "
					"HEAD content=<%s>. "
					"Application Ended.\033[0m " %(self.git_current_branch))
			sys.exit(2)
		print ("getting update from server and merge to current branch %s..."
				% self.git_current_branch)
		(out, status)=self.execBash("git pull conti_dev %s" % self.git_current_branch)
		if status != 0:
			print out
			print("\033[1;31mWarning!! Not able to get the update from "
					"server! Application Ended.\033[0m ")
			sys.exit(2)

#----------------- commit_log() ----------------#
	def commit_log(self, author, msg, top_cmd):
		## retain current directory before proceeding
		self.current_dir=os.getcwd()

		# check if the commit log exist
		filepath=os.path.join(os.getcwd(), self.commit_file)
		print filepath
		## check if we are at the commit_dir directory
		if not os.path.isfile(filepath):
			if os.path.isdir(os.path.join(os.getcwd(), self.commit_dir)):
				## cd into commit_dir directory
				os.chdir(self.commit_dir)
				## get update from server
				self.get_server_update()
				filepath=os.path.join(os.getcwd(), self.commit_file)
				if not os.path.isfile(filepath):
					print("\033[1;31mWarning!! %s does not exist in %s! "
							"Have you deleted the file? use 'git checkout HEAD "
							"commit.log' to restore the file. "
							"Application Ended.\033[0m " %(self.commit_file,
								os.getcwd()))
					os.chdir(self.current_dir)
					sys.exit(2)
			else:
				## commit_dir not exists, quit
				print("\033[1;31mWarning!! Directory %s does not exist! "
						"Have you updated your manifest? "
						"Application Ended.\033[0m " %(self.commit_dir))
				os.chdir(self.current_dir)
				sys.exit(2)
			#print("\033[1;31mWarning!! %s does not exist, are you in commitlog "
			#		"directory?\033[0m " %(self.commit_file))
			#input=raw_input("If you are sure you are in commitlog "
			#		"directory, do you want to create the %s now? (y/n) " % self.commit_file)
			#if input == 'y':
			#	self.execBash("touch %s" % self.commit_file)
			#else:
			#	print("\033[1;31m File not created."
			#		"Application Ended\033[0m")
			#	sys.exit(2)

		## get update from server
		self.get_server_update()
		# append the details to commit log
		log_date=self.execBash("date")[0]
		log_msg="\nAuthor: " +author+ "\nDate  : " +log_date+"\n"+msg+ "-"*120
		cmd=("mv -f %s %s.tmp && echo '%s' > %s"
				% (self.commit_file, self.commit_file, log_msg, self.commit_file))
		status = self.execBash(cmd)[1]
		if status != 0:
			self.execBash("rm -f %s" % self.commit_file)
			print("\033[1;31mWarning!! Failed to execute %s."
					"Application Ended (%d)\033[0m" % (cmd, status))
			sys.exit(2)
		cmd="cat %s.tmp >> %s" % (self.commit_file, self.commit_file)
		status = self.execBash(cmd)[1]
		if status != 0:
			self.execBash("rm -f %s" % self.commit_file)
			print("\033[1;31mWarning!! Failed to execute %s."
					"Application Ended (%d)\033[0m" % (cmd, status))
			sys.exit(2)

		## run git commit
		(out, status)=self.execBash(top_cmd)
		print out

		if status==0:
			# commit successfully, remove the temporary file
			self.execBash("rm -f %s.tmp" % (self.commit_file))
		else:
			# not commit, revert change to commit_file
			self.execBash("rm -f %s && mv %s.tmp %s"
					%(self.commit_file, self.commit_file, self.commit_file))

		#out=self.execBash("git log -n1")[0]
		#print("show the last commit")
		#print out
		## go back to where we from
		self.execBash("git push conti_dev")
		os.chdir(self.current_dir)


#----------------- main() ----------------#
	def Execute(self, options, args):
		## testing
		#rp = self.manifest.repoProject
		#print "rp is %s" % rp.revisionExpr

		#(options, args) = parseCmd()
		commit_msg=""

		## set the duration for the commits to be considered
		duration="2 hour"
		if options.duration:
			duration=options.duration

		## set the author name
		current_user=self.execBash("git config user.name")[0]
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
		log_result=self.execBash(cmd)[0].splitlines()
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
			#git_status = subprocess.Popen("git status", shell=True,
			#								stdout=subprocess.PIPE).stdout.read()
			#git_status='git status: \n' + git_status
			git_status=""
			cmd = "git commit -am '%s'" % (commit_msg_format)
			msg_ready=("%s\ncommit message:\n%s \n%s\n%s\nReady to commit: (y/n)? "
							#%("-"*120 ,commit_msg_format, "-"*120, files_changes))
							%("-"*120 ,commit_msg_format, "-"*120, git_status))
			readyToCommit=raw_input(msg_ready)
			if "y"==readyToCommit:
				## commit the log
				self.commit_log(author, commit_msg_format, cmd)

		print "End of application. Have a nice day!"

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
#if __name__ == '__main__':
#	main()

