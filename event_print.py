gb = GB('KeysReader')
gb.foreach(lambda x: log('Key %s was %s with value: %s' % (x['key'], x['event'], x['value'])))
gb.register(prefix='person:*', mode="sync")