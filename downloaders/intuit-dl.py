#!/usr/bin/env python
# coding: utf-8

import HTMLParser
import urllib
from os.path import basename
from os.path import splitext
import xml.dom.minidom as xml #Для парсинга xml файла с ссылкой на поток.
import sys
import subprocess as sps

class findXML(HTMLParser.HTMLParser):
	'''Парсер для страницы с видео.'''
	xml=None
	url=None
	def findVideoIn(self, url):
		self.url=url
		self.feed(urllib.urlopen(url).read())
	def handle_data(self, data):
		if data.find("show_video")!=-1: 
			print "The video has been detected."
			#print data
			if data.find('&')!=-1:
				self.xml=self.url+basename(data[ data.find("'")+1 : data.rfind("&") ])
			elif data.find('?')!=-1:
				self.xml=self.url+basename(data[ data.find("'")+1 : data.rfind("?") ])
			else:
				self.xml=self.url+basename(data[ data.find("'")+1 : data.rfind("'") ])
			

def getChannel(text):
	if text.find("clip")!=-1:
		 return text[:text.rfind(".")]+'M'
	else:
		return text[:text.rfind(".")]+'L'



if __name__=='__main__':
	p=findXML()
	try:	p.findVideoIn(sys.argv[1])
	except IndexError:
		print "Не передана ссылка."
		raise SystemExit
	p=xml.parseString(urllib.urlopen(p.xml).read())
	channel=getChannel(p.getElementsByTagName("resource")[0].getAttribute("source"))# Передалать в более универсальный случай
	sps.call(['rtmpdump', '-q', '-r', channel, '-o', 'video.flv'])
