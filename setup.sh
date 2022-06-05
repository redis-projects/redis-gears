#!/bin/bash

GEARS=`cat event_countmodified.py`
redis-cli -p 30001 -c RG.PYEXECUTE "$GEARS" ID event_countmodified UPGRADE

GEARS=`cat event_lastmodified.py`
redis-cli  -p 30001 -c RG.PYEXECUTE "$GEARS" ID event_lastmodified UPGRADE

GEARS=`cat event_maxage.py`
redis-cli  -p 30001 -c RG.PYEXECUTE "$GEARS" ID event_maxage UPGRADE

GEARS=`cat stream_maxage.py`
redis-cli  -p 30001 -c RG.PYEXECUTE "$GEARS" ID stream_maxage UPGRADE

echo "Loading data"
cat data.txt | redis-cli -x  -p 30001 -c

echo "Batch processing"
cat batch_avg.py | redis-cli -x -p 30001 -c RG.PYEXECUTE
