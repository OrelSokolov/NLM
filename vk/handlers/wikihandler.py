
#По полученным параметрам строит вики-страницу и сохраняет ее под нужным именем.



##
##
##   ДОРАБОТАТЬ!!!!!!! ДОРАБОТАТЬ!!!!!
##
def buildPage(photo="vk.com/id0", url="vk.com/id0", title="Title", authors="authors", descr="empty"):
	'''Строит страницу по полученным данным.'''
	page='''
{|
|-
|[[photo-'''+photo+'''|200px;nolink| Обложка]]
|'''+descr+'''<br/>
|-
!['''+url+'''|Скачать]
|'''+title+authors+'''
|}
'''


