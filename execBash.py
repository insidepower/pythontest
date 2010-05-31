#!/usr/bin/python
import subprocess

## execute the bash command
def execBash(cmd):
	print cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read()
	#print out
	return out

## if standalone, i.e. called directly from shell
if __name__ == '__main__':
	out=execBash('echo "testing"')
	print out
