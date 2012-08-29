#!/usr/bin/python
# coding: utf-8

from vk.api import api
import json
from urllib import urlopen
try: import requests #For uploading
except:
	print "Установите python-requests!"
	raise SystemExit


GID="-38508808"
app_path="/home/oleg/python/NerdLibraryManager/"

def upload(filename, gid=GID):
	'''Загружает документ в личные документы пользователя'''
	print "Загружаю ", filename
	if gid[0]=='-': gid=gid[1:]
	response=api.call("docs.getUploadServer", {'gid':gid})
	f = open (filename)
	full_url=response['upload_url']	

	#----------------------|Загрузка файла|---------------------
	r =  requests.post(url=full_url, data ={'title':'test_file'},  files={'file':f} )

#	print r.content
	try:
		fFile=json.loads(r.content) #field file
#		print fFile['file']
		return api.call("docs.save", {'file': fFile['file']})
		print "Вроде файл загрузился :)"
	except:
		print "Сервер выдал ошибку:", r.content

def getById(oid, did):
	'''Возвращает информацию о документе.'''
	return api.call("docs.getById", {'docs': str(oid)+'_'+str(did)})	

def download(oid, did):
	'''Загружает документ на локальную машину.'''
	doc=getById(oid, did)[0]
	ext=doc['ext'];	url=doc['url'];	title=doc['title']	
	fdoc=open(app_path+"tmp/"+title+'.'+ext, "wb"); fdoc.write(urlopen(url).read()); fdoc.close 

def get(gid=GID):
	'''Возвращает вложенный список'''
	if gid[0]=='-': gid=gid[1:]
	response=api.call("docs.get",{'oid':'-'+gid})
	docs=[]
#	print response
	for x in xrange(int(response[0])):
		docs.append([response[x+1][u'title'] , response[x+1][u'owner_id'], response[x+1][u'did']]) 
	
	return docs

def getAmount(gid=GID):
	'''Возврщащает количество документов'''
	if gid[0]=='-': gid=gid[1:]
	return int(api.call("docs.get", {'oid':'-'+gid})[0])
	

def getLast(gid=GID): 
	'''Возвращает последний загруженный документ'''
	return get()[0]


def find(name, exact=True):
	'''Ищет все документы с заданным именем и возвращает список'''
	result=[]
	if exact==True:
		for x in get():
			if x[0]==name: result.append(x)
	elif exact==False:
		for x in get():
			if x[0].find(name)!=-1: result.append(x)		
	else: 
		raise TypeError
	return result


if __name__=='__main__':
	download(getLast()[1], getLast()[2])

