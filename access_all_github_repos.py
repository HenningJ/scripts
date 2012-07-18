# This is a quick python script I threw together to apply some action through 
# the GitHub API to all repos of a user.
# Here it's setting an IRC service hook, but that can be easily changed 
# by adjusting the repoUrlSuffix and jsonData variables
# 
# Use at your own peril. :-)

import requests
from requests.auth import HTTPBasicAuth
import json

# adjust username and password for API calls that need authentication
auth = HTTPBasicAuth('username','password')

# suffix defining which exact API of the repos you want to access
repoUrlSuffix = '/hooks'
# data you want to send to each repo API
jsonData = json.dumps({"name":"irc","config":{"nick": "GitHub","server":"irc.freenode.net","password":"","room":"#quicksilver","port":"6667"},"events":["push","issues","pull_request"],"active":True})

page=1
pageSize=100
resultNum=pageSize;

while resultNum >= pageSize:
	r = requests.get('https://api.github.com/users/quicksilver/repos?page='+ repr(page) +'&per_page='+ repr(pageSize), auth=auth)
	resultNum = len(r.json)
	
	print
	print 'Processing '+ repr(resultNum) +' repos...'
	print
	
	for eachRepo in r.json:
		print eachRepo["name"] + ' (URL: '+ eachRepo["url"] +')'
		
		# might need to adjust the requests.method for some of the API actions (eg. delete). 
		# "requests" supports the following HTTP Verbs: GET, OPTIONS, HEAD, POST, PUT, PATCH and DELETE
		p = requests.post(url=eachRepo["url"] + repoUrlSuffix, data=jsonData, auth=auth)
		print
		if p.status_code >= 300:
			print 'Error:'
			print p.headers['status']
			print p.text
		else:
			print 'Success'
	
	page += 1
