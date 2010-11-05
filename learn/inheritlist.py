#!/usr/bin/python

class CounterList(list):
	def __init__(self, *args):
		super(CounterList, self).__init__(*args)
		self.counter = 0       # variable of this CounterList
	
	def __getitem__(self,index):
		self.counter += 1
		return super(CounterList, self).__getitem__(index)

cl = CounterList(range(10))

print cl
del cl[2:5]                           #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print cl.counter                      #0
print (cl[2]+cl[5])                   #13
print cl.counter                      #2

