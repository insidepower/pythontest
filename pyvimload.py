#!/usr/bin/python
'''
usage: to load the android files to vim
'''
#----------------- import ----------------#
import optparse
import subprocess
import socket
import time
import sys
from optparse import OptionParser

#----------------- global (user customizable) variable ----------------#
xml_cmd='find . -name "*.xml" | /bin/egrep -v bin | /bin/egrep -v values-v*'
java_cmd='find . -name "*.java" | /bin/egrep -v R.java\|BuildConfig.java'
load_vim_host='gvim --servername %s --remote-tab-silent '
find_cmd='find . -name '
sleep_time=0.9

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)   #when --help is used or when wrong opt
	parser.add_option("-c", "--command_find",
			action="store", type="string", dest="filename",
			help="use find command from user")  # set options.verbose=True
	parser.add_option("-s", "--server",
			action="store", type="string", dest="server",
			help="")  # set options.verbose=True
	parser.add_option("-a", "--app",
			action="store", type="string", dest="app",
			help="")  # set options.verbose=True
	return parser.parse_args()  #options.filename, options.verbose..

#----------------- execBash() ----------------#
def execBash(cmd, is_suppress=False, is_print=False, no_output=False):
	if ( is_print ):
		print cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	#(stdoutdata, stderrdata) = p.communicate()

	if (False==no_output):
		stdoutdata = p.communicate()[0]
		p.poll()
		if (p.returncode != 0) and (not is_suppress):
			print ("\033[1;31mWarning!! command_find (%s) not ended properly."
					"exit status = %d\033[0m" %(cmd, p.returncode))
		#out = p.stdout.read()
		#print out
	else:
		stdoutdata=""
	return (stdoutdata, p.returncode)


#----------------- main() ----------------#
def main():
	(options, args) = parseCmd()
	result_arr = []
        result_java = None
        result_xml = None

	### specify new remote server
	if options.server:
		load_vim = load_vim_host % options.server
	else:
		load_vim = load_vim_host % (socket.gethostname())

	## use different file name than provided
	if args:
		result_command = \
			execBash(find_cmd+args[0], is_print=True)[0]
		result_arr.extend(result_command.split());
                print "main: use args"
	else:
		# use default cmd which look for java and xml
		result_xml = execBash(xml_cmd)[0];
		result_java = execBash(java_cmd)[0];

		result_arr = result_xml.split();
		result_arr.extend(result_java.split());
                print ("main: result_java %s" % (result_java))

	## determining application to use
	if options.app=="":
		load_vim="xdg-open "

	for i, line in enumerate(result_arr):
		print ("%d - %s" % (i, line))

	if (0==len(result_arr)):
		print("No matching file found.\n")
		sys.exit(0)

	print("\nDocument(s) to load. *(all), j(java), x(xml), c(cancel), empty(first doc)")
	print("Multiple documents separated by space, e.g.: 3 5\n")
	print("Or type part of the document name here\n")
	choices= raw_input("Doc(s) to load : ");

	if ( choices == "*"):
		for myfile in result_arr:
			execBash(load_vim+myfile, is_print=True, no_output=True)[0];
			# wait for 0.5 seconds
			time.sleep(0.5);
	elif ( choices == "x"):
            if result_xml is None:
                # arg is passed in
                result_final = result_arr;
            else:
                result_final = result_xml.split();

	    for i, myfile in enumerate(result_final):
                    execBash(load_vim+myfile, is_print=True, no_output=True)[0];
                    time.sleep(0.3);
	elif ( choices == "j"):
            load_vim_arr = load_vim.split()

            if result_java is None:
                # arg is passed in
                result_final = result_arr;
            else:
                result_final = result_java.split();

            for i, myfile in enumerate(result_final):
                    #load_vim_arr.append(myfile)
                    #execBash(load_vim_arr, is_print=True, use_shell=False);
                    #load_vim_arr.pop()

                    execBash(load_vim+myfile, is_print=True, no_output=True);
                    time.sleep(sleep_time);
	elif ( choices == "c"):
		print("Operation cancelled")
	elif ( choices == ""):
		print("Opening the first document")
		execBash(load_vim+result_arr[0], is_print=True)[0];
	else:
		is_digit = False
		for choice in choices.split():
			if choice.isdigit():
				execBash(load_vim+result_arr[int(choice)], is_print=True, 
							no_output=True)[0];
				is_digit=True
				time.sleep(sleep_time);
		if ( not is_digit ):
			for i,s in enumerate(result_arr):
				if (s.__contains__(choices)):
					execBash(load_vim+result_arr[i], is_print=True, 
								no_output=True)[0];
					time.sleep(sleep_time);


#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()
