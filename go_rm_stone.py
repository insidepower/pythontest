#!/usr/bin/python
from dbg_print import dbg_p as dbg_p

class RemoveStone(object):
	## board=set(color+'pos', color+'pos2', ... )
	board = set()
	captured_stone = set()
	temp = set()
	pos = None
	color = None
	invert_color = None
	alive = False
	neighbour_checked=set()

	def rm_stone(self, pos, color, invert_color):
		dbg_p("")
		dbg_p("rm_stone: pos =", pos, "; color =", color)
		assert (pos not in self.board)
		self.pos = pos
		self.color = color;
		self.invert_color = invert_color
		## insert into board
		self.board.update([color+pos])
		dbg_p(self.board)
		self.neighbour_checked = set()
		self.alive = False
		self.recursive_check()
		if self.captured_stone:
			captured = self.captured_stone
			self.captured_stone = set()
			dbg_p("captured:", captured)
			## todo: remove captured stone from board
			return captured

	def recursive_check(self):
		for liberty in self.my_liberty(self.pos):
			dbg_p("liberty:", liberty)
			if self.invert_color+liberty not in self.board:
				## this group have liberty, ignore
				dbg_p("recursive_check: pass =", self.invert_color+liberty)
				pass
			elif self.invert_color+liberty in self.board:
				dbg_p("recursive_check:", self.invert_color+liberty)
				#self.neighbour_checked.add(self.pos)
				self.temp.add(liberty)
				if self.captured_check(liberty):
					self.captured_stone.update(self.temp)
				## reset variable
				self.temp = set()
				self.alive = False
				self.neighbour_checked = set()

	def captured_check(self, pos):
		dbg_p("captured_check: pos =", pos)
		for liberty in self.my_liberty(pos):
			if liberty in self.temp or liberty == self.pos:
				dbg_p("liberty in temp/self.pos:", liberty, ", so pass")
				continue

			dbg_p(" == liberty = ", liberty)

			## since some are shared liberty between a few stones,
			## we want to skip whatever we have checked previously.
			## if it has been checked, return False
			## or if this group is alive, return False
			if not self.alive and liberty not in self.neighbour_checked:
				self.neighbour_checked.add(liberty)
				dbg_p(" == neighbour_checked =", self.neighbour_checked, ";",self.alive)
			else:
				dbg_p(" == neighbour_checked : else, alive =", self.alive)
				return False

			## color here is inverted
			if self.invert_color+liberty in self.board:
				## found connect stone of same color, expand the liberty
				## and check if this group is being captured or not
				dbg_p("recursive capture check:", liberty)
				self.temp.add(liberty)
				self.captured_check(liberty)
			elif self.color+liberty not in self.board:
				## this group has at least one liberty
				dbg_p(" == captured_check: alive, liberty @", liberty)
				#dbg_p("captured_check: board:", self.board)
				self.alive = True
				return False
			elif self.color+liberty in self.board:
				## add the possible dead stone to temp
				self.temp.add(pos);
				dbg_p(" == temp =", self.temp)
			else:
				dbg_p(" *** why i am here *** ")
				## continue recursive check for possible captured stone
		return True

	def my_liberty(self, pos):
		## return the liberties of this stone have
		liberty=[]

		## get the neighbour base on first coordinate of pos
		if pos[0]=='a':
			liberty.append('b'+pos[1])
		elif pos[0]=='s':
			liberty.append('r'+pos[1])
		else:   ## a < pos[0] < s
			num=ord(pos[0])
			liberty.extend([chr(num-1)+pos[1], chr(num+1)+pos[1]])

		## get the neighbour base on second coordinate of pos
		if pos[1]=='a':
			liberty.append(pos[0]+'b')
		elif pos[1]=='s':
			liberty.append(pos[0]+'r')
		else:   ## a < pos[1] < s
			num=ord(pos[1])
			liberty.extend([pos[0]+chr(num-1), pos[0]+chr(num+1)])
		dbg_p("liberty:",liberty)
		return liberty

if __name__ == "__main__":   #if it is standalone(./xxx.py), then call main
	test=RemoveStone()
	testcase = 6;

if testcase == 1:
### test 1 ###
# B[sa];W[sb];B[rb];W[ra]
	print "\n captured: ", test.rm_stone('sa', 'B', 'W')
	print "\n captured: ", test.rm_stone('sb', 'W', 'B')
	print "\n captured: ", test.rm_stone('rb', 'B', 'W')
	print "\n captured: ", test.rm_stone('ra', 'W', 'B')

	### result ###
	# ['ra', 'sb']
	# ['rb', 'sa', 'sc']
	# ['qb', 'sb', 'ra', 'rc']
	# ['qa', 'sa', 'rb']

if testcase == 2:
### test 2 ###
	print "\n captured: ", test.rm_stone('rb', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('ra', 'W', 'B')
	print "\n captured: ", test.rm_stone('rc', 'W', 'B')
	print "\n captured: ", test.rm_stone('qb', 'W', 'B')
	print "\n captured: ", test.rm_stone('sb', 'W', 'B')

if testcase == 3:
### test 3 ###
	print "\n captured: ", test.rm_stone('rb', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('rc', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('rd', 'B', 'w')  ## captured
	print "\n captured: ", test.rm_stone('ra', 'W', 'B')
	print "\n captured: ", test.rm_stone('re', 'W', 'B')
	print "\n captured: ", test.rm_stone('qd', 'W', 'B')
	print "\n captured: ", test.rm_stone('sd', 'W', 'B')
	print "\n captured: ", test.rm_stone('qb', 'W', 'B')
	print "\n captured: ", test.rm_stone('sb', 'W', 'B')
	print "\n captured: ", test.rm_stone('qc', 'W', 'B')
	print "\n captured: ", test.rm_stone('sc', 'W', 'B')

if testcase == 4:
### test 4 ###
	print "\n captured: ", test.rm_stone('sa', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('sb', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('ra', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('rb', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('sc', 'W', 'B')
	print "\n captured: ", test.rm_stone('rc', 'W', 'B')
	print "\n captured: ", test.rm_stone('qa', 'W', 'B')
	print "\n captured: ", test.rm_stone('qb', 'W', 'B')

if testcase == 5:
### test 4 ###
	print "\n captured: ", test.rm_stone('qa', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('qb', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('qc', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('rc', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('sc', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('pa', 'W', 'B')
	print "\n captured: ", test.rm_stone('ra', 'W', 'B')
	print "\n captured: ", test.rm_stone('pb', 'W', 'B')
	print "\n captured: ", test.rm_stone('rb', 'W', 'B')
	print "\n captured: ", test.rm_stone('sb', 'W', 'B')
	print "\n captured: ", test.rm_stone('pc', 'W', 'B')
	print "\n captured: ", test.rm_stone('qd', 'W', 'B')
	print "\n captured: ", test.rm_stone('rd', 'W', 'B')
	print "\n captured: ", test.rm_stone('sd', 'W', 'B')

if testcase == 6:
	print "\n captured: ", test.rm_stone('qa', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('sa', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('qb', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('rb', 'B', 'W')  ## captured
	print "\n captured: ", test.rm_stone('pa', 'W', 'B')
	print "\n captured: ", test.rm_stone('pb', 'W', 'B')
	print "\n captured: ", test.rm_stone('sb', 'W', 'B')
	print "\n captured: ", test.rm_stone('qc', 'W', 'B')
	print "\n captured: ", test.rm_stone('rc', 'W', 'B')
	print "\n captured: ", test.rm_stone('ra', 'W', 'B')
