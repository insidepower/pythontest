#!/usr/bin/python
# return a sequence of stone suitable to be used on nokia S60py
# this module is written in a way that it should be easy to be ported desktop app as well
# format of sequence = [[color, coordinate, captured_after_sequence], [...], [...] ...]

import re
import string        # for atoi
from dbg_print import dbg_p as dbg_p
from add_stone import AddStone as AddStone

def draw_game(size, seq):
	board = size*[size*['. ']]
	for row in board:
		print '			', ''.join(row)

class parse_sgf(object):
	## class variable
	depth = 0
	reg_bw=re.compile(r";(W|B)\[([^\]]*)\]")
	game_lines = None
	game_info_dict = {}
	game_info_key = [	'RU', 'KM', 'PW', 'PB', 'WR',
						'BR', 'GN', 'DT', 'PC', 'AB', 'RE']
	game_info_key_i = [	'SZ', 'HA', 'TM']		# integer based value


	#------ < __init__ > ------
	def __init__(self, fp):
		game_str = ""
		self.game_lines = fp.readlines()

		## look for the first (main) variation
		for i, line in enumerate(self.game_lines):
			result = re.search('\(;', line)
			if result:
				dbg_p(line[:-1])
				self.depth += 1
				break

		## find out the line the game play sequence started
		for m, line in enumerate(self.game_lines[i:]):
			result = self.reg_bw.search(line)
			if not result:
				game_str+=line[:-1]
			else:
				break

		## get game info
		self.parse_game_info(game_str)

		## parse game play
		self.parse_game_play(i)

		## free up space
		del self.game_lines


	#------ < parse_game_info > ------
	def parse_game_info(self, game_str):
		for key in self.game_info_key:
			key_pattern = '%s\[([^\]]*)\]' % key
			#print "key_pattern = ", key_pattern
			result = re.search(key_pattern, game_str)
			if result:
				self.game_info_dict[key]=result.group(1)
			else:
				self.game_info_dict[key]=""

		## get game info which is integer based
		for key in self.game_info_key_i:
			key_pattern = '%s\[([^\]]*)\]' % key
			#print "key_pattern = ", key_pattern
			result = re.search(key_pattern, game_str)
			if result:
				self.game_info_dict[key]=string.atoi(result.group(1))
		print self.game_info_dict


	#------ < parse_game_play > ------
	def parse_game_play(self, i):
		for line in self.game_lines[i:]:
			start_pos = 0
			res = self.reg_bw.search(line,start_pos)
			while res:
				start_pos = res.start()+1
				print res.group()
				res = self.reg_bw.search(line,start_pos)


if __name__ == "__main__":   #if it is standalone(./xxx.py), then call main
	#draw_game(19,[])
	#draw_game(13,[])
	#draw_game(9,[])
	fp = open('test.sgf', 'r')
	#fp = open('2009-9-29-sai2004-kumano.sgf', 'r')
	parse_sgf(fp)
