#!/usr/bin/python

__metaclass__ = type

class MyClass:
	@staticmethod
	def my_static_method():
		print "staticmethod"
	
	@classmethod
	def my_class_method(clas):
		print "classmethod"

MyClass.my_static_method()
MyClass.my_class_method()
