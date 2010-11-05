#!/usr/bin/python
# return a sequence of stone suitable to be used on nokia S60py
# this module is written in a way that it should be easy to be ported desktop app as well
# format of sequence = [[color, coordinate, captured_after_sequence], [...], [...] ...]

from dbg_print import dbg_p as dbg_p
from add_stone import AddStone as AddStone

def draw_game(size, seq):
	board = size*[size*['. ']]
	for row in board:
		print '			', ''.join(row)

def parse_sgf(fp):
	depth = 0
	for line in fp:
		## look for the first (main) variation
		first_var = line.find('(')
		if first_var != -1:
			dbg_p(line, '( @ ', first_var)
			depth += 1
			break

#	print "after"
	for line in fp:
		print line[:-1]

if __name__ == "__main__":   #if it is standalone(./xxx.py), then call main
	#draw_game(19,[])
	#draw_game(13,[])
	#draw_game(9,[])
	fp = open('test.sgf', 'r')
	parse_sgf(fp)
