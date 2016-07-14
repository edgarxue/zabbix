#!/usr/bin/env python
#coding=utf-8
import json
import urllib2

url = "http://service.zabbix.com/zabbix/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
user=""
passwd=""


def get_auth_key(user,passwd):
    data = json.dumps(
        {
           "jsonrpc": "2.0",
           "method": "user.login",
           "params": {
                     "user": user,
                     "password": passwd
                     },
           "id": 1
       })
    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key,header[key])
    try:
        result = urllib2.urlopen(request)
    except URLError as e:
        print "urlerror as: ", e.code
    else:
        response = json.loads(result.read())
        result.close()
    return response['result']

get_auth_key(user,passwd)
