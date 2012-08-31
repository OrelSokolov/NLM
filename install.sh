echo 'Запущена установка Nerd Library Manager'
if [ -e ~/.NerdLiraryManager ]; then
	echo 'В системе присутствуют файлы от прошлой установки. Выполните удаление сначала'
	exit 0
fi
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
echo $login > ~/.NerdLibraryManager/auth.data
echo $password >> ~/.NerdLibraryManager/auth.data
echo "[done]"
#Сейчас установи все необходимые зависимости.
dist=`uname -a`
if [[ $dist ==  *Ubuntu* ]]; then
	echo "Ваш дистрибутив: Ubuntu."
	echo "Сейчас тебе будет предложено установить необходимые пакеты.\n"
	sleep 5
	sudo apt-get install rtmpdump
fi

echo "Все. Вроде установили =)"
