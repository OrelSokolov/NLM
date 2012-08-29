from vk.basics import docs

opened=False

def upload():
	'''Загружает файл базы данных, и делает соответствующие заметки в вики странице.'''
	pass		

def download():
	'''Загружает самый новый файл базы для последующего открытия.'''
	pass

def append(doc):
	'''Добавляет запись к базе данных.'''
	if opened==True:
		s='|' # Separator
		result_string=doc['title']+s+doc['id']+s+doc['cover']+s+doc['page']+s+doc['descr']+s+doc['section']+s
	else:
		print "Нечего редактировать!"


