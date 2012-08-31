#!/usr/bin/env python
# coding: utf-8

from gi.repository import Gtk, WebKit
import os, sys, urllib 
from urlparse import urlparse, parse_qs
import time
import cfg.main

app_path=cfg.main.getAppPath()
cfg_path=cfg.main.getCfgPath()
UI_FILE=app_path+"vk/api/browser.ui"

class Browser:
	def __init__(self):
		self.builder=Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.url=self.builder.get_object("url")

		self.webview = WebKit.WebView()
		scrolled_window=self.builder.get_object("scrolledwindow")
		scrolled_window.add(self.webview)

		self.webview.connect("title-changed", self.on_title_changed)
		self.webview.connect("load-finished", self.on_load_finished)

		self.window=self.builder.get_object("window")

		self.window.show_all()
		url="http://oauth.vk.com/authorize?"

		params= { 'client_id':'3029477',
		 'scope':'docs,groups,wall,photos,video,messages,pages',
		 'redirect_uri':'http://oauth.vk.com/blank.html',
		 'display':'page',
		 'response_type': 'token'
		}
		url=url+urllib.urlencode(params)

		self.webview.load_uri(url)
		self.url.set_text("Ну что, поехали!")

	def on_entry_activate(self, widget):
		pass

	def on_title_changed(self, webview, frame, title):
		self.window.set_title(title)

	def on_load_finished(self, webview, frame):
		current_uri=frame.get_uri()
		self.url.set_text(current_uri)
		r=urlparse(current_uri)
		if "/blank.html" in r.path :
			data=parse_qs(r.fragment) #Извлекаем access_token
			fdata=open(cfg_path+"auth.txt", "w")
			try:fdata.write(data['access_token'][0]+"\n")
			except KeyError:#Нет тукена. Это бывает при нажатии на кнопку отмены. 
				print "И зачем вы это сделали?"
				raise SystemExit(1)
			fdata.write(data['user_id'][0]+"\n")
			fdata.write(str(time.time()+int(data['expires_in'][0])/2)+"\n")# Время, когда нужно сменить ключ
			fdata.close()
			print "Успешно авторизировались!"
			print '''
Создали файл с данными авторизации вида:
	access_token
	user_id
	apocalypse_time'''
			Gtk.main_quit()


	def destroy(self, window):
		Gtk.main_quit()


def main():
	app=Browser()
	Gtk.main()

if __name__=="__main__":
	main()


