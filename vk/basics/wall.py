#!/usr/bin/python
# coding: utf-8

from vk import api
import json


NerdID="-38440718"

def post(message,owner_id=NerdID, attach=""):
	if attach=="":
		return api.call("wall.post",{'owner_id':owner_id, 'message':message, 'signed':'1', 'from_group':'1'})
	else:
		return api.call("wall.post",{'owner_id':owner_id, 'message':message, 'signed':'1', 'from_group':'1', 'attachments':str(attach)})



