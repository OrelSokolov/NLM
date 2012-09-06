#!/usr/bin/env python
# coding: utf-8

from vk.basics import docs
import cfg.main
from vk.basics import storage
import time

tmp_path=cfg.main.getTmpPath()
opened=False

# Переманная 1: отвечает за занятость базы


class DataBase(object):
	database_is_busy=False
	name='database.db'
	filename=None
	downloaded=False
	def __init__(self):
		self.getStatus()
	def setBusy(self):
		storage.Set(key=1, value='Busy')
	def setFree(self):
		storage.Set(key=1, value='Free')
	def getStatus(self):
		'''Проверяет, занята ли сейчас база другим пользователем.'''
		self.database_is_busy=True if storage.Get(key=1)=='Busy' else False
	def upload(self):
		'''Загружает файл базы данных, и делает соответствующие заметки в вики странице.'''
		docs.upload(self.filename)
		filename=None
		downloaded=False
		self.setFree()
	def download(self):
		'''Загружает самый новый файл базы для последующего открытия.'''
		while self.database_is_busy:
			print "База данных занята другим админом. Ждем..."
			time.sleep(120)
			self.getStatus()

		current=docs.findLast(self.name)
		print current
		self.setBusy()
		self.filename=docs.download(current[1], current[2])
		self.downloaded=True
	def lastNumber(self):
		lastLine=''
		for line in open(self.filename):
			if line[:1]!='#': lastLine=line
		lastNumber=lastLine[:lastLine.find('|')]
		return lastNumber
	def append(self, doc):
		'''Добавляет запись к базе данных.'''
		s='|' # Separator
		result_string=doc['number']+s+doc['docUrl']+s+doc['coverUrl']+s+doc['page']+'\n'
		if self.downloaded: db=open(self.filename, 'a'); db.write(result_string); db.close()


if __name__=='__main__':
	print docs.findLast('database.db')
	p=DataBase()
	p.download()
	print p.filename
	print p.lastNumber()


