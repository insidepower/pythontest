#!/usr/bin/python
import subprocess

p = subprocess.Popen('echo "to stdout"', shell=True,
		stdout=subprocess.PIPE)
stdout_value = p.communicate()[0]
print(repr(stdout_value))
print stdout_value
print str(stdout_value)
