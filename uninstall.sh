#Восстановить .bashrc
echo -n "Восстанавливаем системные файлы..."
mv ~/.nerd_backup/.bashrc ~/
echo "[done]"
# Удалить папку с бэкапам
echo -n "Удаляем папку с прошлым бэкапом..."
rm -R  ~/.nerd_backup/ 
echo "[done]"
echo -n "Удаляем папку с пользовательскими настройками..."
rm -R ~/.NerdLibraryManager/
echo "[done]"


