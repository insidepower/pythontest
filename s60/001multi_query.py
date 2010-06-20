import appuifw

pwd = u"secret"

print "multi_query"

info = appuifw.multi_query(u"Username:", u"Password")
if info:	#returns a tuple with the info
	login_id, login_pwd = info
	if login_pwd == pwd:
		appuifw.note(u"Login successful", "conf")
	else:
		appuifw.note(u"Wrong password", "error")
else:
	appuifw.note(u"Cancelled")

