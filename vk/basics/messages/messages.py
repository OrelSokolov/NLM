#!/usr/bin/python
# coding: utf-8

from vk import api
import json
import time
import subprocess as sps
import urllib2

user_id=api.getUserId()

count_msg=0

def send(uid, message):
	return api.call("messages.send", {'uid':uid, 'message':message})

		
def get(filters="1",count='40'): 
	return api.call("messages.get", {'filters':filters, 'count':count} )

def markAsRead(mids):
	return api.call("messages.markAsRead", {'mids':mids})

def toFile(message):
	f=open("current.sh", "w")
	message=unicode(message).encode('utf-8')
	f.write(message)
	f.close()

def runCode(message):
	global count_msg
	count_msg=count_msg+1
	#toFile(message) #Теперь нам не придется проверять существование файла.
	result=str(count_msg)+"|============================================\n" #Для сообщения, которое мы отправим
	log=open("log.txt", "w")
	#sps.call(['bash', 'current.sh'], stdout=log, stderr=log)
	sps.call(["python", "youtube-dl.py", "-q", "-t", message])
	if count_msg%2==0: #Набралось достаточно видео для аплоада
		send('40733432', "Набралось достаточно видео для аплоада. Сейчас попробуем загрузить.")
		sps.call(['bash', 'upload.sh'], stdout=log)
	log.close()
	log=open("log.txt")
	result=result+log.read()
	log.close()
	return result

def getById(mid):
	return api.call("messages.getById", {'mid':'mid'})

def lookForNewMessage():
	'''Ищет последнее сообщение в списке новых сообщений. Читает его. Отмечает как прочитанное. Испольняет. Остальные не трогает.'''
	response=get()
	if response!=[0]:
		print "Есть невыполненные задания."
		message=response[response[0]][u'body']
		mid=response[response[0]][u'mid']
		print "Отмечаем сообщение как прочитанное."
		markAsRead(mid)
		return message
	else: return None

def Sleep():
	try:
		sps.call (["python", "print.py"," "*90+"\r"])
		for x in xrange(80):
			sps.call (["python", "print.py", "  ["+" "*x+"===="+" "*(76-x)+"]\r"])
			time.sleep(0.01)
		sps.call (["python", "print.py"," "*90+"\r"])
		for x in xrange(80):
			sps.call (["python", "print.py", "  ["+" "*(76-x)+"===="+" "*x+"]\r"])
			time.sleep(0.01)
		sps.call (["python", "print.py","\r"+" "*90+"\r"])
	except KeyboardInterrupt:
		print "Прервано пользователем"
		raise SystemExit
	
	

def startDaemon():
	def answer(message): #На случай, если среди сообщений найдено непрочитанное с кодом.
		jresponse=send('40733432', runCode(message))#Ответ все еще в JSON
		response=str(jresponse)
		if response.find("error")!=-1: 
			try:
				print "-->",jresponse['error']['error_msg'],'<--'
			except KeyError: print "Возникла ошибка при отображении ошибки."
		else: print "Сообщение успешно послано..."
	while True:
		try:
			#print "Проверка новых сообщений...", 
			sps.call(["python", "print.py", "Проверка новых сообщений\r"])
			message=lookForNewMessage()
			sps.call (["python", "print.py","Список сообщений получен\r"])
			if message!=None: 
				sps.call (["python", "print.py","Выполняем задание.\r"])
				answer(message)
			Sleep()
		except KeyboardInterrupt: 
			print "\nПрервано пользователем."
			raise SystemExit
		except urllib2.URLError: 
			print "Ошибка сети. Продолжаем цикл через 10 секунд."
			time.sleep(10)
		except: 
			print "Неизвестная ошибка. Продолжаем цикл через 5 секунд."
			try:time.sleep(5)
			except KeyboardInterrupt: raise SystemExit

if __name__=='__main__':
	startDaemon()
