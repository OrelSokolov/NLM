#!/usr/bin/python
# coding: utf-8

try: from vk.api import api
except:
	print "Установите переменную PYTHONPATH в файле .bashrc командой export"
	raise SystemExit
import json
try: import requests #For uploading
except:
	print "Установите python-requests!"
	raise SystemExit


GID="38508808"
album1_500="159194272"
album501_1000="161364785"

def upload(filename, aid=album1_500, gid=GID, caption="Загружено с помощью Nerd Library Manager."):
	'''Загружает фото в альбом группы'''
	if gid[0]=='-': gid=gid[1:]
	response=api.call("photos.getUploadServer", {'aid':aid,'gid':gid} )
	f = open (filename)
	full_url=response['upload_url']	
	aid=response['upload_url']
	#----------------------|Загрузка файла|---------------------
	r =  requests.post(url=full_url, data ={'title':'test_file'},  files={'file1':f} )

#	print r.content
	photo=json.loads(r.content) #field file
	photo['caption']=caption
	return api.call("photos.save", photo )

def get():
	pass

def getStep(gid=GID, offset="0", step='10'):
	'''Служит для получения промежуточного списка документов. Запрашивает \'step\' штук.'''
	if gid[0]!='-': gid='-'+gid	
	result=[]
	response= api.call("photos.getAll", {'owner_id': gid, 'count':step, 'offset':offset})[1:]
	for x in response:
		result.append([ x[u'text'], x[u'owner_id'], x[u'pid'] ])
	return result


def getAll(gid=GID):
	'''Получает все фотографии группы, запрашивая по 50 штук за итерацию.'''
	allBooks=[]
	step=90
	amount=getAmount() #Для уменьшения обращений к api
	for x in xrange(amount/step+1):
		#print float(x)/float((amount/step+1))*100, "Выполено"
		for y in getStep(offset=str(step*x), step=step): #Специально для случаев, когда видео меньше 10 в списке.
			allBooks.append(y)
	return allBooks
	
	

def getAmount(gid=GID):
	'''Возвращает количество фотографий в группе в целом или в альбоме.'''
	if gid[0]=='-': gid=gid[1:]
	return int(api.call("photos.getAll", {'owner_id':'-'+gid, 'count': '1'})[0])
	

def find(name, exact=True):
	'''Ищет фотографии по описанию во ВСЕХ фото. Возращает список найденных фотографий.'''
	result=[]
	if exact==True:
		for x in getAll():
			if x[0]==name: result.append(x)
	elif exact==False:
		for x in getAll():
			if x[0].find(name)!='-1': result.append(x)
	else: 
		print "Неверное значение для exact"
		raise SystemExit
	return result


if __name__=='__main__':
	print find('32')
