#!/usr/bin/env python
# coding: utf-8

import subprocess as sps
from local import docpages
from os.path import exists
import sys

ISBNline=0 #На случай ошибки распознования в русской версии

def extractFrom(filename):
	'''Находит и извлекает страницу с описанием в файле. Поиск проводится среди 5 первых страниц.'''
	if exists(filename):
		desc=None
		for page in xrange(5):
			desc=pageDescr(docpages.extractPage(filename, page))
			if desc!=None: break
		if desc==None: desc='None'
		return desc
	else:
		print "Файл не существует!"
		raise SystemExit
	
def ISBN(pagefile):
	'''Ищет ISBN в заданной странице. А там и описание недалеко'''
	sps.call(['tesseract',pagefile, 'en'+pagefile,'-l', 'eng'])			
	ISBN=None
	i=0#For debug
	global ISBNline #На случай, если потом не сможем найти ISBN
	for line in open('en'+pagefile+'.txt'):
		i=i+1
		if line.find('ISBN')!=-1:
			print 'Найден ISBN в строке',i
			ISBNline=i 
			ISBN=line[5:-1]
			break
	sps.call(['rm', 'en'+pagefile+'.txt']) # Для чистоты
	#print 'ISBN', ISBN
	return ISBN

def pageDescr(pagefile):
	isbn=ISBN(pagefile)
	if isbn==None:
		sps.call(['rm', pagefile]) # Для чистоты
		return None
	else:
		sps.call(['tesseract',pagefile, 'rus'+pagefile,'-l', 'rus'])
		result=''
		after_ISBN=False
		i=0
		lastline=None
		for line in open('rus'+pagefile+'.txt'):
			if after_ISBN:
				i=i+1
				result=result+line
				if line=='\n' and i>2 and lastline=='\n': break
				lastline=line
			if line.find(isbn)!=-1 and after_ISBN==False: after_ISBN=True; print "Опознали ISBN. Граббим описание."
		if result=='': #Так как isbn был найден, но возможно при OCR произошла ошибка.
			i=0
			for line in open('rus'+pagefile+'.txt'):
				i=i+1
				if after_ISBN:
					result=result+line
					if line=='\n' and i>2 and lastline=='\n': break
					lastline=line
				if i==ISBNline: after_ISBN=True; print "Граббим описание, основываясь на английской версии."
			
			
		sps.call(['rm', 'rus'+pagefile+'.txt']) # Для чистоты
		sps.call(['rm', pagefile]) # Для чистоты
		return result		

if __name__=='__main__':
	try: print extractFrom(sys.argv[1])
	except IndexError: print "Не передан файл."; raise SystemExit
