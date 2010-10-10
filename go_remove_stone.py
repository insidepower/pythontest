#!/usr/bin/python
# RemoveStone: this class will group solidly connected black or white
#   stones. When a particular group has no more liberty, the stones'
#	coordinate in the group will be passed back to the caller.
#
# w_grp: is white groups of stones which are solidly connected together
#	each item (which is a set type) in this group will have -
#		a) all the liberties of this group has
#		b) coordinate/position of all the stones in this group
#	e.g: [[(liberty_positions),(stone_positions)], [..], [..], ...]

class RemoveStone(object):
	w_grp = []
	b_grp = []

	def __init__ (self):
		pass

	def remove_stone(self, pos, color):
		combine=None
		print ""
		print "pos =",pos, "; color =", color
		if color == 'w':
			print "white"
			grp = self.w_grp
			opp_grp = self.b_grp
		else:
			print "black"
			grp = self.b_grp
			opp_grp = self.w_grp

		## add to group(s) which is solidly connected with this stone
		## if this stone connected to more than one group, combine these
		## two groups
		## hint: if this stone is one of the liberty in this group, it
		## means it is solidly connected to this group
		if grp:
			for i,x in enumerate(grp):
				print "grp: enumerate:",i,x
				if pos in x[0]:
					print "belong to group ",i
					x[0].remove(pos)
					x[1].update(pos)
					if combine:
						grp[combine][0].update(x[0])
						grp[combine][1].update(x[1])
						del grp[combine]
					else:
						combine=i

		## if does not belong to any group, or grp is empty
		if (not combine) or (not grp):
			print "not belong to any group"
			grp.append([set(self.my_liberty(pos)),set([pos])])
			## if it is the last liberty, return to caller
			## the captured stons (set type)

		## check if x is one of the liberty in this (opposite) group
		#if grp and [(i,x) for i,x in enumerate(grp) if pos in x[0]]:
		#if grp and [x for x in ['aa'] if pos in x[0]]:
		if opp_grp:
			for i,x in enumerate(opp_grp):
				print "opp_grp: enumerate:",i,x
				if pos in x[0]:
					print "reduce the liberty of opp_grp [", i, "]"
					me=grp[i]
					## if it is the last liberty, return to caller
					## the captured stons (set type)
					if len(me[0])==1:
						captured=me[1]
						del me[1]
						return captured
					else:
						me[0].remove(pos)
				else:
					print "not in grp"
		print grp

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
		print "liberty:",liberty
		return liberty

if __name__ == "__main__":   #if it is standalone(./xxx.py), then call main
	test=RemoveStone()
	test.remove_stone('sa', 'b')
	test.remove_stone('sb', 'w')
	test.remove_stone('rb', 'b')
	test.remove_stone('ra', 'w')

### test
# B[sa];W[sb];B[rb];W[ra]
### result ###
# ['ra', 'sb']
# ['rb', 'sa', 'sc']
# ['qb', 'sb', 'ra', 'rc']
# ['qa', 'sa', 'rb']

