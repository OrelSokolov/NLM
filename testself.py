#!/usr/bin/env python
# coding: utf-8

print "Запущена системы базового самотестирования."

def mod(name): print "Есть проблемы в модуле", name

try: import cfg.main
except: mod('cfg.main')

try: import vk.api.api
except: mod('vk.api.api')

try: import vk.basics.docs
except: mod('vk.basics.docs')
