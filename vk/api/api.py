#!/usr/bin/env python
# coding: utf-8

import json
from urllib import urlencode
import urllib
import urllib2
import time
import subprocess as sps

	
app_path="~/.NerdLibraryManager/"

apocalypse_time="none"
token="none"
user_id="none"

def loadUserData():
	'''Загрузка из файла пользовательских данныx: пароля, логина..'''
	data=open(app_path+"vk/api/UserData.txt")
	email=data.readline()[:-1]
	password=data.readline()[:-1]
	data.close()
	return 	email, password

def auth(auth_type="GUI"):
	if auth_type=="GUI":
		print "Запущена графическая авторизация."
		sps.call(["python", app_path+"vk/api/browser.py"])
		init()#Не забываем обновить такие глобальные переменные как тукен, user_id, apocalypse_time, которые используются getToken() и др.
	elif auth_type=="term":
		print "Используем консольный вариант авторизации."
		import term_auth
		global token, user_id
		try:
			try: email, password = loadUserData()
			except: print "Проблема при загрузке данных из файла."
			try: token, user_id=term_auth.auth(email, password, "3029477", "docs,groups,video,wall,photos,messages,pages")
			except: print "Ошибка при вызове функции авторизации."
			auth=open(app_path+"vk/api/auth.txt", "w")
			#Делаем запись об авторизации#
			auth.write(token+"\n")
			auth.write(user_id+"\n")
			auth.write(str(time.time()+43200))#86400 - время жизни ключа. Для длительных лучше не использовать точное время во избежание проблем. 
			auth.close()
			init()
			print "Успешно авторизировались с консоли."
		except KeyboardInterrupt:
			print "Прервано пользователем."
		except: 
			print "Провал консольной авторизации."
			raise SystemExit(1)
	else:
		print "Передан неизвестный тип авторизации. Аварийный астонов."
		raise SystemExit(1)


def call(method, params):
	if time.time()>float(apocalypse_time):
		print "Тукен устарел, меняем на новый."
		auth(auth_type="term")	
		init() #Мы должны обновить тукен и user_id для функций token() и user_id()
	if isinstance(params, list):
		params_list = [kv for kv in params]
	elif isinstance(params, dict):
		params_list = params.items()
	else:
		params_list = [params]
	params_list.append(("access_token", token))
	url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params_list)) 
	try:
		return json.loads(urllib2.urlopen(url).read())["response"]
	except:
		return json.loads(urllib2.urlopen(url).read())

def getToken():
	global token
	return token

def getUserId(): 
	global user_id 
	return user_id

def init(): #Initialization
	try:
		auth_file=open(app_path+"vk/api/auth.txt")
		global token, user_id, apocalypse_time # Работаем именно с глобальными переменными
		token=auth_file.readline()[:-1]#Удаляем '\n' из тукена заодно
		if token=='': 
			print "Файл авторизации возможно пуст. Перезапуск..."
			raise ValueError
		user_id=auth_file.readline()[:-1]
		apocalypse_time=auth_file.readline()[:-1]
		auth_file.close()
		print "Данные авторизации успешно загружены из файла."
	except: auth(auth_type="term") #Если отсутсвует файл авторизации


init() #При импорте запустится раньше обращения к тукену и user_id, что предотвратит баги.
