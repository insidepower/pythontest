#!/usr/bin/python 
'''
usage :
	- able to unzip the xxx.bin.gz
	- able to parse xxx.bin using searchgramar server parser tool
	- will extract the TimeStamp from xxx_parsed_output.txt
	- check for the discontinuity of the TimeStamp

version : 0.1
'''

import optparse
import subprocess
import re
import os
import sys
import calendar
from optparse import OptionParser
import glob

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = \
	'''
Before running the tool, make sure the either xxx.bin.gz or xxx.bin or \
xxx.bin_parsed_output.txt is presented in the same directory where this \
scripts is placed

usage: to unzip the xxx.bin.gz file, parse it, and check for the continuous time
	$ extract_dcm_time.py -z

usage: to parse the xxx.bin file, then check for continuous time stamp
	$ extract_dcm_time.py -p

usage: to check for continuous time stamp
	$ extract_dcm_time.py
	'''
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
	info = None

	def __init__(self, filename, reason, line1, line2):
		#print "WrongLine: init - ", filename
		#print "length of info = ", self.info
		self.info = []
		self.filename=filename
		self.info.append([reason, line1, line2])
	
	def add_wrongline(self, reason, line1, line2):
		#print "add_wrongline: ", self.filename
		#print "length of info = ", self.info
		self.info.append([reason, line1, line2])

	def print_me(self):
		#print "~"*100
		i = 1
		print "\n\nfilename: ", self.filename
		print "total possible error: ", len(self.info)
		for line in self.info:
			print ("%d: @@@@@  reason: %s  @@@@@" % (i, line[0]))
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
	linepair=[[],[]]
	secondpair=[]
	firstline=[]
	wrongline=[]
	CORRECT = True
	WRONG = False
	wl = None
	current_file = None
	day1 = None
	mon1 = None
	year1 = None
	hr1 = None
	min1 = None
	sec1 = None
	day2 = None
	mon2 = None
	year2 = None
	hr2 = None
	min2 = None
	sec2 = None

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

	def comparelinepair(self, i):
		result = self.CORRECT
		if self.linepair[0][i][36:]!=self.linepair[1][i][36:]:
			reason = "indicative and engineering pair are different" 
			if not self.wl:
				self.wl = WrongLine(self.current_file, reason, self.linepair[0][i],
						self.linepair[1][i])
			else:
				self.wl.add_wrongline(reason, self.linepair[0][i], self.linepair[1][i]);
			print ("\033[1;31mWarning!! line pair time stamp are "
			"different: \n%s\n%s\033[0m" % (self.linepair[0][i], self.linepair[1][i]))
			result = self.WRONG
		return result

	def comparetime(self):
		min = self.min1
		hr = self.hr1
		sec=(self.sec1+1)%60
		day = self.day1
		mon = self.mon1
		year = self.year1
		if sec == 0:
			min = (min+1)%60
			if min == 0:
				hr = (hr+1)%24
				if hr == 0:
					max_day = calendar.monthrange(self.year1, self.mon1)[1]
					day = (day+1)% max_day
					if day == 0:
						mon = (mon+1)%12
						## month = 1-12
						if mon == 1:
							year = year+1
		#print "sec =", sec
		#print "self.sec2 = ", self.sec2
		if sec!=self.sec2:
			print "second is not continuous..."
			return self.WRONG
		else:
			## second is continuous
			if(min!=self.min2 or hr!=self.hr2):
				print "minute or hour is not continuous..."
				return self.WRONG
			elif (day!=self.day2 or mon!=self.mon2 or year!=self.year2):
				print "day, month or year is not continuous..."
				return self.WRONG
			else:
				return self.CORRECT

	## compare_incremental_time: check for the continuous time stamp
	def compare_incremental_time(self):
		## we just check for indicative for the continuous time stamp
		## as in the comparelinepair we have compared both indicative and 
		## engineering data to make sure they are same
		prevline = self.linepair[0][0]
		print prevline
		self.day1 = int(prevline[36:38])
		self.mon1 = int(prevline[39:41])
		self.year1 = int(prevline[42:46])
		#print "dd:mm:yyyy = ", self.day1, self.mon1, self.year1

		self.hr1 = int(prevline[66:68])
		self.min1 = int(prevline[69:71])
		self.sec1 = int(prevline[72:74])
		#print "self.hr:self.min:self.sec = ", self.hr1, self.min1, self.sec1

		for i, line in enumerate(self.linepair[0][1:]):
			self.day2 = int(line[36:38])
			self.mon2 = int(line[39:41])
			self.year2 = int(line[42:46])
			#print "dd:mm:yyyy", self.day2, self.mon2, self.year2

			self.hr2 = int(line[66:68])
			self.min2 = int(line[69:71])
			self.sec2 = int(line[72:74])
			#print "self.hr:self.min:self.sec = ", self.hr2, self.min2, self.sec2

			if self.comparetime()==self.WRONG:
				reason = "time is not continuous"
				if not self.wl:
					self.wl = WrongLine(self.current_file, reason, prevline, line)
				else:
					self.wl.add_wrongline(reason, prevline, line);
				print ("\033[1;31mWarning!! line pair time stamp are "
				"not continuous: \n%s\n%s\033[0m" % (prevline, line))

			self.day1 = self.day2;
			self.mon1 = self.mon2;
			self.year1 = self.year2;
			self.hr1 = self.hr2;
			self.min1 = self.min2;
			self.sec1 = self.sec2;

		
	def extractContent(self, file):
		#print "\n\n########## start parsing #########"
		print "\n\n"
		print "filename: ", file
		fp = open(file)
		is_first_line = False
		self.wl = None
		self.current_file = file
		array_id = 1

		for line in fp:
			#print line
			res = re.match(" TimeStamp.*", line)
			if res:
				print res.group(0)
				if is_first_line:
					#self.firstline.append(res.group(0))
					is_first_line = False
					array_id ^= 1
					#print "array_id: ", array_id
				self.linepair[array_id].append(res.group(0))
				continue

			## looking for indicative header
			res = re.match(" DATA TYPE.*", line)
			if res:
				print "*"*50
				print res.group(0)
				print "*"*50
				is_first_line = True
				continue

		#if self.compareFirstTime()==self.WRONG:
		#	print "line is wrong 1"
		#	if not wl:
		#		wl = WrongLine(file, "firstline", 
		#				self.firstline[0][36:], self.firstline[1][36:])
		#	else:
		#		wl.add_wrongline("firstline", 
		#				self.firstline[0][36:], self.firstline[1][36:])
		#del self.firstline[:]

		for i in range(0, len(self.linepair[0])):
			self.comparelinepair(i)

		self.compare_incremental_time()

		if self.wl:
			print "adding wl..."
			self.wrongline.append(self.wl)
		self.linepair = [[],[]]
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
			print "*"*80
			print "* summary: line that could be wrong "
			print "*"*80
			#print "length of wrongline: ", len(self.wrongline)
			print ""
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

