# Preparation

see https://github.com/RedisGears/gears-cli
```
pip install gears-cli

# make sure to have Gears 1.2+
docker pull redislabs/redismod:latest

# Note we switch to port 30001 to keep same port as for below cluster setup
docker run -p 30001:6379 redislabs/redismod:latest
```

Or for a 3 masters distributed cluster:
```
docker run -p 30001:30001 -p 30002:30002 -p 30003:30003 redislabs/rgcluster:latest

# updated IP for laptop to access it and follow slots from "redis-cli -c"
./cluster.sh
redis-cli -p 30001 CONFIG SET cluster-announce-ip 127.0.0.1
redis-cli -p 30002 CONFIG SET cluster-announce-ip 127.0.0.1
redis-cli -p 30003 CONFIG SET cluster-announce-ip 127.0.0.1
```

# Scenario

- We will create sample data `person:...` HASH with `age: ...`
- then have `_count_modified_` and `_last_modified_` automatically added upon write (hset EVENT)
- and SET `_maxage` added as real-time max counter
- and the change log of maxage XADD to STREAM `_maxage_log`

- there is also an example cluster-distributed Gears BATCH compute of `avg()` age using aggregate accumulator

The entire scenario can be played in one go using this script instead of running 1 by 1 commands.
```
./setup.sh
```

# RediSearch

Create index
```
FT.CREATE person_idx on HASH PREFIX 1
person:
SCHEMA
name TEXT
gender TAG
age NUMERIC SORTABLE
```

Sample search and aggregate
```
FT.SEARCH person_idx "Smith"
FT.SEARCH person_idx "Smit*"
FT.SEARCH person_idx "-Smit*"

FT.SEARCH person_idx "@age:[50 +inf]" SORTBY age DESC

FT.AGGREGATE person_idx "*" GROUPBY 1 @gender REDUCE AVG 1 @age as maxage
```


# Known issues
- When using cluster, the ./setup.sh script fails with the ID argument
- Cannot use redisgears-py, have not found proper way to load it into server side gears which seems to be a requirement (that would then simplify setup.sh using python) [app_* file]
- pip virtualenv not documented
- not sure why gears cluster has an IP announced on the docker internal IP vs 127.0.0.1 hence the script cluster.sh as a workaround


# Docs

Cluster
https://stackoverflow.com/questions/63191884/redis-gears-events-in-cluster

Reference
https://oss.redis.com/redisgears/

Events
https://redis.io/docs/manual/keyspace-notifications/

Python client
https://github.com/RedisGears/redisgears-py
https://pypi.org/project/gearsclient/
https://stackoverflow.com/questions/51201515/pipenv-requires-an-egg-fragment-for-version-controlled-dependencies-warning-w


# Sample data

see https://oss.redis.com/redisgears/intro.html
```
cat data.txt | redis-cli -x

or

SET foo bar
HSET person:1 name "Rick Sanchez" age 70
HSET person:2 name "Morty Smith" age 14
HSET person:3 name "Summer Smith" age 17
HSET person:4 name "Beth Smith" age 35
HSET person:5 name "Shrimply Pibbles" age 87
```



# Batch processing

```
cat batch_avg.py| redis-cli -x -p 30001 -c RG.PYEXECUTE

gears-cli run --port 30001 batch_avg.py
```


