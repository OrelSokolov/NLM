#!/usr/bin/python
# coding: utf-8

from vk.api import api
import json
from urllib import urlopen
import cfg.main
try: import requests #For uploading
except:
	print "Установите python-requests!"
	raise SystemExit


GID="-38508808"
app_path=cfg.main.getAppPath()
cfg_path=cfg.main.getCfgPath()
tmp_path=cfg.main.getTmpPath()

def upload(filename, gid=GID):
	'''Загружает документ в личные документы пользователя'''
	print "Загружаю ", filename
	if filename.find(tmp_path)==-1: filename=tmp_path+filename
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
		rs=api.call("docs.save", {'file': fFile['file']})
		print "Вроде файл загрузился :)"
		return 'http://vk.com/doc'+str(rs[0][u'owner_id'])+'_'+str(rs[0][u'did'])
	except:
		print "Сервер выдал ошибку:", r.content

def getById(oid, did, gid=GID):
	'''Возвращает информацию о документе.'''
	if gid[0]=='-': gid=gid[1:]
	response=api.call("docs.get",{'oid':'-'+gid})
	docs=[]
	for x in xrange(int(response[0])):
		if response[x+1][u'owner_id']==oid and response[x+1][u'did']==did: return response[x+1]
	return []

def download(oid, did):
	'''Загружает документ на локальную машину.'''
	doc=getById(oid, did)
	#print 'doc', doc
	if doc!=[]: 
		ext=doc['ext'];	url=doc['url'];	title=doc['title']	
		print 'Скачивается документ', title
		try:	
			filename=tmp_path+title+'.'+ext if ext!='db' else tmp_path+title
			fdoc=open(filename, "wb"); fdoc.write(urlopen(url).read()); fdoc.close 
			print 'Скачан'
			return filename
		except: print 'Возникла ошибка при скачивании документа.'
	else: print 'Ошибка при запросе документа.' 




def get(gid=GID):
	'''Возвращает вложенный список'''
	if gid[0]=='-': gid=gid[1:]
	response=api.call("docs.get",{'oid':'-'+gid})
	docs=[]
	try:
		for x in xrange(int(response[0])):
			docs.append([response[x+1][u'title'] , response[x+1][u'owner_id'], response[x+1][u'did']]) 
	except: print "Сервер выдал ошибку", response
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

def findLast(name):
	result=find(name, exact=True)
	if result==[]: return []
	else: return result[0]

if __name__=='__main__':
	download(getLast()[1], getLast()[2])
