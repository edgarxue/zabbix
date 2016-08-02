#!/usr/bin/env python
#coding=utf-8

"""
Collects stats from flume by JSON Reporting
##
We can start Flume with JSON Reporting support as follows:

bin/flume-ng agent --conf-file example.conf --name a1 -Dflume.monitoring.type=http -Dflume.monitoring.port=5432 
##
Use this script like:
    python flume.py [SINK|CHANNEL|SOURCE] NAME KEY
example:
    If you want to get CHANNEL.c1.ChannelFillPercentage,you can run:
    $> python flume.py CHANNEL c1 ChannelFillPercentage
   
"""

import json
import sys
import urllib2
from urllib2 import URLError

url = "http://localhost:5432/metrics"

def report():
    request = urllib2.Request(url)
    try:
        result = urllib2.urlopen(request)
    except URLError as e:
        print "Error as ", e
    else:
        response = json.loads(result.read())
        result.close()
        key = sys.argv[1]+"."+sys.argv[2]
        channel =  response[key]
        tag = channel[sys.argv[3]]
        return tag
print(report())
