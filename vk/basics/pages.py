#!/usr/bin/env python
# coding: utf-8

from vk.api import api
import json


GID="38508808"


class Page:
	pass

def save(title='untitled', gid=GID, text="This is page"):
	pid=api.call("pages.save", {'gid': gid, 'Text': text, 'title':title})
	api.call("pages.save", {'gid': gid, 'Text': text, 'pid':pid})
	api.call("pages.saveAccess", {'pid':pid, 'gid': gid, 'view':'2' , 'edit': '0'})
	return  'http://vk.com/page-'+gid+'_'+str(pid)


def get():
	return api.call("pages.getTitles", {'gid': GID})


if __name__=='__main__':
	print save('Страница')

