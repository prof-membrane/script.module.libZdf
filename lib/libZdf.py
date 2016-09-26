# -*- coding: utf-8 -*-
import xbmc
import urllib
import xbmcaddon
import libMediathek
import mediathekxmlservice as xmlservice

addonID = 'plugin.video.zdf_de_lite'
translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString
showSubtitles = xbmcaddon.Addon().getSetting('subtitle') == 'true'
params = {}

baseUrl = 'http://www.zdf.de/ZDFmediathek'


def getNew():
	return xmlservice.getNew(baseUrl)
def getMostViewed(entries=50):
	return xmlservice.getXML('http://www.zdf.de/ZDFmediathek/xmlservice/web/meistGesehen?maxLength=50&id=%5FGLOBAL')
def getAZ(letter):
	list = xmlservice.getXML('http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd='+letter+'&detailLevel=2&characterRangeStart='+letter)
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
	return list
def getSearch(search_string,page=1):
	return xmlservice.getXML('http://www.zdf.de/ZDFmediathek/xmlservice/web/detailsSuche?maxLength=50&types=Video&properties=HD%2CUntertitel%2CRSS&searchString='+urllib.quote_plus(search_string))
	
def getXML(url,page=1,baseUrl='http://www.zdf.de/ZDFmediathek'):
	return xmlservice.getXML(url,page,baseUrl)
def getVideoUrl(url,useSub=False):
	print 'playing:'+url
	video,subUrl,offset = zdf_play.getVideoUrl(url)
	xbmc.log(xbmcaddon.Addon().getSetting('subtitle'))
	xbmc.log(str(showSubtitles))
	if showSubtitles and subUrl:
		xbmc.log('getting sub')
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

channels = {'3sat': '1209116',
'phoenix': '2256088',
'zdf': '1209114',
'zdfinfo': '1209120',
'zdfkultur': '1317640',
'zdfneo': '1209122'}

sport = [
	["Neuste Videos", "2686260"],
	["Badminton", "2686332"],
	["Basketball", "2686338"],
	["Beachvolleyball", "2686340"],
	["BMX", "2686308"],
	["Bogenschießen", "2686330"],
	["Boxen", "2686328"],
	["Fechten", "2686352"],
	["Freiwasser-Schwimmen", "2686298"],
	["Fußball", "2684700"],
	["Gewichtheben", "2686326"],
	["Golf", "2686434"],
	["Handball", "2686300"],
	["Hockey", "2686306"],
	["Judo", "2686324"],
	["Kanu", "2686322"],
	["Kanu-Slalom", "2686322"],
	["Leichtathletik", "2686292"],
	["Moderner Fünfkampf", "2686304"],
	["Mountainbike", "2686308"],
	["Radsport Bahn", "2686308"],
	["Radsport Straße", "2686308"],
	["Reiten", "2686342"],
	["Rhythmische Sportgymnastik", "2686314"],
	["Ringen", "2686294"],
	["Rudern", "2686344"],
	["Rugby", "2686448"],
	["Schießen", "2686320"],
	["Schwimmen", "2686298"],
	["Segeln", "2686318"],
	["Synchronschwimmen", "2774518"],
	["Taekwondo", "2686316"],
	["Tennis", "2686348"],
	["Tischtennis", "2686334"],
	["Trampolin", "2686314"],
	["Triathlon", "2686310"],
	["Turnen", "2686314"],
	["Volleyball", "2686350"],
	["Wasserball", "2686302"],
	["Wasserspringen", "2686312"],
]

def listMain():
	print ''
	
	libMediathek.addEntry({'name':translation(31030), 'mode':'xmlListPage', 'type': 'dir', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=%5FSTARTSEITE'})
	libMediathek.addEntry({'name':translation(31031), 'mode':'xmlListPage', 'type': 'dir', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/meistGesehen?maxLength=50&id=%5FGLOBAL'})
	libMediathek.addEntry({'name':translation(31032), 'mode':'listLetters',    'type': 'dir'})
	libMediathek.addEntry({'name':translation(31033), 'mode':'listDate',       'type': 'dir'})
	libMediathek.addEntry({'name':translation(31034), 'mode':'xmlListPage', 'type': 'dir', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/rubriken'})
	libMediathek.addEntry({'name':translation(31035), 'mode':'xmlListPage', 'type': 'dir', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/themen'})
	libMediathek.addEntry({'name':translation(31039), 'mode':'libZdfSearch',   'type': 'dir'})

def listSpecial():	
	for name,id in sport:
		thumb = 'http://www.zdf.de/ZDFmediathek/contentblob/'+id+'/timg946x532blob/'
		libMediathek.addEntry({'name':name, 'mode':'libZdfListPage', 'thumb':thumb, 'type': 'dir', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id='+id})
def listLetters():
	libMediathek.populateDirAZ('libZdfListLetter')
		
def libZdfListLetter():
	letter = params['name'].replace('#','0%2D9')
	libZdfListPage('http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd='+letter+'&detailLevel=2&characterRangeStart='+letter)

def listDate():
	libMediathek.populateDirDate('listDateChannels')
	
def listDateChannels(datum=False):
	if not datum:
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
	items = xmlservice.getXML(url)
	xbmc.log(str(items))
	#libMediathek.addEntries(items,int(page))
	libMediathek.addEntries(items)
	#for dict in items:
	#	libMediathek.addEntry(dict)
	#if nextPage:
	#	libMediathek.addEntry({'name':translation(31040),'url':url,'page':str(int(page)+1),'fanart':fanart,'mode':'libZdfListPage', 'type': 'dir'})
def xmlListPage():
	libMediathek.addEntries(xmlservice.getXML(params['url']))

def xmlPlay():
	videoUrl,subUrl,offset = xmlservice.getVideoUrl(params['url'])
	listitem = xbmcgui.ListItem(path=videoUrl)
	
	if True and subUrl:
		sub = xmlservice.getSubtitle(subUrl,offset)
		listitem.setSubtitles([sub])
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

### PVR context ###		
def libZdfPvrPlay(dict):
	url,sub = getVideoUrl(video['url'],showSubtitles)
	#url,sub = getVideoUrl(dict['url'],False)
	listitem = xbmcgui.ListItem(label=dict['name'],thumbnailImage=dict["thumb"],path=url)

	xbmc.Player().play(url, listitem)
"""
	r = 0.0
	video = False
	from difflib import SequenceMatcher
	d = date.today() - timedelta(int(day))
	ddmmyy = d.strftime('%d%m%y')
	for c,a,i in cannelList:
		c = c.lower().replace(" ","").replace(".","").replace("-","")
		if c == channel:
			id = i
	items = zdf_listing.getXML('http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungVerpasst?startdate='+ddmmyy+'&channelFilter='+id+'&enddate='+ddmmyy+'&maxLength=50')
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
"""
def libZdfPvrDate(datum,channel):
	day = date.today() - timedelta(int(datum))
	ddmmyy = day.strftime('%d%m%y')
	id = channels[channel]
	url = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungVerpasst?startdate='+ddmmyy+'&channelFilter='+id+'&enddate='+ddmmyy+'&maxLength=50'
	return getXML(url)
	
def libZdfPlay(p = False):
	#from player import myPlayer
	if not p:
		p = params
	url,sub = getVideoUrl(p['url'],showSubtitles)
	listitem = xbmcgui.ListItem(path=url)
	if sub:
		listitem.setSubtitles([sub])
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	

import time
import urllib2,re,random,xbmc,xbmcplugin,xbmcgui,xbmcaddon,cookielib,HTMLParser,datetime
import sys
from datetime import date, timedelta
try:
	pluginhandle = int(sys.argv[1])
except: pass
hideAudioDisa = True
helix = False
fanart = ''	

def list(p=False):	
	xbmc.log('list')
	global params
	if p:
		params = p
	else:
		params = libMediathek.get_params()
		
	#isCached = libMediathek.checkIfCachedVersionIsAvailable()
	xbmc.log('check')
	if False:# isCached:
		libMediathek.retrieveCached()
	elif not params.has_key('mode'):
		listMain()
	elif params['mode']=='xmlListPage':
		xmlListPage()
	elif params['mode']=='xmlPlay':
		xmlPlay()
	elif params['mode']=='listSpecial':
		listSpecial()
	elif params['mode']=='listDate':
		listDate()
	elif params['mode']=='listDateChannels':
		listDateChannels()
	elif params['mode']=='listLetters':
		listLetters()
	elif params['mode']=='libZdfListLetter':
		libZdfListLetter()
	elif params['mode']=='libZdfListPage':
		libZdfListPage()
	elif params['mode']=='libZdfSearch':
		libZdfSearch()
	elif params['mode']=='libZdfPlay':
		libZdfPlay()
	elif params['mode']=='libZdfAddMore':
		libZdfListPage()
	else:
		listMain()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	
	#if not 'mode' in params or params['mode'] != 'libZdfListPage':
	#	xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	#elif isCached:
	#	xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing = True, cacheToDisc = False)
		
