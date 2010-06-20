import appuifw, e32

def play():
	print "play"

def volume_up():
	print "volume_up"

def volume_down():
	print "volume_down"

def quitApp():
	print "Exiting..."
	app_lock.signal()

appuifw.app.exit_key_handler = quitApp
appuifw.app.title = u"mp3 player"
appuifw.app.menu = [(u"Play", play), 
	(u"Volume", ((u"Up", volume_up), (u"Down", volume_down)))]

print "App is running..."
app_lock = e32.Ao_lock()
app_lock.wait()
