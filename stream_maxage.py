def logit(x):
  log(f"..streams: {x}")

gb = GearsBuilder('StreamReader')
gb.foreach(logit)
gb.register('_maxage_log', batch=1, duration=0, trimStream=False)
