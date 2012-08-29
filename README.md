# Прочитай меня!
Привет, админ!

Этот пакет скриптов и модулей поможет тебе легко управлять библиотекой.

Список поддерживаемых дистрибутивов GNU/Linux:
----------------------------------------------
	-Ubuntu 12.04


------------------------| КОНФИГУРИРОВАНИЕ СИСТЕМЫ |--------------------------------

Выполнить:


`export PYTHONPATH="/home/user/python/NerdLibraryManager/"`


-------------------------| НАСТРОЙКА ДЕЙСТВИЙ КОНТЕКСТНОГО МЕНЮ |-----------------------------
NAUTILUS:
	1) Установите пакет nautilus-actions
	2) Создайте новое действие для меню.
-----------------------------------
Пример для загрузки документов в ВК.
	1) Action -> Context label: Upload to VK
	2) Action -> Icon -> Browse (Выбираем иконку)
	3) Command -> Path: python
	4) Command -> Parameters: '/home/oleg/python/NerdLibraryManager/network/upload.py'  '%f'
	5) Execution -> Execution mode -> Display output


