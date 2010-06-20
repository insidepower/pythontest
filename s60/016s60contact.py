import contacts

def search_name():
	db=contacts.open()
	my_contact = appuifw.query(u"name:", "text")
	print("-"*15)
	print ("search name: %s" %(my_contact,))
	result = db.find(my_contact)
	print result
	print("-"*15)

def search_number():
	db=contacts.open()
	my_number = appuifw.query(u"number:", "text")
	print("-"*15)
	print("number entered: %s" % (my_number,))
	for entry_id in db:
		for field in db[entry_id]:
			# suggestion: use field.mobile_number
			if my_number in repr(field.value):
				print("%s:%s" %(db[entry_id],field.value))
	print("-"*15)

count=0
def update_me(field):
	'''
	called by update_number to update the Mobile field
	'''
	global count
	info = 'update +65 ' +field.value
	items = [info, u"no update", u"Exit"]
	count += 1
	if count == 10:
		user_input = appuifw.selection_list(items, 0)
	else:
		user_input = 0

	if user_input == 0:
		field.value='+65'+field.value
		print field.value
		return 0
	elif user_input == 2:
		#print 'exiting'
		return -1
	else:
		return 0

def update_number():
	'''
	update the mobile number so that it start with +65
	'''
	db=contacts.open()
	print("-"*15)
	print(" searching for number not starting with +65")
	for entry_id in db:
		for field in db[entry_id]:
			#print ("%s:%s" % (field.label, field.value))
			if field.label == "Mobile":
				val=field.value[0]
				if val=='8' or val=='9' or val=='6':
					print db[entry_id]
					ret = update_me(field)
					if ret == -1:
						print 'exiting'
						return 0
	print("-"*15)

import appuifw
import e32
lock=e32.Ao_lock()
appuifw.app.menu=[
	(u'search name', search_name),
	(u'search number', search_number),
	(u'update number +65', update_number)
	]
old_exit_handler=appuifw.app.exit_key_handler
def exit_hander():
	appuifw.app.exit_key_handler=old_exit_handler
	lock.signal()

appuifw.app.exit_key_handler=exit_hander
lock.wait()
