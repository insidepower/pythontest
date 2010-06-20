import appuifw, messaging, sysinfo

# can use dict too, but here is more straightforward later on
infoNames = [u"Profile", u"Battery", u"Signal DBM"]
infoCalls = ["sysinfo.active_profile()", \
				"sysinfo.battery()", "sysinfo.signal_dbm()"]

# let the user choose the info 
choices = appuifw.multi_selection_list(infoNames, 'checkbox', 1)
infoSms = ""
for idx in choices:
	# Execute the statement(s) stored the in infoCalls-list thru eval
	# convert the result to a string and append it to the sms text
	infoSms += infoNames[idx] + ";" + str(eval(infoCalls[idx])) + ";"

# Query the telephone number
smsNum = appuifw.query(u"Number:", "text", u"56765767")
if smsNum:
	# send the sms if the user didn't cancel
	messaging.sms_send(smsNum, infoSms)
	print infoSms
