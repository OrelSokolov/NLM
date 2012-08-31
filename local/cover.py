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

if not path.exists("/usr/bin/ddjvu"):
	print "Установите ddjvu"
	raise SystemExit		
elif not path.exists("/usr/bin/convert"):
	print "Установите convert"
	raise SystemExit
elif not path.exists("/usr/bin/pdf2djvu"):
	print "Установите pdf2djvu"
	raise SystemExit

def extractPagePDF(filename):
	'''Извлевает из PDF файла первую страницу и записывает ее в файл'''

	output = PdfFileWriter()
	input1 = PdfFileReader(file(filename, "rb"))
	#--------------------------------------------------------------------------------------------------
	# добавляем в output страницу №1 из inpu1, без изменений
	#--------------------------------------------------------------------------------------------------
	output.addPage(input1.getPage(0))
	#--------------------------------------------------------------------------------------------------
	# Наконец, записываем "output" в файл "Результат.pdf"
	#--------------------------------------------------------------------------------------------------
	outputStream = file("cover-"+filename, "wb")
	output.write(outputStream)
	outputStream.close()


def coverPDF(filename):
	'''Записывает первую страницу из PDF файла в Jpeg файл'''
	try:
		extractPagePDF(filename) # Получаем PDF файл с одной страницей
	except:
		print "Ошибка, при вырезании страницы из файла", filename
		raise SystemExit
	#--------------------------------------------------------------------------------------------------
	#- Конвертируем файл с одной страницей в djvu с одной страницей.
	#--------------------------------------------------------------------------------------------------
	filename="cover-"+filename
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


def coverDJVU(filename):
	'''Записывает первую страницу из DJVU файла в JPG файл.'''
	outName, ext = path.splitext(filename)
	#--------------------------------------------------------------------------------------------------
	#- Попробуем извлечь обложку из файла.
	#--------------------------------------------------------------------------------------------------
	try: sps.call(['ddjvu', '-format=tiff', '-page', '0', filename, "cover-"+outName+".tiff"])
	except: print "Возникли проблемы с извлечением обложки из файла."
	#--------------------------------------------------------------------------------------------------
	#- Теперь сконвертируем обложку в png.
	#--------------------------------------------------------------------------------------------------
	try: sps.call(['convert', "cover-"+outName+".tiff", '-resize', 'x400', "cover-"+outName+".png"])
	except: print "Возникли проблемы с конвертированием в PNG."

	sps.call(['rm', "cover-"+outName+".tiff"])


def cover(filename):
	name, ext = path.splitext(filename)
	print "Делаем обложку для",filename
	if(ext==".djvu"):
		coverDJVU(filename)
	elif (ext==".pdf"):
		coverPDF(filename)
	else:
		pass

if __name__== '__main__' :
	try: cover(sys.argv[1])
	except IndexError:
		print("Не передано имя файла для создания обложки.")

