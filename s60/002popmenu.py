import appuifw

items = [u"firstchoice", u"second"]
index = appuifw.popup_menu(items, u"Your choice=")

if index == 0:
	appuifw.note(u"you choose first!")
elif index == 1:
	appuifw.note(u"you choose second")
else:
	appuifw.note(u"Cancel choice")

