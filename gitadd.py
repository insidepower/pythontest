#!/usr/bin/python
import execBash
import optparse
import subprocess
from optparse import OptionParser
#import re

#----------------- parseCmd() ----------------#
## parse the command line arguments
def parseCmd():
	usage = "usage: %prog [options] bash-command\nE.g. %prog \'echo \"hello\"\'"
	parser = OptionParser(usage)   #when --help is used or when wrong opt
	parser.add_option("-a", "--add-all",
			action="store_true", dest="add_all",
			help="all the untracked file will be added")  # set options.verbose=True
	#parse_args(arg) arg (default) = sys.argv[1:]
	return parser.parse_args()  #options.filename, options.verbose..


#----------------- main() ----------------#
def main():
	file_to_add=""
	cmd="git status | sed -n '/Untracked/,$ s/#\t// p'"

	## parse command line options and arguments
	(options, args) = parseCmd()
	#print options
	#print args

	## split into lines
	#myline = re.split('\n', out)
	myline = execBash.execBash(cmd).splitlines()

	## iterate through to add wanted file
	for my_file in myline[3:]:
		#print line
		#my_file = line.lstrip('# \t')
		#print my_file

		## add file
		if options.add_all:
			file_to_add = file_to_add + " " + my_file
		else:		# interactive mode (default)
			input = raw_input("you want to add " + my_file + " (y/n): ")
			if input == 'y':
				file_to_add = file_to_add + " " + my_file

	#print file_to_add

	if file_to_add != "":
		## execute bash command
		out=execBash.execBash("git add"+file_to_add)
		print out


#----------------- standalone() ----------------#
## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	main()
