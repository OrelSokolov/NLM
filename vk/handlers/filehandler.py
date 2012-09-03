#!/usr/bin/env python
# coding: utf-8

import sys
from local import cover
from local import description
from os.path import exists
from os.path import basename
from os.path import splitext
from vk.handlers import dbhandler 
from vk.handlers import wikihandler
import subprocess as sps
import cfg.main
from vk.basics import photos
from vk.basics import pages 
from vk.basics import docs

def nextFor(number):
	number=str(number)
	for x in xrange(1,10000):
		if str(hex(x-1))==number: return str(hex(x))
	return None

tmp_path=cfg.main.getTmpPath()

if __name__=='__main__':
	print "Поехали!"
	try: filename=sys.argv[1]
	except IndexError: 
		print "не передан аргумент"
		raise SystemExit
	if not exists(filename):
		print "Нет такого файла."
		raise SystemExit
	def photoListToAddr(arg):
		return 'photo'+str(arg[0])+'_'+str(arg[1])

#Выдираем описание, или оставляем поле empty.
	print 'Делаем описание'
	desc=description.makeDescr(filename)
#Выдираем название книжки
	'Делаем название книжки'
	title=basename(filename)
#Загружаем базу данных.
	print 'Скачиваем базу данных'
	db=dbhandler.DataBase()
	db.download()
#Определяем номер документа.
	print 'Определяем номер документа:',
	currentNumber=nextFor(db.lastNumber())
	print currentNumber
#Делаем обложку для файла
	print 'Делаем обложку для файла'
	coverfile=cover.make(filename)
	print coverfile
#Переименовываем документ.
	print 'Переименовываем документ'
	docname=str(currentNumber)
	docFilename=tmp_path+docname
	sps.call(['mv', filename, docFilename])
#Загружаем документ и сохраняем адрес.
	print 'Загружаем документ'
	docUrl=docs.upload(docFilename)
#Загружаем обложку и сохраняем адрес.
	print 'Загружаем обложку'
	covUrl=photoListToAddr(photos.upload(coverfile, caption=currentNumber))
#Собираем текст wiki-страницы.
	print 'Собираем вики-страницу'
	wikitext=wikihandler.buildPage(covUrl[5:], docUrl, title, '_', desc[:2000])	
	print '----------------------------------------------------------'
	print wikitext
	print '----------------------------------------------------------'
#Публикуем вики-страницу
	print 'Делаем вики-страницу'
	wikiUrl=pages.save(str(currentNumber), text=wikitext)	
#Создаем словарь, олицетворяющий документ.
	doc={}
	doc['number']=currentNumber; doc['page']=wikiUrl; doc['docUrl']=docUrl; doc['coverUrl']= covUrl
#Делаем соответствующие записи в базе данных.
	print 'Делаем запись в базе данных'
	db.append(doc)
#Выгружаем базу-данных.
	print 'Выгружаем базу данных.'
	db.upload()
#Делаем пост.
