from gearsclient import GearsRemoteBuilder as GRB
from gearsclient import execute, atomic
import redis
from time import sleep

conn = redis.Redis(host='localhost', port=6379)

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

gb = GRB(r=conn)
gb.map(lambda x: int(x['value']['age']))
gb.accumulate(prepare_avg)
gb.map(compute_avg)
res = gb.run('person:*')

print(res)