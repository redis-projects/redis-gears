def my_hsetCount(r):
  execute('hincrby', r[1], '_count_modified_', 1)
  return call_next(*r[1:])

GB('CommandReader').map(my_hsetCount).register(hook='hset', keyprefix='person', mode='sync')
