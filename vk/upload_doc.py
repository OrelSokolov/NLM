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

#Определяем номер файла.
#Загружаем файл в вк.
#Загружаем обложку в Вк.
#Создаем вики-страницу с нужными параметрами.
#Записываем в базу.
#Загружаем базу.
#Обновляем страницу с файлом.
