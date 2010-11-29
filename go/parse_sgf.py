#!/usr/bin/python
# return a sequence of stone suitable to be used on nokia S60py
# this module is written in a way that it should be easy to be ported desktop app as well
# format of sequence = [[color, coordinate, captured_after_sequence], [...], [...] ...]

import re
import string        # for atoi
from dbg_print import dbg_p as dbg_p
from dbg_print import dbg_p2 as dbg_p2
from add_stone import AddStone as AddStone

def draw_game(size, seq):
	board = size*[size*['. ']]
	for row in board:
		print '			', ''.join(row)

class parse_sgf(object):
	## class variable
	## game = [ [common variation for all - variant0], [variant1, variant2, ... ]]
	## game_var = [variation-x, child, line (;, column (;, line ), column )]
	game_var = []
	g = 0
	var = 0
	## parents' index in game_var
	par = 0
	## prop_start store the index of (; in game_var
	prop_start = []
	next_var_ready = False
	reg_bw=re.compile(r";(W|B)\[([^\]]*)\]")
	reg_prop = re.compile('\(;')
	reg_prop_se = re.compile('(\(;)|(\)$)')
	game = []
	game_lines = None
	game_info_dict = {}
	game_info_key = [	'RU', 'KM', 'PW', 'PB', 'WR',
						'BR', 'GN', 'DT', 'PC', 'AB', 'RE']
	game_info_key_i = [	'SZ', 'HA', 'TM']		# integer based value
	reg_comment_s = re.compile("C\[")
	reg_comment_e = re.compile(r"(.?])")
	comment_line = []
	comment_line_g = []
	game_line_del = []
	is_comment = False


	#------ < __init__ > ------
	def __init__(self, fp):
		game_str = ""
		self.game_lines = fp.readlines()

		## parse comment
		self.parse_comment()
		self.print_comment()
		self.remove_comment()
		self.delete_comment()

		## look for the first (main) variation
		for i, line in enumerate(self.game_lines):
			res = self.reg_prop.search(line)
			if res:
				dbg_p("firstline:",line[:-1])
				self.game_var.append([[self.var], 0, i, res.start(), None])
				self.prop_start.append(len(self.game_var)-1)
				print "prop_start:*****", self.prop_start
				break

		## find out the line the game play sequence started
		for m, line in enumerate(self.game_lines[i:]):
			result = self.reg_bw.search(line)
			if not result:
				game_str+=line[:-1]
			else:
				break

		## check if game play sequence start on the line first property (; start
	#	if m > i:
	#		## both not on the same line
	#		self.var += 1

		## get game info
		self.parse_game_info(game_str)

		### parse game play
		self.parse_game_play(m)

		### print parsed game
		print "var:", self.var
		print self.game_var
		print self.prop_start

		## free up space
		del self.game_lines

	#------ < parse_comment > ------
	def parse_comment(self):
		grp="c"
		for i, line in enumerate(self.game_lines):
			line = line.rstrip()
			#print len(line), "line:", line
			if len(line) == 0:
				#print "empty line ****** "
				self.game_line_del.append(i)
				#print self.game_line_del
				continue
			if not (self.is_comment):
				self.parse_comment_single(i, line)
			else:
				## handle multiple line commnets
				#dbg_p2(grp, "self.is_comment=True,", line)
				ret = self.parse_comment_multiline(i, line)
				if ret:
					self.parse_comment_single(i, line[ret[1]:])
			#dbg_p2(grp,"final:", self.comment_line_g)


	#------ < parse_comment_single > ------
	def parse_comment_single(self, i, line):
		grp = "c"
		res = self.reg_comment_s.search(line)
		#print "parsing:", line.rstrip()
		if res:
			dbg_p2(grp,"comment_s: ", res.group())
			self.comment_line[0:]=i, res.start()
			#print "added:", comment_line
			self.is_comment = True
			#print "b4:", line.rstrip()
			#print "b4:", line[res.end():]
			self.parse_comment_multiline(i, line[res.end():])
			## search for end of comment
			## (i.e. start & end on same line) - single line


	#------ < parse_comment_multiline > ------
	# return True if found the end of previous comment
	def parse_comment_multiline(self, i, line):
		res = self.reg_comment_e.search(line)
		#print "line2:", line
		while res:
			#print "inside multiline"
			if line[res.start()] == "\\":
				## comment not ended yet
				#print "inside multiline: continue1"
				res = self.reg_comment_e.search(line, res.end())
			else:
				#print "inside multiline: stop", res.group(), line[res.start()]
				self.is_comment = False
				self.comment_line[2:]=i,res.end()-1
				#print "added2:", comment_line
				self.comment_line_g.append(self.comment_line[:])
				return True, res.end()


	#------ < print_comment > ------
	def print_comment(self):
		grp = "c"
		dbg_p2(grp,self.comment_line_g)
		for comment in self.comment_line_g:
			if comment[0]==comment[2]:
				## comment on single line
				dbg_p2(grp,\
				  self.game_lines[comment[0]][comment[1]:comment[3]+1])
			else:
				## comments on multiple line
				dbg_p2(grp,self.game_lines[comment[0]][comment[1]:])
				dbg_p2(grp,self.game_lines[comment[2]][:comment[3]+1])
				

	#------ < remove_comment > ------
	def remove_comment(self):
		for comment in self.comment_line_g:
			if comment[0]==comment[2]:
				## comment on single line
				self.game_lines[comment[0]]= \
					self.game_lines[comment[0]][:comment[1]+1]+\
					self.game_lines[comment[0]][comment[3]+1:]
			else:
				## comments on multiple line
				self.game_lines[comment[0]] = \
					self.game_lines[comment[0]][:comment[1]+1]
				self.game_lines[comment[2]] = \
					self.game_lines[comment[2]][comment[3]+1:]
				## prepare list of line which contain only comment
				if comment[1] == 0:
					## start of comment of first line comment == 0, 
					## i.e. whole line is comment
					self.game_line_del.append(comment[0])
				if comment[3] == len(self.game_lines[comment[2]]):
					## length of second line comment end == length of that line
					self.game_line_del.append(comment[2])
		#for line in self.game_lines:
		#	print line[:-1]


	#------ < delete_comment > ------
	def delete_comment(self):
		m = 0
		#print "game_line_del:", self.game_line_del
		for i in sorted(self.game_line_del):
			del self.game_lines[i-m]
			m +=  1
		## print remaining lines in game_lines
		print "start of game === "
		for line in self.game_lines:
			print line[:-1]
		print "end of game === "

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
		#print self.game_info_dict


	#------ < parse_game_play > ------
	def parse_game_play(self, i):
		for n, line in enumerate(self.game_lines[i:]):
			print ""
			print "line:", line[:-1]
			prop = self.reg_prop_se.search(line)
			while prop:
				#print "prop0:", prop.group()
				#print "len=",len(line),"; end=",prop.end()
				print "var:", self.var
				print "game_var:", self.game_var
				if line[prop.start()] == '(':
					print "next_var_ready", self.next_var_ready
					if self.next_var_ready:
						self.next_var_ready = False
						self.var += 1
					print "prop1:", prop.group()
					self.game_var.append(
						[[self.var], self.prop_start[-1], i+n, prop.start(), None])
					### update child-parent relationship
					self.update_var()
					#self.update_kid()
					#print "prop_start:", self.prop_start
					self.prop_start.append(len(self.game_var)-1)
					#print "prop1:", prop.start(), ", ", start_pos
				else: ## match ')'
					print "match ); prop_start=", self.prop_start
					my_prop = self.prop_start.pop(-1)
					self.game_var[my_prop][-1:] = i+n, prop.start()
					self.next_var_ready = True
				prop = self.reg_prop_se.search(line, prop.end())
#			res = self.reg_bw.search(line,start_pos)

#			while res:
#				print "res:",res.group()
#				prop = self.reg_prop.search(line, res.end()-1)
#				if prop:
#					print "prop2:", prop.group()
#					start_pos = prop.end()-1
#				else:
#					start_pos = res.end()-1
#				res = self.reg_bw.search(line,start_pos)

	#------ < update_var > ------
	def update_var(self):
		parent = -1
		while True:
			parent = self.game_var[parent][1]
			cur = self.game_var[parent][0]
			if self.var not in cur:
				cur.append(self.var)
			else:
				break

	#------ < update_kid > ------
	def update_kid(self):
		parent = -1
		kid_index = len(self.game_var)-1
		while True:
			parent = self.game_var[parent][1]
			print "parent:", self.game_var[parent]
			self.game_var[parent][-1].append(kid_index)
			if parent == 0:
				break

if __name__ == "__main__":   #if it is standalone(./xxx.py), then call main
	#draw_game(19,[])
	#draw_game(13,[])
	#draw_game(9,[])
	#fp = open('game2.sgf', 'r')
	fp = open('test.sgf', 'r')
	#fp = open('2009-9-29-sai2004-kumano.sgf', 'r')
	parse_sgf(fp)
