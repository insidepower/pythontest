#!/usr/bin/python

class NewObj(object):         # must inherit object
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def setCoor(self, coor):
		self.x, self.y = coor
	
	def getCoor(self):
		return self.x, self.y

	coor = property(getCoor, setCoor)        # get first then only set attr
	# after this, we can use new-coor = NewObj.coor; NewObj.coor = x, y

my_obj = NewObj(10, 20)
print my_obj.coor			# (10, 20)
my_obj.coor = 50, 60
print my_obj.coor			# (50, 60)
