try:
    f = file(u"c:\\Data\python\\delete.txt", "w+")
    print >> f, "Welcome to Python"
    f.seek(0)
    print "File =", f.read()
    f.close()
except IOError, reason:
    print reason
