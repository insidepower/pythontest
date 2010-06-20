import inbox, appuifw

# Create an instance of the Inbox object
box = inbox.Inbox()
index = "0"

# Query search phrase
query = appuifw.query(u"Search For:", "text") #query==None if user cancel search
if query != None:
	query = query.lower()
	hits = []
	ids = []

	# sms_messages() return message IDs for all msg in SMS inbox
	for sms_id in box.sms_messages():
		# Retrieve the full message text and convrt it to lowercase
		msg_text = box.content(sms_id).lower()
		if msg_text.find(query) != -1: ## text found
			hits.append(msg_text[:25])  # store a preview
			ids.append(sms_id)

	# NOTE: index=None(cancel), index==-1 (OK button)
	while index != None:
		# Display all results in a list
		index = appuifw.selection_list(hits, 1)

		if index >= 0:
			# show the full text
			appuifw.note(box.content(ids[index]))
			print box.content(ids[index])
