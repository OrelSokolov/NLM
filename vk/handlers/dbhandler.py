from vk.basics import docs
import cfg.main

tmp_path=cfg.main.getTmpPath()
opened=False


def upload(filename):
	'''Загружает файл базы данных, и делает соответствующие заметки в вики странице.'''
	pass		

def download(name):
	'''Загружает самый новый файл базы для последующего открытия.'''
	filename=None # Чтобы потом возвратить имя файла как результатат
	return filename

def append(filename, doc):
	'''Добавляет запись к базе данных.'''
	if opened==True:
		s='|' # Separator
		result_string=doc['title']+s+doc['id']+s+doc['cover']+s+doc['page']+s+doc['descr']+s+doc['section']+s
	else:
		print "Нечего редактировать!"


