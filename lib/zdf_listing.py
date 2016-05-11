#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import xbmcplugin
import xbmcgui
import xbmc
import urllib
import _utils as utils
import fanart


baseUrl = "http://www.zdf.de"
fallbackImage = "http://www.zdf.de/ZDFmediathek/img/fallback/946x532.jpg"
defaultThumb = ''

def getXML(url,page=1):
	page = int(page)
	if page > 1:
		url += '&offset='+str((page-1)*50)
	print url
	#t = []
	list = []
	response = utils.getUrl(url)
	#r = requests.get(url)
	#response = r.text.decode('utf-8')
	nextPage = False
	if '<additionalTeaser>' in response:
		nextPage=re.compile('<additionalTeaser>(.+?)</additionalTeaser>', re.DOTALL).findall(response)[0] == 'true'
	elif '<batch>' in response:
		batch=re.compile('<batch>(.+?)</batch>', re.DOTALL).findall(response)[0]
		if int(batch) > page * 50:
			nextPage = True
	#xbmc.log(response)
		
	if not '<teasers>' in response:
		return list,False
	teasers=re.compile('<teasers>(.+?)</teasers>', re.DOTALL).findall(response)[0]
	match_teaser=re.compile('<teaser(.+?)</teaser>', re.DOTALL).findall(teasers)
	for teaser in match_teaser:
		dict = {}
		#match_member=re.compile('member="(.+?)"', re.DOTALL).findall(teaser)
		type = re.compile('<type>(.+?)</type>', re.DOTALL).findall(teaser)[0]
		dict['thumb'] = chooseThumb(re.compile('<teaserimages>(.+?)</teaserimages>', re.DOTALL).findall(teaser)[0])
		dict.update(getInfo(re.compile('<information>(.+?)</information>', re.DOTALL).findall(teaser)[0]))
		dict.update(getDetails(re.compile('<details>(.+?)</details>', re.DOTALL).findall(teaser)[0]))
		#title = cleanTitle(title)
		if type == 'sendung' and dict['duration'] != '0':
			dict['url'] = baseUrl+'/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=' + dict['assetId']
			dict['fanart'] = dict['thumb']
			dict['mode'] ='libZdfListPage'
			dict['type'] = 'dir'
			list.append(dict)
		elif type == 'video':
			dict['plot'] += '\n\n'+dict['airtime'].split(' ')[0]+' | '+toMin(dict['duration'])+' | '+dict['channel']
			dict['url'] = baseUrl+'/ZDFmediathek/xmlservice/web/beitragsDetails?id=' + dict['assetId']
			dict['mode'] = 'libZdfPlay'
			dict['type'] = 'video'
			f = fanart.getFanart(dict['originChannelId'])
			if f:
				dict['fanart'] = f
			list.append(dict)
		elif type == 'rubrik' or type == 'thema':
			dict['url'] = baseUrl+'/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=' + dict['assetId']
			dict['mode'] ='libZdfListPage'
			dict['type'] = 'dir'
			list.append(dict)
		else:
			xbmc.log('libZdf: unsupported item type "' + type + '"')
	return list,nextPage
			
			
		

def getInfo(infos):
	dict = {}
	dict['name']=re.compile('<title>(.+?)</title>', re.DOTALL).findall(infos)[0]
	try:
		dict['plot']=re.compile('<detail>(.+?)</detail>', re.DOTALL).findall(infos)[0]
	except: pass
		
	return dict
	
def chooseThumb(images,maxW=476):
	thumb = fallbackImage
	height = 0
	width = 0
	match_images=re.compile('<teaserimage.+?key="(.+?)x(.+?)">(.+?)</teaserimage>', re.DOTALL).findall(images)
	for w,h,image in match_images:
		if not "fallback" in image:
			if int(h) > height or int(w) > width:
				if int(w) <= maxW:
					height = int(h)
					width = int(w)
					thumb = image
	#print str(width)+'x'+str(height)
	return thumb

def getDetails(details):
	dict = {}
	try:
		dict['assetId']=re.compile('<assetId>(.+?)</assetId>', re.DOTALL).findall(details)[0]
	except: pass
	try:
		dict['originChannelId']=re.compile('<originChannelId>(.+?)</originChannelId>', re.DOTALL).findall(details)[0]
	except: pass
	try:
		dict['channel']=re.compile('<channel>(.+?)</channel>', re.DOTALL).findall(details)[0]
	except: pass
	try:
		dict['channelLogo']=re.compile('<channelLogoSmall>(.+?)</channelLogoSmall>', re.DOTALL).findall(details)[0]
	except: pass
	try:
		dict['airtime']=re.compile('<airtime>(.+?)</airtime>', re.DOTALL).findall(details)[0]
	except: pass
	try:
		dict['timetolive']=re.compile('<timetolive>(.+?)</timetolive>', re.DOTALL).findall(details)[0]
	except: pass
	try:
		dict['fsk']=re.compile('<fsk>(.+?)</fsk>', re.DOTALL).findall(details)[0]
	except: pass
	try:
		dict['hasCaption']=re.compile('<hasCaption>(.+?)</hasCaption>', re.DOTALL).findall(details)[0]
	except: pass
	try:
		dict['url']=re.compile('<vcmsUrl>(.+?)</vcmsUrl>', re.DOTALL).findall(details)[0]
	except: pass
		
	try:
		if '<lengthSec>' in details:
			dict['duration'] = int(re.compile('<lengthSec>(.+?)</lengthSec>', re.DOTALL).findall(details)[0])
		else:
			length=re.compile('<length>(.+?)</length>', re.DOTALL).findall(details)[0]
			if ' min ' in length:
				l = length.split(' min ')
				length = int(l[0]) * 60 + int(l[1])
			elif ' min' in length:
				l = length.replace(' min','')
				length = int(l) * 60
			elif '.000' in length:#get seconds
				length = length.replace('.000','')
				l = length.split(':')
				length = int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])
			dict['duration'] = length
	except: pass
	
	return dict
	
def toMin(s):
	m, s= divmod(int(s), 60)
	M = str(m)
	S = str(s)
	if len(M) == 1:
		M = '0'+M
	if len(S) == 0:
		S = '00'
	elif len(S) == 1:
		S = '0'+S
	return M+':'+S+' Min.'