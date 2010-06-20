import appuifw, e32

def quitFunc():
    print"Exit key pressed"
    app_lock.signal()  ## release lock

appuifw.app.exit_key_handler= quitFunc   #function name with () to get ptr
appuifw.app.title= u"UIApp"

print"App is now running"
app_lock= e32.Ao_lock()
app_lock.wait()

print"Application exits"
