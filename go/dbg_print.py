#!/usr/bin/python

#debug=False
debug=True
# whatever named in the group, the debug msg will be printed
# c=comment
group_g = []
#group_g = ["c"]

def dbg_p(*args):
	if not debug:
		pass
	else:
		print args

def dbg_p2(group, *args):
	if group in group_g:
		print args

