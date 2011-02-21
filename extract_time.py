#!/usr/bin/python 
'''
usage :
	- Parsed the Probe-ttprb00017-00000034.bin 
	- extract the TimeStamp from Probe-ttprb00017-00000034.bin_parsed_output.txt
	- check for the discontinuity of the TimeStamp
'''

import optparse
import subprocess
import re
import os
import sys
from optparse import OptionParser
import glob

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = "usage: %prog [options] "
	parser = OptionParser(usage)   #when --help is used or when wrong opt
	parser.add_option("-z", "--is_zip",
			action="store_true", dest="is_zip",
			help="to indicate it is gunzipped file")  # set options.verbose=True
	parser.add_option("-p", "--is_not_parsed",
			action="store_true", dest="is_not_parsed",
			help="to indicate the file is not parsed")  # set options.verbose=True
	#parse_args(arg) arg (default) = sys.argv[1:]
	return parser.parse_args()  #options.filename, options.verbose..

#----------------- execBash() ----------------#
def execBash(cmd, is_suppress=False):
	print cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	#(stdoutdata, stderrdata) = p.communicate()
	stdoutdata = p.communicate()[0]
	p.poll()
	if p.returncode != 0 and (not is_suppress):
		print ("\033[1;31mWarning!! command (%s) not ended properly."
				"exit status = %d\033[0m" %(cmd, p.returncode))
	#out = p.stdout.read()
	#print out
	return (stdoutdata, p.returncode)

#----------------- class WrongLine() ----------------#
class WrongLine(object):
	filename = None
	info = []

	def __init__(self, filename, reason, line1, line2):
		print "WrongLine: init"
		self.filename=filename
		self.info.append([reason, line1, line2])
	
	def add_wrongline(self, reason, line1, line2):
		self.info.append([reason, line1, line2])

	def print_me(self):
		#print "~"*100
		i = 1
		print "filename: ", self.filename
		print "total possible error: ", len(self.info)
		for line in self.info:
			print ("%d: reason: %s" % (i, line[0]))
			print "line1: ", line[1]
			print "line2: ", line[2]
			i += 1
		print ""
		#print "~"*100

#----------------- class ExtractTime() ----------------#
class ExtractTime(object):
	filename="Probe-ttprb00017*bin"
	file_to_be_parsed = None
	filelist = None
	is_zip = False
	is_not_parsed = False
	firstline=[]
	wrongline=[]
	CORRECT = True
	WRONG = False

	def __init__(self, fn=None, is_zip=False):
		print "ExtractTime: init"
		self.is_zip = False
		self.is_not_parsed = False
		if fn:
			self.filename=fn
		else:
			self.filename="Probe-ttprb00017*bin"
	
	def gunzipfile(self, file):
		basename, ext = os.path.splitext(file)
		if ext!=".gz":
			print ("\033[1;31mWarning!! %s not ended with gz\033[0m" % file)
		#print os.getcwd()
		if execBash("gunzip -f %s" % file)[1] == 0:
			self.file_to_be_parsed = "%s" % basename
	
	def parsefile(self, file):
		print "parsing file: ", file
		print execBash("./searchgramar signals_ver4.3.1.xml %s" % file)
		self.parsed_filename = "%s_parsed_output.txt" % file
	
	def compareFirstTime(self):
		result = self.CORRECT
		if len(self.firstline) != 2:
			mylen = len(self.firstline)
			print ("\033[1;31mWarning!! length of self.firstline is %d\033[0m " % mylen)
			print "self.firstline: ", self.firstline
			return self.WRONG
		if self.firstline[0]!=self.firstline[1]:
			print ("\033[1;31mWarning!! first line time stamp are "
			"different: \n%s\n%s\033[0m" % (self.firstline[0], self.firstline[1]))
			result = self.WRONG
		return result
		
	def extractContent(self, file):
		#print "\n\n########## start parsing #########"
		print "\n\n"
		print "filename: ", file
		fp = open(file)
		is_first_line = False
		wl = None

		for line in fp:
			#print line
			res = re.match(" TimeStamp.*", line)
			if res:
				print res.group(0)
				if is_first_line:
					self.firstline.append(res.group(0))
					is_first_line = False
				continue

			## looking for indicative header
			res = re.match(" DATA TYPE.*", line)
			if res:
				print "*"*50
				print res.group(0)
				print "*"*50
				is_first_line = True
				continue

		if self.compareFirstTime()==self.WRONG:
			print "line is wrong 1"
			if not wl:
				wl = WrongLine(file, "firstline", self.firstline[0], self.firstline[1])
			else:
				wl.add_wrongline("firstline", self.firstline[0], self.firstline[1])
			self.wrongline.append(wl)
		del self.firstline[:]
		#print "########## end of parsing #########\n\n"
		print "\n\n"
			

	
	def execute(self):
		print "Executing..."
		self.filelist = glob.glob(self.filename)
		print self.filelist

		for file in self.filelist:
			self.file_to_be_parsed = file
			self.parsed_filename = file
			if self.is_zip: self.gunzipfile(file)
			if self.is_not_parsed: self.parsefile(self.file_to_be_parsed)
			self.extractContent(self.parsed_filename)

		if self.wrongline:
			print "-- line that could be wrong --"
			for wl in self.wrongline:
				wl.print_me()


if __name__ == "__main__":   #if it is standalone(./xxx.py), then call main
	print "Executing as a standalone application..."
	(options, args) = parseCmd()
	## options are like --list-file, -l etc
	## arguments is the parameters passed by user

	## begin parser
	log = None
	if args:
		print "args: ", args
		log = ExtractTime(args[0]) 
	else:
		log = ExtractTime()
	
	log.filename="Probe-ttprb00017*bin_parsed_output.txt"

	if options.is_not_parsed:
		log.is_not_parsed = True
		log.filename="Probe-ttprb00017*bin"

	## if the file is zipped, it need to be parsed as well
	if options.is_zip:
		log.is_zip = True
		log.is_not_parsed = True
		log.filename="Probe-ttprb00017*bin.gz"
	

	print " -- log's attribute -- "
	print log.__dict__
	log.execute()

