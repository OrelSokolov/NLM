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


def extractPagePDF(filename, page):
	'''Извлевает из PDF файла первую страницу и записывает ее в файл'''

	output = PdfFileWriter()
	input1 = PdfFileReader(file(filename, "rb"))
	#--------------------------------------------------------------------------------------------------
	# добавляем в output страницу №1 из inpu1, без изменений
	#--------------------------------------------------------------------------------------------------
	output.addPage(input1.getPage(page))
	#--------------------------------------------------------------------------------------------------
	# Наконец, записываем "output" в файл "Результат.pdf"
	#--------------------------------------------------------------------------------------------------
	outputStream = file("desc-"+filename, "wb")
	output.write(outputStream)
	outputStream.close()


def coverPDF(filename):
	'''Записывает первую страницу из PDF файла в Jpeg файл'''
	try:
		extractPagePDF(filename) # Получаем PDF файл с одной страницей
	except:
		print "Ошибка, при вырезании страницы из файла", filename
	#--------------------------------------------------------------------------------------------------
	#- Конвертируем файл с одной страницей в djvu с одной страницей.
	#--------------------------------------------------------------------------------------------------
	filename="desc-"+filename
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
	sps.call(['convert', inputName, '-resize','x400', outName], )
	sps.call(['rm', inputName]) # чистим каталог от мусора
	#--------------------------------------------------------------------------------------------------
	#- Теперь можно наслаждаться результатом. Получен нужный файл.
	#--------------------------------------------------------------------------------------------------


def coverDJVU(filename, page):
	'''Записывает первую страницу из DJVU файла в JPG файл.'''
	outName, ext = path.splitext(filename)
	#--------------------------------------------------------------------------------------------------
	#- Попробуем извлечь обложку из файла.
	#--------------------------------------------------------------------------------------------------
	try: sps.call(['ddjvu', '-format=tiff', '-page', str(page), filename, "desc-"+outName+".tiff"])
	except: print "Возникли проблемы с извлечением обложки из файла."
	#--------------------------------------------------------------------------------------------------
	#- Теперь сконвертируем обложку в png.
	#--------------------------------------------------------------------------------------------------
	try: sps.call(['convert', "desc-"+outName+".tiff", '-resize', 'x400', "desc-"+outName+".png"])
	except: print "Возникли проблемы с конвертированием в PNG."

	sps.call(['rm', "desc-"+outName+".tiff"])


def cover(filename, page):
	name, ext = path.splitext(filename)
	print filename
	if(ext==".djvu"):
		coverDJVU(filename, page)
	elif (ext==".pdf"):
		coverPDF(filename, page)
	else:
		pass

if __name__== '__main__' :
	if not path.exists("/usr/bin/ddjvu"):
		print "Установите ddjvu"
		raise SystemExit		
	elif not path.exists("/usr/bin/convert"):
		print "Установите convert"
		raise SystemExit
	elif not path.exists("/usr/bin/pdf2djvu"):
		print "Установите pdf2djvu"
		raise SystemExit
	else:
		try:
			cover(sys.argv[1], sys.argv[2])
		except IndexError:
			print("Не передано имя файла для создания обложки.")

