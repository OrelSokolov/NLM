#!/usr/bin/env python
# coding: utf-8

import subprocess as sps
import os.path as path
import sys
#--------------------------------------------------------------------------------------------------
#- Попытаемся импортировать библиотеку для резки PDF.
#--------------------------------------------------------------------------------------------------
try:
	from pyPdf import PdfFileWriter, PdfFileReader
except: 
	print "Установите pyPDF."
	raise SystemExit

#Проверяем на установленный программы.
if not path.exists("/usr/bin/ddjvu"):
	print "Установите ddjvu"
	raise SystemExit		
elif not path.exists("/usr/bin/convert"):
	print "Установите convert"
	raise SystemExit
elif not path.exists("/usr/bin/pdf2djvu"):
	print "Установите pdf2djvu"
	raise SystemExit

def extractPagePDF(filename, page):
	'''Извлевает из PDF файла страницу и записывает ее в файл'''
	page=int(page)
	output = PdfFileWriter()
	input1 = PdfFileReader(file(filename, "rb"))
	#--------------------------------------------------------------------------------------------------
	# добавляем в output страницу №1 из inpu1, без изменений
	#--------------------------------------------------------------------------------------------------
	output.addPage(input1.getPage(page))
	#--------------------------------------------------------------------------------------------------
	# Наконец, записываем "output" в файл "Результат.pdf"
	#--------------------------------------------------------------------------------------------------
	outputStream = file(str(page)+"desc-"+filename, "wb")
	output.write(outputStream)
	outputStream.close()


def pagePDF(filename, page):
	'''Записывает первую страницу из PDF файла в Jpeg файл'''
	try:
		extractPagePDF(filename, page) # Получаем PDF файл с одной страницей
	except:
		print "Ошибка, при вырезании страницы из файла", filename
		raise SystemExit
	#--------------------------------------------------------------------------------------------------
	#- Конвертируем файл с одной страницей в djvu с одной страницей.
	#--------------------------------------------------------------------------------------------------
	filename=str(page)+"desc-"+filename
	name, ext = path.splitext(filename)
	outName=name+".djvu"
	sps.call(['pdf2djvu', '-o',outName, filename], stderr=open('/dev/null'))
	sps.call(['rm', filename]) #имя файла уже изменено, так что исходный не удалится, а удалится мусор
	#--------------------------------------------------------------------------------------------------
	#- Есть файл DJVU с одной страницей. Теперь сконвертируем его в JPG
	#--------------------------------------------------------------------------------------------------
	inputName=outName
	#print inputName
	name, ext=path.splitext(inputName)
	outName=name+".png"
	#print outName
	sps.call(['convert', inputName, '-resize','x3000', outName], )
	sps.call(['rm', inputName]) # чистим каталог от мусора
	#--------------------------------------------------------------------------------------------------
	#- Теперь можно наслаждаться результатом. Получен нужный файл.
	#--------------------------------------------------------------------------------------------------
	return outName

def pageDJVU(filename, page):
	'''Записывает страницу под номером page из DJVU файла в JPG файл.'''
	outName, ext = path.splitext(filename)
	#--------------------------------------------------------------------------------------------------
	#- Попробуем извлечь страницу из файла.
	#--------------------------------------------------------------------------------------------------
	try: sps.call(['ddjvu', '-format=tiff', '-page', str(page+1), filename, str(page)+"desc-"+outName+".tiff"])
	except: print "Возникли проблемы с извлечением страницы из файла."
	#--------------------------------------------------------------------------------------------------
	#- Теперь сконвертируем страницу в png.
	#--------------------------------------------------------------------------------------------------
	try: sps.call(['convert',str(page)+"desc-"+outName+".tiff", '-resize', 'x3000', str(page)+"desc-"+outName+".png"])
	except: print "Возникли проблемы с конвертированием в PNG."

	sps.call(['rm', str(page)+"desc-"+outName+".tiff"])
	return  str(page)+"desc-"+outName+".png"


def extractPage(filename, page):
	name, ext = path.splitext(filename)
	print "Page", page, "from", filename
	if(ext==".djvu"):
		return pageDJVU(filename, page)
	elif (ext==".pdf"):
		return pagePDF(filename, page)
	else:
		return None

if __name__== '__main__' :
	try: extractPage(sys.argv[1], sys.argv[2])
	except IndexError: 
		print "Неверный список аргументов."
		raise SystemExit
