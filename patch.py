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
	remote_branch = "nissan_ev_dev"
	## active_branch = branch with active development
	active_branch = "nissan_ev_wipro"

	helpSummary = """generate or apply patches"""
	cur_dir_len = 0
	#options = None
	#args = None
	dest_dir = ""

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
		parser.add_option("-g", "--generate-patch", dest="is_gen_patch",
				action="store_true", default=False,
				help="path to destination directory to be created");
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

#----------------- gen_directory() ----------------#
	def gen_directory(self):
		self.cur_dir_len = len(os.getcwd())+1
		#print "cur_dir_len=",self.cur_dir_len;
		out = self.execBash("repo forall -c pwd")[0].splitlines()
		for line in out:
			#print line[(self.cur_dir_len):]
			cmd = "mkdir -p %s/%s" % (self.dest_dir, line[self.cur_dir_len:])
			print cmd
			result = self.execBash(cmd)[1]
			if result:
				print "error! return code= ", result

#----------------- main() ----------------#
	def Execute(self, options, args):
		#(self.options, self.args) = self.parseCmd()

		## generate the empty directory hierarachy according to manifest
		if options.dest_dir:
			self.dest_dir = options.dest_dir
			print "destination folder = ", self.dest_dir
			self.gen_directory();

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
#if __name__ == '__main__':
#	f = patch();
#	f.main();
#	f.gen_directory();

