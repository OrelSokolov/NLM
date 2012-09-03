#!/usr/bin/env python
# coding: utf-8

from vk.api import api

def Set(key='0', value='None',glob='1'): #glob=global
	key=str(key)
	return api.call("storage.set", {'key':key, 'global':glob, 'value':value})

def Get(key='0', glob='1'):
	return api.call("storage.get", {'key':key, 'global':glob})
	

if __name__=='__main__':
	print Set(key=1, value='Работает')
	print Get(key=1)
