#!/usr/bin/python
import subprocess

## execute the bash command
#def execBash(cmd):
#	print cmd
#	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#	out = p.stdout.read()
#	#print out
#	return out
def execBash(cmd, is_suppress=False, is_print_cmd=False):
	if is_print_cmd:
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

## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	out=execBash('echo "testing"')
	print out
