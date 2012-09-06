#!/usr/bin/env python
# coding: utf-8

import subprocess as sps
import os.path as path
import sys
import time
#--------------------------------------------------------------------------------------------------
#- Попытаемся импортировать библиотеку для резки PDF.
#--------------------------------------------------------------------------------------------------
try:
	import pyPdf.utils
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
	folder=path.dirname(filename)+'/'
	filename=path.basename(filename)
	print folder+filename
	page=int(page)
	output = PdfFileWriter()
	input1 = PdfFileReader(file(folder+filename, "rb"))
	#--------------------------------------------------------------------------------------------------
	# добавляем в output страницу №1 из inpu1, без изменений
	#--------------------------------------------------------------------------------------------------
	output.addPage(input1.getPage(page))
	#--------------------------------------------------------------------------------------------------
	# Наконец, записываем "output" в файл "Результат.pdf"
	#--------------------------------------------------------------------------------------------------
	outputStream = file(folder+str(page)+"cover-"+filename, "wb")
	output.write(outputStream)
	outputStream.close()

def fixPdf(pdfFile):
    try:
        fileOpen = file(pdfFile, "ab")
        fileOpen.write("%%EOF")
        fileOpen.close()
        return "Fixed"
    except Exception, e:
        return "Unable to open file: %s with error: %s" % (pdfFile, str(e))

def pagePDF(filename, page):
	'''Записывает первую страницу из PDF файла в Jpeg файл'''
	try:
		extractPagePDF(filename, page) # Получаем PDF файл с одной страницей
	except pyPdf.utils.PdfReadError:
		fixPdf(filename)
		extractPagePDF(filename, page) # Получаем PDF файл с одной страницей
	except:
		raise SystemExit
	#--------------------------------------------------------------------------------------------------
	#- Конвертируем файл с одной страницей в djvu с одной страницей.
	#--------------------------------------------------------------------------------------------------
	folder=path.dirname(filename)+'/'
	filename=path.basename(filename)

	filename=folder+str(page)+"cover-"+filename
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
	return outName

def pageDJVU(filename, page):
	'''Записывает страницу под номером page из DJVU файла в JPG файл.'''
	folder=path.dirname(filename)+'/'
	filename=path.basename(filename)
	
	outName, ext = path.splitext(filename)
	#--------------------------------------------------------------------------------------------------
	#- Попробуем извлечь страницу из файла.
	#--------------------------------------------------------------------------------------------------
	try: sps.call(['ddjvu', '-format=tiff', '-page', str(page+1), folder+filename, folder+"cover-"+outName+".tiff"])
	except: print "Возникли проблемы с извлечением страницы из файла."
	#--------------------------------------------------------------------------------------------------
	#- Теперь сконвертируем страницу в png.
	#--------------------------------------------------------------------------------------------------
	try: sps.call(['convert', folder+"cover-"+outName+".tiff", '-resize', 'x400', folder+"cover-"+outName+".png"])
	except: print "Возникли проблемы с конвертированием в PNG."

	sps.call(['rm', folder+"cover-"+outName+".tiff"])
	return  folder+"cover-"+outName+".png"


def make(filename):
	page=0
	name, ext = path.splitext(filename)
	print "Page", page, "from", filename
	if(ext==".djvu"):
		return pageDJVU(filename, page)
	elif (ext==".pdf"):
		return pagePDF(filename, page)
	else:
		return None

if __name__== '__main__' :
	try: print make(sys.argv[1])
	except IndexError: 
		print "Неверный список аргументов."
		raise SystemExit
