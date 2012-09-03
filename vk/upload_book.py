#!/usr/bin/python
# coding: utf-8

import json
import os
import os.path
import getpass
import sys
from urllib import urlencode
import urllib
import urllib2
import urlparse
import subprocess as sps
try: import requests #For uploading
except:
	print "Установите python-requests!"
	raise SystemExit


def nextFor(number):
	for x in xrange(10000):
		if str(hex(x-1))==number: return str(hex(x))
	return None

print nextFor('0x32')


#Загружаем базу данных
#Определяем номер следующего файла.
#Загружаем файл в вк.
#  Перемещаем файл в ~./NerdLibraryManger/tmp/
#  Изменяем его имя
#  Загружаем файл в вк
#  Получаем его Description
#Загружаем обложку в Вк.
#  Делаем обложку в папку ~/.NerdLibraryManager/tmp/
#  Загружаем обложку с нужным caption
#Создаем вики-страницу с нужными параметрами.
#Записываем в базу.
#Загружаем базу.
#Обновляем страницу с файлом.


