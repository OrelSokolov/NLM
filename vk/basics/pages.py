#!/usr/bin/env python
# coding: utf-8

from vk.api import api
import json


GID="38508808"


class Page:
	pass

def create(title='untitled', gid=GID, text="empty"):
	return api.call("pages.save", {'gid': '-'+gid, 'Text': text, 'title':title})


def get():
	return api.call("pages.get", {})


if __name__=='__main__':
	print get()
