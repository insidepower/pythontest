#!/usr/bin/python 
'''
usage :
	- able to unzip the xxx.bin.gz
	- able to parse xxx.bin using searchgramar server parser tool
	- will extract the TimeStamp from xxx_parsed_output.txt
	- check for the discontinuity of the TimeStamp

'''

import optparse
import subprocess
import re
import os
import sys
import calendar
from optparse import OptionParser
import glob
import datetime

version = 0.3
#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = \
	'''
software version = %.1f
Before running the tool, make sure the either xxx.bin.gz or xxx.bin or \
xxx.bin_parsed_output.txt is presented in the same directory where this \
scripts is placed

usage: to unzip the (multiple) xxx.bin.gz file, parse it, and check for the \
continuous time
	$ dcm_extract_time.py -z

usage: to parse the (multiple) xxx.bin file, then check for continuous time stamp
	$ dcm_extract_time.py -p

usage: to check for (multiple) continuous time stamp of xxx.bin_parsed_output.txt files
	$ dcm_extract_time.py

usage: to check for missing file only
	$ dcm_extract_time.py -c
	$ dcm_extract_time.py -c 'FILE_MATCHING_*PATTERN'

usage: to check for continuous time stamp of a single file \
(xxx.bin, xxx.bin.gz xxx.parsed_output.txt)
	$ dcm_extract_time.py
	''' % version
	parser = OptionParser(usage)   #when --help is used or when wrong opt
	parser.add_option("-z", "--is_zip",
			action="store_true", dest="is_zip",
			help="to indicate it is gunzipped file")  # set options.verbose=True
	parser.add_option("-p", "--is_not_parsed",
			action="store_true", dest="is_not_parsed",
			help="to indicate the file is not parsed")  # set options.verbose=True
	parser.add_option("-c", "--count_only",
			action="store_true", dest="count_only",
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
		print "filename: ", self.filename
		print "total possible error: ", len(self.info)
		for line in self.info:
			print ("%d: @@@@@  reason: %s  @@@@@" % (i, line[0]))
			print "line1: ", line[1]
			print "line2: ", line[2]
			i += 1
		print "\n"
		#print "~"*100

#----------------- class ExtractTime() ----------------#
class ExtractTime(object):
	filename=None
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
	NOT_EVEN = 0xFF
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
	totalfile = 0
	check_all = True
	record_line = []

	def __init__(self, fn=None, is_zip=False):
		#print "ExtractTime: init"
		self.filename="Probe-*bin_parsed_output.txt"
		(options, args) = parseCmd()
		self.is_zip = False
		self.is_not_parsed = False

		if options.is_not_parsed:
			self.is_not_parsed = True
			self.filename="Probe-*bin"

		## if the file is zipped, it need to be parsed as well
		if options.is_zip:
			self.is_zip = True
			self.is_not_parsed = True
			self.filename="Probe-*bin.gz"

		if sys.platform=="win32":
			if (options.is_zip or options.is_not_parsed):
				print "system used:", sys.platform
				print "Extraction and Parsing of files need to be run in linux/cygwin"
				print "Please extract the file before running it in window"
				user_in = raw_input("do you want to continue? Thing may be broken... (y/n): ")
				if 'y' == user_in.lower():
					print "Application Ended\n"
					sys.exit(2)

		## if only interested in the lost files
		if options.count_only:
			self.check_all = False

		if args:
			self.filename=args[0]

		#print " -- log's attribute -- "
		print self.__dict__

		self.filelist = glob.glob(self.filename)
		self.filelist.sort()
		#print self.filelist
		self.totalfile = len(self.filelist)
		if self.totalfile == 0:
			print "no file found. Possible solution: "
			print "1. put xxx.bin file\n2. run with correct parameter"
			print "3. specify file pattern to find, e.g.: dcm_extract_time.py FILE*PATTERN"
			print "Application Ended"
			sys.exit(2)
		#print "Total file found: ", self.totalfile

		if not fn:
			if options.is_not_parsed:
				count1 = glob.glob("Probe-*bin.gz")
				count2 = glob.glob("Probe*parsed_output.txt")
				count1 = len(count1)
				count2 = len(count2)
				if count1 or count2:
					user_in = raw_input('There is %d of *.gz file and %d of '
							'*.bin_parsed_output.txt will not be processed '
							'this time. \nPlease run this tool again later with '
							'dcm_extract_time.py -z and dcm_extract_time.py.\n'
							'Another good suggestion is to move all *.gz and '
							'*.parsed_output.txt file to another folder first.\n'
							'Then run again.\n'
							'Continue with just *.bin only? (y/n) ' % (count1, count2))
					if 'n'== user_in.lower():
						print("Application Ended")
						sys.exit(2)
			if options.is_zip:
				count1 = glob.glob("Probe-*bin")
				count2 = glob.glob("Probe-*parsed_output.txt")
				count1 = len(count1)
				count2 = len(count2)
				if count1 or count2:
					user_in = raw_input('There is %d of *.bin file and %d of '
							'*.bin_parsed_output.txt will not be processed '
							'this time. \nPlease run this tool again later with '
							'dcm_extract_time.py -p and dcm_extract_time.py.\n'
							'Another good suggestion is to move all *.gz and '
							'*.parsed_output.txt file to another folder first.\n'
							'Then run again.\n'
							'Continue with just *.bin.gz only? (y/n) ' % (count1, count2))
					if 'n'== user_in.lower():
						print("Application Ended")
						sys.exit(2)

	

	def gunzipfile(self, file):
		basename, ext = os.path.splitext(file)
		if ext!=".gz":
			print ("\033[1;31mWarning!! %s not ended with gz\033[0m" % file)
		#print os.getcwd()
		if execBash("gunzip -f %s" % file)[1] == 0:
			self.file_to_be_parsed = "%s" % basename
	
	def parsefile(self, file):
		if not os.path.isfile("searchgramar"):
			print "Not able to find searchgramar. Application terminated"
			sys.exit(2)
		print "parsing file: ", file
		execBash("./searchgramar signals_ver4.3.1.xml %s" % file, True)
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

	## compare indicative and engineering pair to make sure both have the same time stamp
	def comparelinepair(self):
		result = self.CORRECT

		if len(self.linepair[0])!=len(self.linepair[1]):
			ind_len = len(self.linepair[0])
			eng_len = len(self.linepair[1])
			reason = "eng & ind pair is not even: ind(%d), eng(%d)" % (ind_len, eng_len)
			if not self.wl:
				self.wl = WrongLine(self.current_file, reason, "(check the file)", "(null)")
			else:
				self.wl.add_wrongline(reason, "(check the file)", "(null)")
			print ("\033[1;31mWarning!! %s\033[0m" % reason)
		else:
			for i in range(0, len(self.linepair[0])):
				#print "comparelinepair: i=", i, "; len0:", len(self.linepair[0]), "len1:", len(self.linepair[1])
				if self.linepair[0][i][36:]!=self.linepair[1][i][36:]:
					reason = "indicative and engineering pair are different" 
					if not self.wl:
						self.wl = WrongLine(self.current_file, reason, self.linepair[0][i],
								self.linepair[1][i])
					else:
						self.wl.add_wrongline(reason, self.linepair[0][i], self.linepair[1][i]);
					print ("\033[1;31mWarning!! line pair time stamp are "
					"different: \n%s\n%s\033[0m" % (self.linepair[0][i], self.linepair[1][i]))
					#result = self.WRONG
				#return result


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

		if len(self.linepair[0]) == 0:
			reason = "zero indicative pair!!"
			myline = "Check Parsed File" 
			if not self.wl:
				self.wl = WrongLine(self.current_file, reason, myline, myline)
			else:
				self.wl.add_wrongline(reason, myline, myline);
			print ("\033[1;31mWarning!! zero indicative pair!! \033[0m")
			return 

		prevline = self.linepair[0][0]
		#print prevline
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
			prevline = line

		
	def extractContent(self, file):
		#print "\n\n########## start parsing #########"
		print "\n\n"
		print "filename: ", file
		if not os.path.isfile(file):
			print "not able to find parsed file:", file
			print "Application Ended."
			sys.exit(2)
		fp = open(file)
		is_first_line = None
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
				if is_first_line == None:
					print ("\033[1;31mWarning!! indicative or engineering"
						"header should be found first before TimeStamp\033[0m")
					sys.exit(2)
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

		self.record_line.append([self.current_file, 
								len(self.linepair[0]), len(self.linepair[1])])
		self.comparelinepair()

		self.compare_incremental_time()

		if self.wl:
			print "adding wl..."
			self.wrongline.append(self.wl)

		del self.linepair[:]
		self.linepair = [[],[]]
		#print "########## end of parsing #########\n\n"
		print "\n\n"


	def checkForMissingFileSeq(self):
		if self.totalfile<=0:
			print "no file found, so not checking for missing file"
			return
		sortedfile = sorted(self.filelist)
		res = re.match("Probe.*-(.*)\.bin.*", sortedfile[0])
		prevSeq = 0
		startSeq = 0
		total_lost_file = 0
		missing_files = []
		if not res:
			print ("\033[1;31mWarning!! not able to get file seq from "
					"%s\033[0m" %(file))
		else:
			prevSeq = int(res.group(1))
			startSeq = prevSeq
		for file in sortedfile[1:]:
			res = re.match("Probe.*-(.*)\.bin.*", file)
			if not res:
					print ("\033[1;31mWarning!! not able to get file seq from "
						"%s\033[0m" %(file))
					continue
			seq = int(res.group(1))

			if (seq != (prevSeq+1)):
				for i in range(prevSeq+1,seq):
					missing_files.append(i)
				#print "prev seq:", prevSeq, "seq jumped: ", seq
				total_lost_file += (seq-prevSeq-1)
				#print "total lost file =", total_lost_file
			prevSeq =  seq

		print "-"*80
		print "Summary: File Lost"
		print "-"*80
		print "checking for lost file from start =", startSeq, "to end =", prevSeq
		if total_lost_file:
			print "\ntotal lost file =", total_lost_file
			print "missing file: ", missing_files
		else:
			print "result:  no file lost\n\n"


	## printing: filename, total indicative entries, total engineering entries
	def print_line_record(self):

		print "-"*80
		print("%-6s%-50s%-15s%-15s" % ("no.", "filename", "totalind", "totaleng"))
		print "-"*80
		for i, line in enumerate(self.record_line):
			print("%-6d%-50s%-15d%-15d" % (i, line[0], line[1], line[2]))
		print "total file checked = ", self.totalfile
		print "\n\n"


	def execute(self):
		#print "Executing..."
		if self.check_all:
			for file in self.filelist:
				self.file_to_be_parsed = file
				self.parsed_filename = file
				if self.is_zip: self.gunzipfile(file)
				if self.is_not_parsed: self.parsefile(self.file_to_be_parsed)
				self.extractContent(self.parsed_filename)

			self.print_line_record()

			print "*"*80
			print "* summary: line that could be wrong "
			print "*"*80
			if self.wrongline:
				#print "length of wrongline: ", len(self.wrongline)
				for wl in self.wrongline:
					wl.print_me()
			else:
				print "result: no error found\n\n"

		self.checkForMissingFileSeq()


if __name__ == "__main__":   #if it is standalone(./xxx.py), then call main
	#print "Executing as a standalone application..."
	print "Date:", datetime.datetime.now()
	log = ExtractTime()
	log.execute()

