#!/usr/bin/env python
# coding: utf-8

import HTMLParser
import urllib
from os.path import basename
from os.path import splitext
from os.path import exists
import xml.dom.minidom as xml #Для парсинга xml файла с ссылкой на поток.
import sys
import subprocess as sps
import time

if not exists('/usr/bin/rtmpdump'):
	print "Установите rtmpdump!"
	raise SystemExit

class findXML(HTMLParser.HTMLParser):
	'''Парсер для страницы с видео. Читайте вики-документацию'''
	xml=None
	url=None
	title=str(time.time())
	title_found=False
	current_starttag={}
	div_closed=False
	def findVideoIn(self, url):
		self.url=url
		self.feed(urllib.urlopen(url).read())
	def handle_starttag(self, tag, attr):
		self.current_starttag=self.get_starttag_text()
		if self.get_starttag_text()=='<div class="lecture_title">':
			self.div_closed=False
	def handle_endtag(self, tag):
		if self.get_starttag_text()=='<div class="lecture_title">'and tag=='div':
			self.div_closed=True #Если тег div вложен. Иначе будем обрабатывать не те данные, которые нужны (еще и несколько раз).
	def handle_data(self, data):
		if data.find("show_video")!=-1: 
			print "Видео обнаружено.",
			#print data
			if data.find('&')!=-1:
				self.xml=self.url+basename(data[ data.find("'")+1 : data.rfind("&") ])
			elif data.find('?')!=-1:
				self.xml=self.url+basename(data[ data.find("'")+1 : data.rfind("?") ])
			else:
				self.xml=self.url+basename(data[ data.find("'")+1 : data.rfind("'") ])
		if self.get_starttag_text()=='<div class="lecture_title">' and self.div_closed==False: 
			if(self.title_found==False):
				print "Название лекции найдено:",
				self.title=data.decode('CP1251')
				while self.title.find('\n')!=-1: # На всякий случай
					i=self.title.find('\n')
					self.title=self.title[:i]+self.title[i+1:]
				self.title_found=True
				print self.title
			else:
				line, pos=self.getpos()
				#if len(data)>len(self.title):
				print "FIXME: Другое название было обнаружено в строке", line, "на позиции", pos, "длинной:", len(data)

	def getTitle(self):
		return self.title

def getChannel(text):
	if text.find("clip")!=-1:
		 return text[:text.rfind(".")]+'M'
	else:
		return text[:text.rfind(".")]+'L'

def downloadVideoFrom(url):	
	'''Загружает видео с переданного url'''
	p=findXML()
	p.findVideoIn(url)
	title=p.getTitle()
	p=xml.parseString(urllib.urlopen(p.xml).read())
	channel=getChannel(p.getElementsByTagName("resource")[0].getAttribute("source"))# Передалать в более универсальный случай
	print "Загрузка начата."
	try: sps.call(['rtmpdump', '-q', '-r', channel, '-o', title+'.flv'])
	except KeyboardInterrupt: print "Прервано пользователем."; raise SystemExit
	print "Вроде загрузилось."

if __name__=='__main__':
	try: downloadVideoFrom(sys.argv[1])
	except IndexError: 
		print "Не передана ссылка."; raise SystemExit
