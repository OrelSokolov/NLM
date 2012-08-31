#!/usr/bin/env python
# coding: utf-8

from os.path import exists

if not exists('main.cfg'):
	print "Отсутствует файл конфигурации."
	raise SystemExit
main=open('main.cfg')
app_path=main.readline()[:-1]
app_cnf=main.readline()[:-1]
main.close()

def getAppPath():
	return app_path	

def getCnfPath():
	return app_cnf

print getAppPath()
print getCnfPath()
