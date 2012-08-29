#!/usr/bin/python
# coding: utf-8

from vk import api
import json


NerdID="38440718"

def post(owner_id,message,token, attach=""):
	if attach=="":
		return api.call("wall.post",{'owner_id':owner_id, 'message':message, 'signed':'1', 'from_group':'1'}, token)
	else:
		return api.call("wall.post",{'owner_id':owner_id, 'message':message, 'signed':'1', 'from_group':'1', 'attachments':str(attach)}, token)



