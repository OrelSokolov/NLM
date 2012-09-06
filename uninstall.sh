function del()
{
	if [ -e $1 ]; then
		if [ -d $1 ]; then
			rm -R $1
			if [[ $2 != 'quiet' ]]; then
				echo "Удален каталог $1" 
			fi;
		fi;
		if [ -f $1 ]; then
			rm $1
			if [[ $2 != 'quiet' ]]; then
				echo "Удален файл $1"
			fi;
		fi;
	fi;
}




# Приводим программу к первоначальному состоянию
if [ -e ./cfg/main.py ]; then
	echo -n "Сносим главный конфиг..."
		del ./cfg/main.py 'quiet'
	echo "[done]"
	echo -n "Сносим главный загрузочный скрипт..."
		del ./vk/handlers/filehandler.py "quiet"
	echo "[done]"
	if [ -e ~/.nerd_backup/ ]; then
		echo -n "Восстанавливаем первоначальное состояние этой папки."
		mv ~/.nerd_backup/main.part1 ./cfg/
		mv ~/.nerd_backup/main.part2 ./cfg/
		mv ~/.nerd_backup/filehandler.part1 ./vk/handlers/
		mv ~/.nerd_backup/filehandler.part2 ./vk/handlers/
		echo '[done]'
	fi;
fi;

if [ -e ~/.nerd_backup ]; then
#Восстановить .bashrc
	echo -n "Восстанавливаем системные файлы..."
	mv ~/.nerd_backup/.bashrc ~/
	echo "[done]"
# Удалить папку с бэкапам
	echo -n "Удаляем папку с прошлым бэкапом..."
	del  ~/.nerd_backup/ 'quiet'
	echo "[done]"
fi;

echo -n "Удаляем папку с пользовательскими настройками..."
	del ~/.NerdLibraryManager/ 'quiet'
echo "[done]" 


echo "Удаляем *.pyc файлы"
#Чистим папку cfg
	del "./cfg/__init__.pyc"
	del "./cfg/main.pyc"
#Чистим папку vk
	del "./vk/__init__.pyc"
#Чистим папку vk/api
	del "./vk/api/api.pyc"
	del "./vk/api/term_auth.pyc"
	del "./vk/api/__init__.pyc"
	del "./vk/api/browser.py" # Мы же его собираем
#Чистим папку vk/basics
	del "./vk/basics/__init__.pyc"
	del "./vk/basics/docs.pyc"
	del "./vk/basics/pages.pyc"
	del "./vk/basics/photos.pyc"
	del "./vk/basics/storage.pyc"
	del "./vk/basics/wall.pyc"
	
#Чистим папку vk/handlers
	del "./vk/handlers/__init__.pyc" 
	del "./vk/handlers/filehandler.pyc"
	del "./vk/handlers/dbhandler.pyc"
	del "./vk/handlers/wikihandler.pyc"
# Чистим папку local
	del "./local/__init__.pyc"
	del "./local/cover.pyc"
	del "./local/description.pyc"
	del "./local/docpages.pyc"
#Чистим папку remote
	del "./remote/__init__.pyc"
#Удаляем контекстные действия
	del ~/.local/share/file-manager/actions/upload.desktop
echo -n -e "Программа приведена к доустановочному состоянию.\r"
sleep 1
echo "Теперь вы можете запустить установку заново.                  "
