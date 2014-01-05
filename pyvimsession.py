#!/usr/bin/python
'''
usage: to load vim session file
'''

#----------------- import ----------------#
import optparse
import subprocess
import socket
import os
import getpass
import sys

#----------------- global (user customizable) variable ----------------#
xml_cmd='find . -name "*.xml" | /bin/egrep -v bin | /bin/egrep -v values-v*'
java_cmd='find . -name "*.java" | /bin/egrep -v R.java\|BuildConfig.java'
load_vim='gvim --servername %s --remote ' % (socket.gethostname())
dir_vim_session=os.path.join("/home", getpass.getuser(),"kn_vimsession")
check_dir_exist="ls %s" % (dir_vim_session)
vim_cmd='ls %s%s*.vims' % (dir_vim_session, os.sep)
vim_session="gvim --servername %s -S " % (socket.gethostname())
load_vim_session=vim_session+" %s &"

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)   #when --help is used or when wrong opt
	#parser.add_option("-l", "--list-file",
	#		action="store_true", dest="list_file",
	#		help="list all changed files")  # set options.verbose=True
	#parse_args(arg) arg (default) = sys.argv[1:]
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
		print ("\033[1;31mWarning!! command (%s) not ended properly."
				"exit status = %d\033[0m" %(cmd, p.returncode))
	#out = p.stdout.read()
	#print out
	return (stdoutdata, p.returncode)


#----------------- main() ----------------#
def main():
	#(options, args) = parseCmd()
	result_arr = []

	result_dir_exist = execBash(check_dir_exist, True)[1];
	#print result_dir_exist
	if (0!=result_dir_exist):
			print("%s is not exist. Program Ended." % (dir_vim_session))
			sys.exit(2)

	result_vim = execBash(vim_cmd, True)[0]
	#result_xml = execBash(xml_cmd)[0];
	#result_java = execBash(java_cmd)[0];

	if ( ""==result_vim ):
			print("No vim session (.vims) found. Program Ended.")
			sys.exit(2)

	result_arr = result_vim.split();
	#result_arr.extend(result_java.split());

	for i, line in enumerate(result_arr):
		print ("%d - %s" % (i, line))

	print("\nDocument(s) to load. *(all), c(cancel)")
	print("Multiple documents separated by space, e.g.: 3 5\n")
	choices= raw_input("Doc(s) to load : ");

	if ( choices == "*"):
		for myfile in result_arr:
			execBash(load_vim_session % myfile, is_print=True)[0];
	elif ( choices == "c"):
		print("Operation cancelled")
	else:
		for choice in choices.split():
			execBash(load_vim_session % result_arr[int(choice)], is_print=True)[0];
	

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()
