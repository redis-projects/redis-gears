list = []
uid = 'abc123'

def test(x): 
	u = 'users:access:id:' + uid
	log('entry ' + u)

	if not list:
		log('getting access ids')
		list = execute('LRANGE', u, 0, -1)
		# log(''.join(list))  
	
	log('Key %s was %s with value: %s' % (x['key'], x['event'], x['value']))
	return x

gb = GB('KeysReader')
gb.foreach(test)
gb.register(prefix='person:*', mode="sync")