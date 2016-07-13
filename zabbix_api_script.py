#!/usr/bin/env python
#coding=utf-8

import json
import time
import urllib2
from urllib2 import URLError

url = "http://zabbix.com/api_jsonrpc.php"
header = {"Content-Type":"application/json"}

#calculation time continued
def time_calculation(tag):

    now = int(time.time())
    try:
        tag = int(tag)
    except Exception as e:
        print "Error as :" ,e.code
    timeSustain = now - tag
    days = timeSustain // 86400
    days_remain = timeSustain % 86400
    hours = days_remain // 3600
    hours_remain = timeSustain % 3600
    minutes = hours_remain // 60
    seconds = timeSustain % 60
    if days == 0:
        if hours == 0:
            if minutes == 0:
                return '%s seconds' % (seconds)
            else:
                return '%s minute %s seconds' % (minutes,seconds)
        else:
            return '%s hours %s minutes %s second' % (hours,minutes,seconds)
    else:
        return '%s days %s hours %s minute %s second' % (days,hours,minutes,seconds)

# get tigger status
def get_tigger_status():
    data = json.dumps({
	        "jsonrpc": "2.0",
                "method": "trigger.get",
   	        "params": {
       	         	"output": [
       		        	 "triggerid",
      			         "description",
       			         "priority"
       			          ],
       	                "filter": {
       		         	 "value": 1
       			   },
                "expandData":"hostname",
       	        "sortfield": "priority",
                "maintenance":"false",
       	        "sortfield":"lastchange",
                "sortorder": "DESC"
   		      }, 
                "auth": "",
                "id": 1
	        	})

    request = urllib2.Request(url,data)
    for key in header:
        	   request.add_header(key,header[key])
    try:
       result = urllib2.urlopen(request)
    except URLError as e:
        	print "Error as ", e.code
    else:
        response = json.loads(result.read())
        result.close()
        issues =  response['result']
        content = ''
    
    if issues:
          for line in issues:
                        try:
                            timeStamp = int(line['lastchange'])
                        except Exception as e:
                            print "Error as ", e.code
                        timeArray = time.localtime(timeStamp)
                        commonStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
			content = content + "%s  %s Continued_time:%s\r\n" % (line['host'],line['description'],time_calculation(timeStamp))
          print content

get_tigger_status()
