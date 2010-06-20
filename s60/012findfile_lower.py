import os, appuifw

def find(dir, filename):
	# print out the path currently examining
    # print dir
    for name in os.listdir(dir):
        path = os.path.join(dir.lower(), name)
        if name.lower() == filename:
            return path
        if os.path.isdir(path):
			# recursive find into each sub-dir
            r = find(path, filename)
            if r is not None:
                return r

info = appuifw.multi_query(u"Directory:", u"Filename:")
if info:
	my_dir, my_filename=info
	#print find('c:\\Data', 'hello.py')
	print find(my_dir.lower(), my_filename.lower())
