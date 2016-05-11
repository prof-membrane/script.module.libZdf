# -*- coding: utf-8 -*-
import zdf_listing
import zdf_play
import libZdfSubtitle
import urllib
import xbmc
import xbmcaddon
import libMediathek

addonID = 'plugin.video.zdf_de_lite'
translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString

params = {}


def getNew(entries=50):
	return zdf_listing.getXML('http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=%5FSTARTSEITE')
def getMostViewed(entries=50):
	return zdf_listing.getXML('http://www.zdf.de/ZDFmediathek/xmlservice/web/meistGesehen?maxLength=50&id=%5FGLOBAL')
def getAZ(letter):
	list,nextPage = zdf_listing.getXML('http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd='+letter+'&detailLevel=2&characterRangeStart='+letter)
	if letter.lower() == "d":
		l = []
		for dict in list:
			name = dict["name"].lower()
			if name.startswith("der ") or name.startswith("die ") or name.startswith("das "):
				if name[4] == 'd':
					l.append(dict)
			else:
				l.append(dict)
		list = l
	return list,nextPage
def getSearch(search_string,page=1):
	return zdf_listing.getXML('http://www.zdf.de/ZDFmediathek/xmlservice/web/detailsSuche?maxLength=50&types=Video&properties=HD%2CUntertitel%2CRSS&searchString='+urllib.quote_plus(search_string))
	
def getXML(url,page=1):
	return zdf_listing.getXML(url,page)
def getVideoUrl(url,useSub=False):
	print 'playing:'+url
	video,subUrl,offset = zdf_play.getVideoUrl(url)
	if useSub and subUrl:
		return video,libZdfSubtitle.getSub(subUrl,offset)
	else:
		return video,False



		
weekdayDict = { '0': translation(31013),#Sonntag
				'1': translation(31014),#Montag
				'2': translation(31015),#Dienstag
				'3': translation(31016),#Mittwoch
				'4': translation(31017),#Donnerstag
				'5': translation(31018),#Freitag
				'6': translation(31019),#Samstag
			  }

cannelList = [['3sat',                  'ZDF',  '1209116'],
			  ['Phoenix',               'ZDF',  '2256088'],
			  ['ZDF',                   'ZDF',  '1209114'],
			  ['ZDFinfo',               'ZDF',  '1209120'],
			  ['ZDF.kultur',            'ZDF',  '1317640'],
			  ['ZDFneo',                'ZDF',  '1209122']]

def listMain():
	libMediathek.addEntry({'name':translation(31030), 'mode':'libZdfListPage', 'type': 'dir', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=%5FSTARTSEITE'})
	libMediathek.addEntry({'name':translation(31031), 'mode':'libZdfListPage', 'type': 'dir', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/meistGesehen?maxLength=50&id=%5FGLOBAL'})
	libMediathek.addEntry({'name':translation(31032), 'mode':'listLetters',    'type': 'dir'})
	libMediathek.addEntry({'name':translation(31033), 'mode':'listDate',       'type': 'dir'})
	libMediathek.addEntry({'name':translation(31034), 'mode':'libZdfListPage', 'type': 'dir', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/rubriken'})
	libMediathek.addEntry({'name':translation(31035), 'mode':'libZdfListPage', 'type': 'dir', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/themen'})
	libMediathek.addEntry({'name':translation(31039), 'mode':'libZdfSearch',   'type': 'dir'})
	
def listLetters():
	dict = {}
	dict['name'] = "0-9"
	dict['url'] = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd=0%2D9&detailLevel=2&characterRangeStart=0%2D9'
	dict['mode'] = 'libZdfListPage'
	dict['type'] = 'dir'
	libMediathek.addEntry(dict)
	letters = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
	for letter in letters:
		letter = letter.upper()
		dict['name'] = letter
		dict['url'] = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd='+letter+'&detailLevel=2&characterRangeStart='+letter
		libMediathek.addEntry(dict)

def listDate():
	dict = {}
	dict['mode'] = 'listDateChannels'
	dict['type'] = 'dir'
	dict['name'] = translation(31020)
	dict['datum']  = '0'
	libMediathek.addEntry(dict)
	dict['name'] = translation(31021)
	dict['datum']  = '1'
	libMediathek.addEntry(dict)
	i = 2
	while i <= 6:
		day = date.today() - timedelta(i)
		dict['name'] = weekdayDict[day.strftime("%w")]
		dict['datum']  = str(i)
		libMediathek.addEntry(dict)
		i += 1

def listDateChannels(datum=False):
	if not datum:#TODO: share global params gracefully
		datum = params['datum']
	dict = {}
	day = date.today() - timedelta(int(datum))
	ddmmyy = day.strftime('%d%m%y')
	for channel,source,id in cannelList:
		if source == 'ZDF':
			dict['mode'] = 'libZdfListPage'
			dict['name'] = channel
			dict['type'] = 'dir'
			dict['url']  = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungVerpasst?startdate='+ddmmyy+'&channelFilter='+id+'&enddate='+ddmmyy+'&maxLength=50'
			libMediathek.addEntry(dict)
	
def libZdfSearch():
	keyboard = xbmc.Keyboard('', translation(31039))
	keyboard.doModal()
	if keyboard.isConfirmed() and keyboard.getText():
		search_string =  urllib.quote_plus(keyboard.getText())
		libZdfListPage("http://www.zdf.de/ZDFmediathek/xmlservice/web/detailsSuche?maxLength=50&types=Video&properties=HD%2CUntertitel%2CRSS&searchString="+search_string)
	
def libZdfListPage(url=False,type=''):
	if not url:
		url = params['url']
	page = params.get('page','1')
	items,nextPage = getXML(url,page)	
	for dict in items:
		libMediathek.addEntry(dict)
	if nextPage:
		libMediathek.addEntry({'name':translation(31040),'url':url,'page':str(int(page)+1),'fanart':fanart,'mode':'libZdfListPage', 'type': 'dir'})


### PVR context ###		
def libZdfPvrPlay(time=0,day=0,name='ZDF heute Sendung',channel='ZDF'):
	r = 0.0
	video = False
	from difflib import SequenceMatcher
	d = date.today() - timedelta(int(day))
	ddmmyy = d.strftime('%d%m%y')
	for c,a,i in cannelList:
		c = c.lower().replace(" ","").replace(".","").replace("-","")
		if c == channel:
			id = i
	items,nextPage = zdf_listing.getXML('http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungVerpasst?startdate='+ddmmyy+'&channelFilter='+id+'&enddate='+ddmmyy+'&maxLength=50')
	n = 0
	foundAccurateTime = False
	for item in items:
		HH,MM = item["airtime"].split(" ")[-1].split(":")
		videoTime = int(HH) * 60 + int(MM)
		
		if time == videoTime:
			video = item
			#xbmc.log("matching string ratio: " + str(SequenceMatcher(None, name, item["name"]).ratio()))
			foundAccurateTime = True
		elif not foundAccurateTime and libMediathek.pvrCheckStartTimeIsComparable(time,videoTime) and libMediathek.pvrCheckNameIsComparable(name,item["name"]):
			video = item
				
	if video == False:
		xbmc.executebuiltin("Notification(Kein Video gefunden,Nicht in Mediathek, 7000)")
		xbmc.log("no video found")
		return
	showSubtitles = False
	url,sub = getVideoUrl(video['url'],showSubtitles)
	listitem = xbmcgui.ListItem(label=video['name'],thumbnailImage=video["thumb"],path=url)

	xbmc.Player().play(url, listitem)
	

def libZdfPlay(p = False):
	if not p:
		p = params
	url,sub = getVideoUrl(p['url'],showSubtitles)
	listitem = xbmcgui.ListItem(path=url)
	if showSubtitles and helix and sub:
		listitem.setSubtitles(sub)
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	

import time
import urllib2,re,random,xbmc,xbmcplugin,xbmcgui,xbmcaddon,cookielib,HTMLParser,datetime
import sys
from datetime import date, timedelta
try:
	pluginhandle = int(sys.argv[1])
except: pass
hideAudioDisa = True
showSubtitles = False
helix = False
fanart = ''	

def list(p=False):	
	global params
	if p:
		params = p
	else:
		params = get_params()
	for key,val in params.items():
		try:
			params[key] = urllib.unquote_plus(val)
		except: 
			print 'Cant unquote this: '+ str(val)
	
	if not params.has_key('mode'):
		listMain()
	elif params['mode']=='listDate':
		listDate()
	elif params['mode']=='listDateChannels':
		listDateChannels()
	elif params['mode']=='listLetters':
		listLetters()
	elif params['mode']=='libZdfListPage':
		libZdfListPage()
	elif params['mode']=='libZdfSearch':
		libZdfSearch()
	elif params['mode']=='libZdfPlay':
		libZdfPlay()
	else:
		listMain()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	
		

def get_params():
	param={}
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
								
	return param