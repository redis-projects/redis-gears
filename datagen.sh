#!/bin/bash

#content="lorem.sentence(10)" \

docker run jruaux/riot-gen -h host.docker.internal -p 30001 import \
uid="#index" \
created="date.birthday" \
blob="lorem.characters(128)" \
name="name.firstName.concat(' ').concat(name.lastName)" \
age="number.numberBetween(0,110)" \
gender="bool.bool() ? 'M' : 'F'" \
country="country.name" \
--end=5000 --threads=1 \
hset --keyspace gen --keys uid \

