#!/usr/bin/python
# coding: utf-8

# НУЖНО ЕЩЕ ПРОПАТЧИТЬ ПУТИ!!!!!!!!!!!!!!!!!!!!!

from vk.api import api
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
import cfg.main
try: import requests #For uploading
except:
	print "Установите python-requests!"
	raise SystemExit


NerdID="38440718"


def upload_video(filename, name="", gid=NerdID, privacy_view=0, privacy_comment=0, description="", export_info=[]):
	'''Загружает видео в альбом группы, а также экспортирует необходимую информацию в export_info'''
	if name=="": name, ext=os.path.splitext(os.path.basename(filename))
	response=api.call("video.save", {'name':name, 'gid':gid, 'privacy_view':privacy_view, 'privacy_comment':privacy_comment, 'description=':description})
	export_info.append(str(response['vid']))
	export_info.append(str(gid))
	# Загрузка файла
	f = open (filename)
	return  requests.post(url=response['upload_url'], data ={'title':'test_file'},  files={'video_file':f} )
	

def rename(vid, oid, name="Default", desc="Загружено с помощью Nerd Library Manager."):
	#print "video",oid,vid
	return api.call("video.edit",{'vid':vid,'oid':oid,'name':name,'desc':desc})


if __name__=='__main__':
	print "Запущен скрипт videos.py"
	path=cfg.main.getAppPath() #Изменить!
	
	#---------Загрузка из папки!
	try:
		path=sys.argv[1]
		if path[-1:]!="/":
			path=path+"/"
	except IndexError:
		print "Не указана папка"
		raise SystemExit


	def isVideo(ext):
		'''Проверяет, является ли расширение файла допустимым.'''
		extensions=["mpeg", "MPEG", "avi", "AVI", "3gp", "3GP","mp4", "MP4", "mov", "MOV", "flv", "FLV", "wmv", "WMV"]
		for current in extensions:
			if ext==current: return True
		return False

	#upload_video("/home/oleg/t.mp4")
	#-------Делаем список файлов
	print "Делаем список файлов"
	videos=open(path+"videos.list", "w")
	sps.call(["ls *.*"], cwd=path, shell=True, stdout=videos)
	videos.close()
	del videos
	#-------Загружаем каждый, проверяя, относится ли он к видео.
	print "Загружаем файлы."
	counter=0#Счетчик для того, чтобы заменять имя файла, а потом загружать нужное.

	for current_video in open(path+"videos.list"):		
		name, extension = os.path.splitext(current_video)
		extension=extension[1:-1]#Удаляем ненужные символы
		if isVideo(extension):
			current_video=current_video[:-1]
			counter=counter+1
			temp_name=path+str(counter)+'.'+extension#Служит временной заменой для настоящего имени, которое не всегда успешно читается
			os.rename(path+current_video, temp_name)#Заменяем имя
			info=[]##Сделать не список, а словарь!!!
			try:#Пробуем загрузить файл под другим именем.
				if str(upload_video(temp_name, export_info=info)).find("size"): 
					print current_video, "успешно загружен под именем", os.path.basename(temp_name)
					#print info
					if str(rename(info[0], '-'+info[1], name=name))=='1':#Минус нужен для группы в Info[1]
						print "Файл бы переименован обратно в ", name
					else: print "Возникли проблемы с переименованием файла"
				else: print "Ошибка при загрузке", current_video
			except UnicodeDecodeError: print "Критическая ошибка при загрузке. Переименуйте", current_video
			except: print "Произошла критическая ошибка при загрузке. Перехожу к следующему файлу..."
			


