#!/usr/bin/python

class MyIterator:
	val = 0
	def next(self):
		self.val += 1
		if self.val > 5: raise StopIteration
		return self.val

	def __iter__(self):
		return self

s = MyIterator()
for seq in s:
	print seq
