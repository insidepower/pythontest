#!/usr/bin/python

## generate an infinite sequence
def checkIndex(key):
	if not isinstance(key, (int,long)): raise TypeError
	if key < 0: raise IndexError

class AriSeq:
	def __init__(self, start=0, step=1):
		self.start = start
		self.step = step
		self.changed = {}

	def __getitem__(self, key):
		checkIndex(key)
		try: return self.changed[key]
		except KeyError:
			return self.start+key*self.step

	def __setitem__(self, key, value):
		checkIndex(key)
		self.changed[key]=value

s = AriSeq(1,2)
print s[4]        # 9
s[4] = 2
print s[4]        # 2
print s[5]        # 11
