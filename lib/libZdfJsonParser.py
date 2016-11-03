# -*- coding: utf-8 -*-
import xbmc
import json
import libMediathek2
#import dateutil.parser

base = 'https://api.zdf.de'
playerId = 'ngplayer_2_3'
log = xbmc.log
auth = '23a1db22b51b13162bd0b86b24e556c8c6b6272d reraeB'
getheader = {'Api-Auth': auth[::-1]}

def parsePage(url):
	response = libMediathek2.getUrl(url,getheader)
	j = json.loads(response)
	xbmc.log('profile')
	xbmc.log(j['profile'])
	if   j['profile'] == 'http://zdf.de/rels/search/result':
		return _parseSearch(j)
	elif j['profile'] == 'http://zdf.de/rels/search/result-page':
		return _parseSearchPage(j)
	elif j['profile'] == 'http://zdf.de/rels/content/page-index':
		return _parsePageIndex(j)
	elif j['profile'] == 'http://zdf.de/rels/content/page-index-teaser':
		return _parseTeaser(j)
	elif j['profile'] == 'http://zdf.de/rels/cmdm/resultpage-broadcasts':
		return _parseBroadcast(j)
	else:
		xbmc.log('Unknown profile: ' + j['profile'])
def getAZ():
	response = libMediathek2.getUrl("https://api.zdf.de/content/documents/sendungen-100.json?profile=default",getheader)
	j = json.loads(response)
	letters = {}
	l = []
	for brand in j['brand']:
		if 'title' in brand:
			#l = []
			if 'teaser' in brand:
				for teaser in brand['teaser']:
					xbmc.log(json.dumps(teaser))
					target = teaser['http://zdf.de/rels/target']
					d = _grepItem(target)
					l.append(d)
		try:
			xbmc.log(brand['title'])
		except:
			xbmc.log(str(brand))
	return l
	
def _parseSearch(j):
	l = []
	for module in j['module']:
		for result in module['filterRef']['resultsWithVideo']['http://zdf.de/rels/search/results']:
			target = result['http://zdf.de/rels/target']
			d = _grepItem(target)
			d['_views'] = str(result['viewCount'])
			l.append(d)
			#try: xbmc.log(str(len(json.dumps(module['filterRef']['resultsWithVideo']['http://zdf.de/rels/search/results']))))
			#except: pass
		#title = module['title']
		"""
		for teaser in module['teaser']:
			#d = {}
			#d['_name'] = teaser['teaserHeadline']
			#d['_plot'] = teaser['teasertext']
			#d['_thumb'] = _chooseImage(teaser['teaserImageRef'],True)
			target = teaser['http://zdf.de/rels/target']
			d = _grepItem(target)
			l.append(d)
		"""
	return l
			
def _parseSearchPage(j):
	l = []
	for result in j['http://zdf.de/rels/search/results']:
		target = result['http://zdf.de/rels/target']
		d = _grepItem(target)
		l.append(d)
	return l
	
def _parsePageIndex(j):
	l = []
	for result in j['module'][0]['filterRef']['resultsWithVideo']['http://zdf.de/rels/search/results']:
		target = result['http://zdf.de/rels/target']
		d = _grepItem(target)
		d['_views'] = str(result['viewCount'])
		l.append(d)
	return l
	
def _parseBroadcast(j):
	l = []
	for broadcast in j['http://zdf.de/rels/cmdm/broadcasts']:
		if 'http://zdf.de/rels/content/video-page-teaser' in broadcast:
			xbmc.log('#########')
			target = broadcast['http://zdf.de/rels/content/video-page-teaser']
			d = _grepItem(target)
			if d:
				#d['airedISO8601'] = broadcast['airtimeBegin']
				d['airedISO8601'] = broadcast['effectiveAirtimeBegin']
				d['type'] = 'date'
				l.append(d)
	return l
def _grepItem(target):
	if target['profile'] == 'http://zdf.de/rels/not-found':
		return False
	xbmc.log('###')
	xbmc.log(json.dumps(target))
	xbmc.log('contentType')
	xbmc.log(target['contentType'])
	d = {}
	d['_name'] = target['teaserHeadline']
	d['_plot'] = target['teasertext']
	d['_thumb'] = _chooseImage(target['teaserImageRef'])
	#d['url'] = base + target['http://zdf.de/rels/brand']['http://zdf.de/rels/target']['canonical']
	if target['contentType'] == 'brand' or target['contentType'] == 'category':
		#d['url'] = base + target['canonical']
		d['url'] = base + target['http://zdf.de/rels/search/page-video-counter-with-video']['self'].replace('&limit=0','&limit=100')
		d['_type'] = 'dir'
		d['mode'] = 'libZdfListPage'
	elif target['contentType'] == 'clip':
		d['url'] = base + target['mainVideoContent']['http://zdf.de/rels/target']['http://zdf.de/rels/streams/ptmd-template'].replace('{playerId}',playerId)
		if 'duration' in target['mainVideoContent']['http://zdf.de/rels/target']:
			d['_duration'] = str(target['mainVideoContent']['http://zdf.de/rels/target']['duration'])
		d['_type'] = 'clip'
		#d['_type'] = 'video'
		d['mode'] = 'libZdfPlay'
	elif target['contentType'] == 'episode':# or target['contentType'] == 'clip':
		if not target['hasVideo']:
			return False
		#if target['mainVideoContent']['http://zdf.de/rels/target']['showCaption']:
		#	d['suburl'] = base + target['mainVideoContent']['http://zdf.de/rels/target']['captionUrl']
		if 'mainVideoContent' in target:
			content = target['mainVideoContent']['http://zdf.de/rels/target']
		elif 'mainContent' in target:
			content = target['mainContent'][0]['videoContent'][0]['http://zdf.de/rels/target']
			
		d['url'] = base + content['http://zdf.de/rels/streams/ptmd-template'].replace('{playerId}',playerId)
		if 'duration' in content:
			d['_duration'] = str(content['duration'])
		d['_type'] = 'video'
		d['mode'] = 'libZdfPlay'
	else:
		xbmc.log('Unknown target type: ' + target['contentType'])
	return d
def _chooseImage(teaserImageRef,isVideo=False):
	if isVideo:
		return teaserImageRef['layouts']['384xauto']
	else:
		#return teaserImageRef['layouts']['1920x1080']
		try:
			return teaserImageRef['layouts']['384xauto']
		except:
			return ''
		
def getVideoUrl(url):
	d = {}
	d['media'] = []
	response = libMediathek2.getUrl(url,getheader)
	j = json.loads(response)
	for item in j['priorityList']:
		if item['formitaeten'][0]['type'] == 'h264_aac_ts_http_m3u8_http':
			for quality in item['formitaeten'][0]['qualities']:
				if quality['quality'] == 'auto':
					d['media'].append({'url':quality['audio']['tracks'][0]['uri'], 'type': 'video', 'stream':'HLS'})
	return d