import appuifw

names = [u"AA", u"BB", u"CC", u"DD"]
selections = appuifw.multi_selection_list(names, 'checkbox', 1)
print selections
