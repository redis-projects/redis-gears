from time import sleep


def prepare_avg(a, x):
  ''' Accumulates sum and count of records '''
  a = a if a else (0, 0)  # accumulator is a tuple of sum and count
  a = (a[0] + x, a[1] + 1)
  log(f".....{a[0]} from {hashtag()}")
  #sleep(1)
  return a

def compute_avg(x):
  ''' Returns the average '''
  # average is quotient of sum and count
  return x[0]/x[1]

gb = GearsBuilder()
gb.map(lambda x: int(x['value']['age']))
#gb.accumulate(prepare_avg)
#gb.map(compute_avg)
gb.foreach(lambda x: log(f"....{x} from {hashtag()}"))
gb.avg()
gb.run('person:*')

## Expected result: [42.0]