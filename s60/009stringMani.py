txt = "I like Python"

print txt[2:6]			# like
print txt.find("like")	# 2
if txt.find("love") == -1:
	print "What's wrong with you?"
	print txt.replace("like", "love") ## new string

print txt.upper()  # I LIKE PYTHON
print "Length", len(txt)  ## 13

txt2 = ""
if txt2:
	print "txt2 contains characters"
else:
	print "txt2 doesn't contain characters" ## this line printed


url= " http://www.mopius.com "
url= url.strip()   #r remove space at the back

if url.startswith("http://"):
	print url, "is a valid URL"  ## this line printed

webServiceInput= " 1, 2, 3, 4"
print webServiceInput.replace(" ", "") # no space

txt = "one;two;three"
print txt.split(";")    # ['one', 'two', 'three']
