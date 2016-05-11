# -*- coding: utf-8 -*-
import _utils as utils
import xbmc
import xbmcaddon
import xbmcvfs
import subtitleHtml2srt

subFile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')+'sub.srt').decode('utf-8')

#todo offset
def getSub(url,subtitleOffset):
	sub = False
	response = utils.getUrl(url)
	srt = subtitleHtml2srt.convert(response,subtitleOffset)
	writeSub(srt)
	return subFile
	
def writeSub(content):
	
	if xbmcvfs.exists(subFile):
		xbmcvfs.delete(subFile)
	f = xbmcvfs.File(subFile, 'w')
	f.write(content)
	f.close()