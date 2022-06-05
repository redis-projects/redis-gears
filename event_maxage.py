def maxage(x):
  age = execute('GET', '_maxage')
  if (age is None or x > int(age)):
      log("..maxage update")
      execute('SET', '_maxage', x)
      execute('XADD', '_maxage_log', '*', 'age', x)

def logit(x):
  log(f"..gears: {x}")

gb = GearsBuilder('KeysReader')
gb.foreach(logit)
gb.map(lambda x: int(x['value']['age']))
gb.foreach(maxage)
gb.register('person:*', event=['hset'], keyTypes=['hash'], mode='async')
