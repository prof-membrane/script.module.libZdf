# -*- coding: utf-8 -*-
import time
import re
import HTMLParser
h = HTMLParser.HTMLParser()

def convert(content,offset = 0):
	srt = ''
	content = content.replace('  <','<')
	matchLine = re.compile('<p begin="(.+?)" end="(.+?)"(.+?)>(.+?)</p>', re.DOTALL).findall(content)
	i = 1
	for begin, end, info, line in matchLine:
		srt += str(i)+'\n'
		srt += _s2time(begin,offset) + ' --> ' + _s2time(end,offset) + '\n'
		line = line.replace('<span tts:color="','<font color="')
		line = line.replace('">','>')
		line = line.replace('</span>','</font>')
		if 'tts:color' in info:
			color = re.compile('tts:color="(.+?)"', re.DOTALL).findall(info)[0]
			srt += '<font color="'+color+'>'+line+'</font>'
		else:
			srt += line
		srt += '\n\n'
		i += 1
	srt = srt.decode('utf-8')
	srt = h.unescape(srt)
	srt = srt.encode('utf-8')
	return srt.replace('<br />','\n')
		


def _s2time(s,offset):
	offset = int(offset) * -1
	ms = s[-1] + '00'
	return time.strftime('%H:%M:%S', time.gmtime(int(s[:-2])+offset))+','+ms
