#!/usr/bin/python
'''
usage: to load the android files to vim
'''
#----------------- import ----------------#
import optparse
import subprocess
import socket

#----------------- global (user customizable) variable ----------------#
xml_cmd='find . -name "*.xml" | /bin/egrep -v bin | /bin/egrep -v values-v*'
java_cmd='find . -name "*.java" | /bin/egrep -v R.java\|BuildConfig.java'
load_vim='gvim --servername %s --remote ' % (socket.gethostname())

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

	result_xml = execBash(xml_cmd)[0];
	result_java = execBash(java_cmd)[0];

	result_arr = result_xml.split();
	result_arr.extend(result_xml.split());

	for i, line in enumerate(result_arr):
		print ("%d - %s" % (i, line))

	print("\n")
	choices= raw_input("docs to load (multiple docs separate by space): ");

	for choice in choices.split():
		execBash(load_vim+result_arr[int(choice)], is_print=True)[0]
	

#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()
