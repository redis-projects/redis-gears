#!/bin/bash

echo "Registering Redis Gears functions"
redis-cli -p 30001 -c RG.PYEXECUTE "`cat event_countmodified.py`" ID event_countmodified UPGRADE

redis-cli  -p 30001 -c RG.PYEXECUTE "`cat event_lastmodified.py` " ID event_lastmodified UPGRADE

redis-cli  -p 30001 -c RG.PYEXECUTE "`cat event_maxage.py`" ID event_maxage UPGRADE

redis-cli  -p 30001 -c RG.PYEXECUTE "`cat stream_maxage.py`" ID stream_maxage UPGRADE

read -n 1 -p "Press a key to continue." key
echo

echo "Loading data"
cat data.txt
cat data.txt | redis-cli -x  -p 30001 -c

read -n 1 -p "Press a key to continue." key
echo


echo "Batch processing"
echo redis-cli -p 30001 -c RG.PYEXECUTE \"\`cat batch_avg.py\`\"
redis-cli -p 30001 -c RG.PYEXECUTE "`cat batch_avg.py`"
echo "Running with UNBLOCKING option"
redis-cli -p 30001 -c RG.PYEXECUTE "`cat batch_avg.py`" UNBLOCKING