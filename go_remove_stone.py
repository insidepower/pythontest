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
		if color == 'w':
			grp = self.w_grp
		else:
			grp = self.b_grp

		## check if x is one of the liberty in this group
		#if grp and [(i,x) for i,x in enumerate(grp) if pos in x[0]]:
		if grp and [x for x in ['aa'] if pos in x[0]]:
			print "inside"
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
			## not belong to the liberty of any group,
			## assign this stone as new group
			grp.append([self.my_liberty(pos),pos])

	def my_liberty(self, pos):
		## return the liberties of this stone have
		liberty=[None]
		if pos[0]=='a':
			liberty.extend('b'+pos[1])
		elif pos[0]=='s':
			liberty.extend('r'+pos[1])
		else:   ## a < pos[0] < s
			num=ord(pos[0])
			liberty.extend([chr(num-1)+pos[1], chr(num+1)+pos[1]])

if __name__ == "__main__":   #if it is standalone(./xxx.py), then call main
	test=RemoveStone()
	test.remove_stone('sa', 'b')
	test.remove_stone('sb', 'w')
	test.remove_stone('rb', 'b')
	test.remove_stone('ra', 'w')

#B[sa];W[sb];B[rb];W[ra]
