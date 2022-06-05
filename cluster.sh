#!/bin/bash

redis-cli -p 30001 CONFIG SET cluster-announce-ip 127.0.0.1
redis-cli -p 30002 CONFIG SET cluster-announce-ip 127.0.0.1
redis-cli -p 30003 CONFIG SET cluster-announce-ip 127.0.0.1
