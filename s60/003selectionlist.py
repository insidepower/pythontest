import appuifw

items = [u"firstchoice", u"second"]
index = appuifw.selection_list(items, 1)

if index == 0:
	appuifw.note(u"you choose first!")
elif index == 1:
	appuifw.note(u"you choose second")
else:
	appuifw.note(u"Cancel choice")
