#!/usr/bin/python
# --------------------------------------------------------------"
# Copyright (C) 2010 Continental Automotive Singapore, Pte. Ltd."
# --------------------------------------------------------------"
# this file is to be placed at .repo/repo/subcmds/patch.py
'''
usage :
'''

import optparse
import subprocess
import re
import os
import sys
from optparse import OptionParser
from command import Command

#----------------- global variable ----------------#


class Patch(Command):
	## remote_branch = branch in server
	remote_branch = "nissan_ev_wipro"
	## active_branch = branch with active development
	active_branch = "nissan_ev_wipro_dev"

	helpSummary = """generate or apply patches"""
	top_dir = ""
	#options = None
	args = None
	dest_dir = ""
	repo_dir = ".repo"
	proj_with_patch=[]

#----------------- parseCmd() ----------------#
## parse the command line arguments
  	def _Options(self, parser):
		def cmd(option, opt_str, value, parser):
			setattr(parser.values, option.dest, list(parser.rargs))
			while parser.rargs:
				del parser.rargs[0]
		#parser = OptionParser()
		parser.add_option("-d", "--destination", dest="dest_dir",
				help="absolute path to destination directory to be created");
		parser.add_option("-o", "--generate-patch-only", dest="is_gen_patch_only",
				action="store_true", default=False,
				help="generate patch only");
		parser.add_option("-g", "--generate-patch", dest="is_gen_patch",
				action="store_true", default=False,
				help="generate patch and extract it to destination, then zip it");
		#return parser.parse_args()  #options.filename, options.verbose..

#----------------- execBash() ----------------#
	def execBash(self, cmd, is_suppress=False):
		#print cmd
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		#(stdoutdata, stderrdata) = p.communicate()
		stdoutdata = p.communicate()[0]
		p.poll()
		if (p.returncode != 0) and (not is_suppress):
			print ("\033[1;31mWarning!! command (%s) not ended properly."
					"exit status = %d\033[0m" %(cmd, p.returncode))
		#out = p.stdout.read()
		#print out
		return (stdoutdata, p.returncode)

#----------------- gen_directory() ----------------#
	def gen_directory(self, dest_dir):
		self.dest_dir = dest_dir
		print "destination folder = ", self.dest_dir

		## check if destination directory exists
		if os.path.isdir(self.dest_dir):
			print ("\033[1;31m"
					"Destination directory exists! Please delete the directory."
					"\033[0m\n")
			should_delete = raw_input("delete the directory now? (y/n) ")
			if 'y' == should_delete.lower():
				out = self.execBash('rm -rf %s' % self.dest_dir)[1]
				if out:
					sys.exit(2)
			else:
				sys.exit(2)

		## create each directory in destination folder
		for project in self.GetProjects(self.args):
			cmd = "mkdir -p %s/%s" % (self.dest_dir, project.relpath)
			#print cmd
			result = self.execBash(cmd)[1]
			#self.proj_name.append(project.relpath)	
			if result:
				print "error! return code= ", result
		#print self.proj_name

#----------------- gen_patch_only() ----------------#
	## generate pathes only
	def gen_patch_only(self):
		print ""
		for project in self.GetProjects(self.args):
			os.chdir(project.relpath)
			print "[project]:", project.relpath
			out = self.execBash("ls *.patch &2>/dev/null", True)[0]
			if out:
				print ("\033[1;31m"
					"Patches exists! Please delete before proceed."
					"\033[0m")
				should_delete = raw_input("delete the patches now? (y/n) ")
				if 'y' == should_delete.lower():
					result = self.execBash("rm -f *.patch")[1]
					if result:
						sys.exit(2)
				else:
					sys.exit(2)
					
			#print "result", out
			out = self.execBash("git format-patch %s..%s" % 
					(self.remote_branch, self.active_branch))[0]
			print out
			self.proj_with_patch.append(project.relpath)	
			os.chdir(self.top_dir)
			#cmd = "repo forall -c 'echo && echo -n [project]: && pwd && " \
			#	  "git format-patch %s..%s'" % (self.remote_branch, self.active_branch)
			#out = self.execBash(cmd, True)[0]

#----------------- copy_patch() ----------------#
	## generate pathes only
	def copy_patch(self):
		for project in self.proj_with_patch:
			cmd = "cp -r %s/*.patch %s/%s" % (project, self.dest_dir, project)
			out = self.execBash(cmd)[1]
			if out:
				sys.exit(2)

#----------------- gen_patch() ----------------#
	## generate patch and copy to destination folder then zip it
	def gen_patch(self, dest_dir):
		self.gen_directory(dest_dir)
		self.gen_patch_only()
		self.copy_patch()

#----------------- main() ----------------#
	def Execute(self, options, args):
		#(self.options, self.args) = self.parseCmd()
		self.args = args

		if os.path.isdir(os.path.join(os.getcwd(), self.repo_dir)):
			self.top_dir = os.getcwd()

			## generate patch and copy to destination folder then zip it
			if options.is_gen_patch:
				if options.dest_dir:
					self.gen_patch(options.dest_dir)
					sys.exit(0)
				else:
					print ("\033[1;31mPlease provide absolute path destination "
							"directory\n e.g.: $ repo patch -g -d "
							"~/home/user/nissan-patches \033[0m\n")
					sys.exit(2)

			## generate the empty directory hierarachy according to manifest
			if options.dest_dir:
				self.gen_directory(options.dest_dir);

			## generate pathes only
			if options.is_gen_patch_only:
				self.gen_patch_only()

		else:
			print ("\033[1;31mPlease execute this command at top project "
					"directory where .repo folder exists \033[0m\n")


#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
#if __name__ == '__main__':
#	f = patch();
#	f.main();
#	f.gen_directory();
