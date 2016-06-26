def find_loc(message):
	locations = ['Richmond Hill', 'First Markham Place', 'Fmp', 'Markham', 'Kitchener', 'Waterloo', 'Loo ', 'Fairview Mall', 'Fairview', 'North York', 'Yorkdale Mall', 'Yorkdale', 'Scarborough Town Center', 'Scarborough', 'Stc', 'Downtown Toronto', 'Dt Toronto', 'Toronto', 'Dt', 'Pacific Mall', 'Pmall', 'Newmarket', 'Brampton', 'Pearson Airport', 'Pearson', 'Don Mills', 'Don Mills Station', 'Square One', 'Mississauga', 'Brantford', 'Oakville', 'Vaughan', 'Ajax', 'Hamilton', 'Guelph', 'Ottawa', 'Finch Station', 'Bk Plaza', 'Bk']
	identified_loc = {-1:None}
	lowest_index = -1
	for location in locations:
		loc_index = message.find(location)
		if loc_index != -1:
			identified_loc.update({loc_index:location})
			#print loc_index
			if lowest_index == -1 or lowest_index >= loc_index :
				lowest_index = loc_index
			message = message.replace(location,'')
	return identified_loc[lowest_index]

def location_scan(message):
	message = message.title()
	if '->' in message:
		message = message.split('>')
	elif ' To ' in message:
		message = message.split(' To ')
	else:
		print 'COULD NOT FIND IDENTIFIER, RETURN'
		return False
	
	if ' From ' in message[0]:
		from_message = message[0].split(' From ')[1]
	else:
		from_message = message[0]

	to_message = message[1]
	duplicate_item = []
	
	from_message = find_loc(from_message)
	if from_message == None:
		from_message = 'Waterloo'
	to_message = find_loc(to_message)
	if to_message == None:
		print 'COULD NOT IDENTIFY LOCATIONS, RETURN'
		return False		

	print 'From: '+str(from_message)
	print 'To: '+str(to_message)