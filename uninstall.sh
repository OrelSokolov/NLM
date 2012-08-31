
if [ -e ~/.nerd_backup ]; then
#Восстановить .bashrc
	echo -n "Восстанавливаем системные файлы..."
	mv ~/.ned_backup/.bashrc ~/
	echo "[done]"
# Удалить папку с бэкапам
	echo -n "Удаляем папку с прошлым бэкапом..."
	rm -R  ~/.nerd_backup/ 
	echo "[done]"
fi;

if [ -e ~/.NerdLibraryManager ]; then
	echo -n "Удаляем папку с пользовательскими настройками..."
	rm -R ~/.NerdLibraryManager/
	echo "[done]" 
fi;


