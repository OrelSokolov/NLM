# Приводим программу к первоначальному состоянию
if [ -e ./cfg/main.py ]; then
	echo -n "Сносим главный конфиг..."
	rm ./cfg/main.py
	echo "[done]"
	if [ -e ~/.nerd_backup/ ]; then
		echo -n "Восстанавливаем первоначальное состояние этой папки."
		mv ~/.nerd_backup/main.part1 ./cfg/
		mv ~/.nerd_backup/main.part2 ./cfg/
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
	rm -R  ~/.nerd_backup/ 
	echo "[done]"
fi;

if [ -e ~/.NerdLibraryManager ]; then
	echo -n "Удаляем папку с пользовательскими настройками..."
	rm -R ~/.NerdLibraryManager/
	echo "[done]" 
fi;

