#!/usr/bin/python
'''
usage: to load the android files to vim
'''
#----------------- import ----------------#
import optparse
import subprocess
import socket
from optparse import OptionParser

#----------------- global (user customizable) variable ----------------#
xml_cmd='find . -name "*.xml" | /bin/egrep -v bin | /bin/egrep -v values-v*'
java_cmd='find . -name "*.java" | /bin/egrep -v R.java\|BuildConfig.java'
load_vim='gvim --servername %s --remote ' % (socket.gethostname())
find_cmd='find . -name '

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)   #when --help is used or when wrong opt
	parser.add_option("-c", "--command_find",
			action="store", type="string", dest="filename",
			help="use find command from user")  # set options.verbose=True
	return parser.parse_args()  #options.filename, options.verbose..

#----------------- execBash() ----------------#
def execBash(cmd, is_suppress=False, is_print=False):
	if ( is_print ):
		print cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	#(stdoutdata, stderrdata) = p.communicate()
	stdoutdata = p.communicate()[0]
	p.poll()
	if (p.returncode != 0) and (not is_suppress):
		print ("\033[1;31mWarning!! command_find (%s) not ended properly."
				"exit status = %d\033[0m" %(cmd, p.returncode))
	#out = p.stdout.read()
	#print out
	return (stdoutdata, p.returncode)


#----------------- main() ----------------#
def main():
	(options, args) = parseCmd()
	result_arr = []

	if options.filename:
		result_command = \
			execBash(find_cmd+options.filename, is_print=True)[0]
		result_arr.extend(result_command.split());
	else:
		# use default cmd which look for java and xml
		result_xml = execBash(xml_cmd)[0];
		result_java = execBash(java_cmd)[0];

		result_arr = result_xml.split();
		result_arr.extend(result_java.split());

	for i, line in enumerate(result_arr):
		print ("%d - %s" % (i, line))

	print("\nDocument(s) to load. *(all), j(java), x(xml), c(cancel), empty(first doc)")
	print("Multiple documents separated by space, e.g.: 3 5\n")
	choices= raw_input("Doc(s) to load : ");

	if ( choices == "*"):
		for myfile in result_arr:
			execBash(load_vim+myfile, is_print=True)[0];
	elif ( choices == "x"):
		for i, myfile in enumerate(result_xml.split()):
			execBash(load_vim+myfile, is_print=True)[0];
	elif ( choices == "j"):
		for i, myfile in enumerate(result_java.split()):
			execBash(load_vim+myfile, is_print=True)[0];
	elif ( choices == "c"):
		print("Operation cancelled")
	elif ( choices == ""):
		print("Opening the first document")
		execBash(load_vim+result_arr[0], is_print=True)[0];
	else:
		for choice in choices.split():
			execBash(load_vim+result_arr[int(choice)], is_print=True)[0];
	

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()
