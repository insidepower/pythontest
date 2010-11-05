#!/usr/bin/python
# sample references from Magnus Lie Hetland (with modification for testing purpose)

nested = [[1,2], [3,4]]

def flatten(nested):
	for sublist in nested:
		for elem in sublist:
			yield elem

for num in flatten(nested):
	print num

print list(flatten(nested))


def safe_flatten(nested):
	try:
		# Don't iterate over string-like object
		for sublist in nested:
			if isinstance(sublist, basestring):
				yield sublist
				continue
			for elem in flatten(sublist):
				if isinstance(elem, basestring):
					yield elem
					continue
				try: elem + ''
				#except TypeError: pass    # break inner try, go to next statement
				except TypeError: print "TypeError1: ", nested    # break inner try, go to next statement
				else: 
					yield elem
					continue
				yield elem		  # flat level of list

	except TypeError:
		print "string: ", nested
		yield nested			# a string

nested_str = ['foo', ['bar', ['barz']]]
print list(safe_flatten(nested_str))
