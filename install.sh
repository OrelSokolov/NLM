echo 'Запущена установка Nerd Library Manager'
if [ -e ~/.NerdLibraryManager ]; then
	echo 'Все выглядит так, словно программа уже установлена. (Если хотите повторить установку - выполните удаление сначала)'
	exit 0
fi;
if [ -e ~/.nerd_backup ]; then
	echo 'Во время прошлой установки что-то пошло не так. Запустите удаление, прежде чем опять устанавливать.'
	exit 0
fi;

# Скопировать файлы в бэкап
echo -n 'Создание копии системных файлов...'
mkdir ~/.nerd_backup/
cp ~/.bashrc ~/.nerd_backup/
echo '[done]'

# Пропатчить файлы в системе
echo "Программа будет зарегестрирована в папке "$PWD
echo -n -e "У вас есть 9 секунд, чтобы отменить установку. Нажмите CTRL-C для отмены...\r"
	sleep 9
	echo -n -e "                                                                             \r"
echo -n "Патчим '.bashrc'..."
	echo "export PYTHONPATH=$PWD" >> ~/.bashrc
	echo "[done]"
echo "Сейчас приготовьтесь ввести свои данные для авторизации."
	sleep 2
echo -n "Введите свой логин для ВК: "
	read login
echo -n "и пароль: "
	read password
echo -n "Сохранение логина и пароля в файле конфигурации..."
	mkdir ~/.NerdLibraryManager
		mkdir ~/.NerdLibraryManager/cfg/ #Для файлов конфигурации
		mkdir ~/.NerdLibraryManager/tmp/ #Для временных файлов
	echo $login > ~/.NerdLibraryManager/cfg/auth.data
	echo $password >> ~/.NerdLibraryManager/cfg/auth.data
	echo "[done]"
echo -n "Собираем главный конфигурационный модуль..."
	cat $PWD/cfg/main.part1 > ./cfg/main.py
	echo  "app_path='$PWD/'" >> ./cfg/main.py
	lastdir=$PWD; cd ~/.NerdLibraryManager/;
	echo  "cfg_path='$PWD/cfg/'" >> $lastdir/cfg/main.py 
	echo  "tmp_path='$PWD/tmp/'" >> $lastdir/cfg/main.py 
	cd $lastdir
	cat $PWD/cfg/main.part2 >> ./cfg/main.py
	echo '[done]'
echo -n "Собираем главный скрипт с учетом запуска не из командной строки."
	cat $PWD/vk/handlers/filehandler.part1 > ./vk/handlers/filehandler.py
	echo "sys.path.append('$PWD')" >> ./vk/handlers/filehandler.py
	cat $PWD/vk/handlers/filehandler.part2 >> ./vk/handlers/filehandler.py
	echo "[done]"
echo -n "Собираем браузер для графической авторизации..."
	cat $PWD/vk/api/browser.part1 > ./vk/api/browser.py
	echo "sys.path.append('$PWD')" >> ./vk/api/browser.py
	cat $PWD/vk/api/browser.part2 >> ./vk/api/browser.py
	echo "[done]"
echo -n "Переносим файлы для сборки в бэкап-каталог..."
	mv ./cfg/main.part1 ~/.nerd_backup/
	mv ./cfg/main.part2 ~/.nerd_backup/
	mv ./vk/handlers/filehandler.part1 ~/.nerd_backup
	mv ./vk/handlers/filehandler.part2 ~/.nerd_backup
echo '[done]' 

#Сейчас установи все необходимые зависимости.
dist=`uname -a`
if [[ $dist ==  *Ubuntu* ]]; then
	echo "Ваш дистрибутив: Ubuntu."
	echo "Сейчас тебе будет предложено установить необходимые пакеты."
	sleep 5
	sudo apt-get install rtmpdump python python-pypdf python-requests djvulibre-bin imagemagick
	echo -n "Собираем действие для контекстного меню..."
		cat $PWD/sysfiles/upload.desktop.part1 > ./sysfiles/upload.desktop
		echo "Icon[ru_RU]=$PWD/sysfiles/upload.png" >> ./sysfiles/upload.desktop
		echo "Icon[ru]=$PWD/sysfiles/upload.png" >> ./sysfiles/upload.desktop
		cat $PWD/sysfiles/upload.desktop.part2 >> ./sysfiles/upload.desktop
		echo "Exec=gnome-terminal -e 'python $PWD/vk/handlers/filehandler.py %f'" >> ./sysfiles/upload.desktop
		echo  "[done]"
	echo -n "Создаем действие контекстного меню..."
		if [ ! -e ~/.local/share/file-manager/actions/ ]; then
			mkdir ~/.local/share/file-manager/actions/
		fi;
		mv ./sysfiles/upload.desktop ~/.local/share/file-manager/actions/
		echo "Создано"
fi

echo "------------------------"
echo "Все. Вроде установили =)"
