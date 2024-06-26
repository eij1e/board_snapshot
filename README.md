Цель проекта – реализовать приложение, позволяющее легко и быстро сделать конспект доски после переговоров или совещаний. Весь рабочий процесс будет запечатлен скриншотами и разослан всем участникам без особых затрат


Функционал:
- Подключается по ip (обязательно нужны port, login, password) к камере
- Получает изображение, записывает его в папку проекта
- Обрабатывает конфигурационный файл для рассылки изображения по необходимым соц. сетям
- Отправка уведомлений (в разработке):
- Определяет windows уведомление со статусом доставки сообщений для каждого пользователя - выводит список пользователей, которым (в разработке) 
- Отправляет windows уведомление с отправляемым скриншотом (при успешном подключении к камере)
- Отправляет windows уведомление при отсутствии подключения к выбранной камере (в разработке)
- Периодическая проверка подключения (в разработке): 
- Проверяет подключение к камере, уведомление при первом отсутствии подключения, при первом успешном подключении (в разработке)
- Проверка и обработка изображения (в разработке):
- Изображение проверяется на качество с помощью openCV , происходит дообработка изображения (по необходимости)


Требования для MVP:
- полностью рабочая логика программы - нет коллизий потоков
- реализован удобный web-интерфейс
- необходимые конфигурации устанавливаются и читаются как необходимо
- программа не крашится из-за возможных ошибок
- программа отправляет изображение в Zulip

Требования для MUP:
- есть проверка подключения к камере раз в n-секунд, приходит соответствующее уведомление
- есть установленный time_error , чтобы за 3 секунды узнавать о невозможности сделать скриншот
- программа уведомляет, кому из списка получателей не было доставлено сообщение (если такие есть)
- программа определяет доску на изображении с помощью OpenCV, исправно корректирует изображение
- программа отправляет изображение в Zulip, Telegram, почту

Содержание репозитория:
- Приложение:
     boardsnapshot - приложение для получения изображения с доски путем нажатия горячих клавиш
- Модули:
     - main.py
     Управляет главными потоками приложения (считывание горячих клавиш для скриншота, открытие приложения в трее, обработка конфига, связывает микро-сервисы между 
     собой) 
    - web_interface.py
      Генерация веб-страницы для управления конфигом приложения
    - cameras_connecting.py
      Работа с onfiv - функции проверки подключения, получения изображения с камеры, установки камеры в home position
    - config.py
      Класс Config, содержащий методы инициализации конфига, перезаписи конфига 
    - notifications.py
      Содержит функции windows уведомлений для отправки уведомлений об удачном\неудачном скриншоте 
- Дополнительные файлы:
  - config.json 
    конфиг файл, хранящий все необходимые пользовательские настройки
  - requirements.txt 
    список библиотек для установки в окружение
  - zuliprc2 
    конфиг бота для рассылки скриншотов в zulip (можете поместить своего)
  - connection_lost.png
    иконка для уведомления об неудачном соединении с камерой

Установка:
- Cклонируйте репозиторий:

     git clone https://github.com/eij1e/board_snapshot.git
- Установите все необходимые библиотеки из списка с помощью команды
  
     pip install -r requirement.txt
- Выполните инструкции по установке библиотеки onvif по [ссылке](https://github.com/FalkTannhaeuser/python-onvif-zeep)
- При возникновении проблемы с путями (библиотека встала криво):
 - Перейдите в папку окружения ~\.venv\Lib\onvif_zeep\Lib
 - Перенесите папку wdsl на 1 вверх в папку ~\.venv\Lib\onvif_zeep
- Запустите файл main.py
Приложение готово к использованию и появилось в трее


