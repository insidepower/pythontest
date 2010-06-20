#!/usr/bin/python
import subprocess
year=2008
month=5
url=r"http://www.gokgs.com/servlet/archives/en_US/sai2004-%s-%s.zip"

while ( (year >= 2004) or (month==12)):
	cmd = "wget " + (url % (year, month));
	print cmd
	subprocess.call(cmd, shell=True)
	if (1==month):
		month=12;
		year-=1;
	else:
		month-=1
