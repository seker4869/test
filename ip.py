#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import urllib
import json
import sys,os,re
import socket
import pprint
reload(sys)
sys.setdefaultencoding( "utf-8" )
if len(sys.argv) <=1:
	print "Please"
	sys.exit(0)
def handler(signum,frame):
	sys.exit(0)
signal.signal(signal.SIGINT,handler)
url = "http://ip.taobao.com/service/getIpInfo.php?ip="
def ip_location(ip):
	data = urllib.urlopen(url + ip).read()
#	pprint.pprint(data)
	datadict = json.loads(data)
	for oneinfo in datadict:
		#if "code" == oneinfo:
		if oneinfo == "code":
			if datadict[oneinfo] == 0:
				return datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"] + datadict["data"]["isp"]
re_ipaddress = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
re_domain = re.compile(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?')
if os.path.isfile(sys.argv[1]):
	file_path = sys.argv[1]
	fh = open(file_path,'r')
	for line in fh.readlines():
		line = line.encode('utf-8')
		#print line
		if re_ipaddress.match(line):
			city_address = ip_location(line)
			city_address = city_address.encode('utf-8')
			print line.strip() + ":" + city_address
else:
	ip_address = sys.argv[1]
	if re_ipaddress.match(ip_address):
		city_address = ip_location(ip_address)
		city_address = city_address.encode('utf-8')
		ip_address = ip_address.encode('utf-8')
		print ip_address + ":" + city_address
	elif(re_domain.match(ip_address)):
		result = socket.getaddrinfo(ip_address,None)
		last = ""
		for i in range(len(result)):
		#print "hehe"
		#result = result.encode('utf-8')
			ip_address = result[i][4][0]
			ip_address = ip_address.encode('utf-8')
			if last == ip_address:
				pass
			else:
				last = ip_address
				city_address = ip_location(ip_address)
				city_address = city_address.encode('utf-8')
				print ip_address.strip() + ":" + city_address
