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
from datetime import date
from glob import glob

#----------------- global variable ----------------#


class Patch(Command):
	## remote_branch = branch in server
	remote_branch = "nissan_ev_wipro"
	## active_branch = branch with active development
	active_branch = "nissan_ev_wipro_dev"

	helpSummary = """generate or apply patches \n
					 Example Usage:\n
				     repo patch -g\n
					 repo patch -g -s my_remote_branch -a my_active_branch\n
					 repo patch -p xxx.tar.gz
				  """
	top_dir = ""
	#options = None
	args = None
	dest_dir = ""
	repo_dir = ".repo"
	proj_with_patch=[]
	tar_target=""
	out_log=""
	patch_log = "patches-summary.txt"
	project_deco = "[project]: "
	tar_target_dir = ""
	creator=""
	email=""

#----------------- parseCmd() ----------------#
## parse the command line arguments
  	def _Options(self, parser):
		def cmd(option, opt_str, value, parser):
			setattr(parser.values, option.dest, list(parser.rargs))
			while parser.rargs:
				del parser.rargs[0]
		#parser = OptionParser(usage=usage_str)
		parser.add_option("-o", "--generate-patch-only", dest="is_gen_patch_only",
				action="store_true", default=False,
				help="generate patch only");
		parser.add_option("-g", "--generate-patch", dest="is_gen_patch",
				action="store_true", default=False,
				help="generate patch and extract it to destination, then zip it");
		parser.add_option("-p", "--apply-patch", dest="untar_patch",
				help="apply patches to current directory");
		parser.add_option("-s", "--server-branch", dest="remote_branch",
				help="indicate the remote branch, default is nissan_ev_wipro");
		parser.add_option("-a", "--active-branch", dest="active_branch",
				help="indicate the active development branch, default is nissan_ev_wipro_dev");
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

#----------------- gen_patch_only() ----------------#
	## generate pathes only
	def gen_patch_only(self):
		print "\n...generating patches..."
		for project in self.GetProjects(self.args):
			project_dir = "%s/%s" % (self.dest_full_dir, project.relpath)
			self.execBash("mkdir -p %s" % project_dir)
			os.chdir(os.path.join(self.top_dir, project.relpath))
			title = "%s%s" % (self.project_deco, project.relpath)
			print ("\033[1;34m%s\033[0m" % title)
			#out = self.execBash("ls *.patch &2>/dev/null", True)[0]
			#print glob("*.patch")
			#if len(glob("*.patch")):
			##if out:
			#	print ("\033[1;31m"
			#		"Patches exists! Please delete before proceed."
			#		"\033[0m")
			#	should_delete = raw_input("delete the patches now? (y/n) ")
			#	if 'y' == should_delete.lower():
			#		result = self.execBash("rm -f *.patch")[1]
			#		if result:
			#			sys.exit(2)
			#	else:
			#		sys.exit(2)

			#print "result", out
			cmd = "git format-patch %s..%s -o %s/%s" % (self.remote_branch, \
					self.active_branch, self.dest_full_dir, project.relpath)
			print cmd
			out, bad_exit = self.execBash(cmd, True)

			if out and (not bad_exit):
				print out
				self.out_log += title + '\n' + out + '\n'
				self.proj_with_patch.append(project.relpath)	
			else:
				## else delete the generated directory
				print "-- No patches --\n"
				self.execBash("rm -rf %s" % project_dir)
			#print self.proj_with_patch
			#cmd = "repo forall -c 'echo && echo -n [project]: && pwd && " \
			#	  "git format-patch %s..%s'" % (self.remote_branch, self.active_branch)
			#out = self.execBash(cmd, True)[0]
		os.chdir(self.top_dir)

		if self.out_log == "":
			print ("\033[1;31m"
					"Application terminated as no patches is generated"
					"\033[0m")
			sys.exit(2)

#----------------- log_patch_summary() ----------------#
	## storing the patch summary
	def log_patch_summary(self):
		self.creator = self.execBash("git config --list "
										"| sed -n 's/user.name=//gp'")[0][:-1]
		self.email = self.execBash("git config --list "
										"| sed -n 's/user.email=//gp'")[0][:-1]
		log_name = "%s/%s" % (self.dest_full_dir, self.patch_log)
		f = open(log_name, "w")
		f.write('-'*80+'\n')
		f.write('Date: %s\n' % date.today())
		f.write('Creator: %s(%s)\n' % (self.creator, self.email))
		f.write('-'*80+'\n')
		f.write(self.out_log)
		f.close()

#----------------- zip_patch() ----------------#
	## zipping the patch destination directory
	def zip_patch(self):
		print "\n...zipping patches..."
		os.chdir(self.top_dir)
		patch_name = "patch-%s.tar.gz" % date.today()
		if os.path.isfile(os.path.join(self.top_dir, patch_name)):
			#print ('deleting exsiting %s' % patch_name)
			os.remove(patch_name)
			#sys.exit(2)
		cmd = "tar -czvf %s %s" % (patch_name, self.dest_dir)
		print cmd
		out = self.execBash(cmd)

#----------------- untar_patch() ----------------#
	## zipping the patch destination directory
	def untar_patch(self, target):
		os.chdir(self.top_dir)
		self.tar_target = target
		self.tar_target_dir = re.match(r"(.*).tar.gz", target).group(1)
		if os.path.isdir(self.tar_target_dir):
			print "%s exists, deleting it" % (self.tar_target_dir)
			self.execBash("rm -rf %s" % self.tar_target_dir)
		print "my tar_target_dir=", self.tar_target_dir
		cmd = "tar -xzvf %s" % (target)
		print cmd
		out = self.execBash(cmd)
		should_apply = raw_input('Proceed to apply pathes? (y/n) ')
		if 'y' == should_apply.lower():
			self.apply_patch()

#----------------- apply_patch() ----------------#
	## generate patch and copy to destination folder then zip it
	def apply_patch(self):
		print "\n...applying patches..."
		os.chdir(self.top_dir)
		patch_file = os.path.join(self.tar_target_dir, self.patch_log)
		f = open(patch_file, "r")
		for line in f:
			#print line
			proj_name=re.match(r"\[project\]: (.*)", line)
			if proj_name:
				proj = proj_name.group(1)
				os.chdir(os.path.join(self.top_dir, proj))
				cmd = "git am --3way %s/%s/%s/*.patch" % \
						(self.top_dir, self.tar_target_dir, proj)
				print "%s: %s" % (proj, cmd)
				self.execBash(cmd)
		f.close()

#----------------- gen_patch_dir() ----------------#
	## generate patch directory
	def gen_patch_dir(self):
		self.dest_dir = "patch-%s" % date.today()
		self.dest_full_dir = os.path.join(self.top_dir, self.dest_dir)
		if os.path.isdir(self.dest_full_dir):
			print ("\033[1;31m"
					"patch directory %s exists "
					"\033[0m" % self.dest_dir)
			should_delete = raw_input('delete patch directory %s? (y/n) ' 
					% self.dest_dir)
			if 'y' == should_delete.lower():
				self.execBash("rm -rf %s" % self.dest_full_dir)
			else:
				sys.exit(2)
		os.mkdir(self.dest_full_dir)

#----------------- main() ----------------#
	def Execute(self, options, args):
		#(self.options, self.args) = self.parseCmd()
		self.args = args

		## check if we are at the top directory
		if os.path.isdir(os.path.join(os.getcwd(), self.repo_dir)):
			self.top_dir = os.getcwd()

			if options.remote_branch:
				self.remote_branch = options.remote_branch

			if options.active_branch:
				self.active_branch = options.active_branch

			## generate patch and copy to destination folder then zip it
			if options.is_gen_patch:
				self.gen_patch_dir()
				self.gen_patch_only()
				self.log_patch_summary()
				self.zip_patch()
				self.execBash("rm -rf %s" % self.dest_full_dir)
				sys.exit(0)

			## generate pathes only
			if options.is_gen_patch_only:
				self.gen_patch_dir()
				self.gen_patch_only()

			## untar patches
			if options.untar_patch:
				self.untar_patch(options.untar_patch)

		else:
			print ("\033[1;31mPlease execute this command at top project "
					"directory where .repo folder exists \033[0m\n")


#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
#if __name__ == '__main__':
#	f = patch();
#	f.main();
#	f.gen_directory();

