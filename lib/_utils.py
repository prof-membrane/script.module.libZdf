import urllib
import urllib2
import socket
import xbmc
import xbmcaddon
import xbmcvfs
import re
from StringIO import StringIO
import gzip

auth = '23a1db22b51b13162bd0b86b24e556c8c6b6272d reraeB'
def getUrl(url):
	xbmc.log("get url: "+url)
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/25.0')
	req.add_header('Api-Auth', auth[::-1])
	req.add_header('Accept-Encoding','gzip, deflate')
	response = urllib2.urlopen(req)
	link = response.read()
	compressed = response.info().get('Content-Encoding') == 'gzip'
	response.close()
	
	if compressed:
		buf = StringIO(link)
		f = gzip.GzipFile(fileobj=buf)
		link = f.read()
	return link
	
def f_open(path):
	f = xbmcvfs.File(path)
	result = f.read()
	f.close()
	return result

def f_write(path,data):
	print 'writing to '+path
	f = xbmcvfs.File(path, 'w')
	result = f.write(data)
	f.close()
	return True
	