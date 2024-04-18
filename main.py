#from win3 import start as settings_window
import PIL.Image
import pystray
from win11toast import toast
import keyboard as keyb
import sys
import threading
import zulip
import os
from config import config
import re
import subprocess
import cameras_connecting
import notifications


def read_config(image_path):
    if config.zulip_stream_status:
        zulip_send_message(image_path, stream=True, zulip_stream=config.zulip_stream.stream, zulip_topic=config.zulip_stream.topic)
    if config.zulip_private_status:
        zulip_send_message(image_path, direct=True, private_list=config.zulip_private_list)

    #сделать отправку на почту и сохранение на пк


def zulip_send_message(image_path, direct=False, stream=False, private_list=[], zulip_stream=None, zulip_topic=None):
    path = r'\\'.join([sys.path[0],'zuliprc2']) #путь конфига бота
    client = zulip.Client(config_file=path)
    # Upload a file
    print('stream',stream, ' direct', direct, ' private_list', private_list)
    with open(image_path, "rb") as fp:
        result = client.upload_file(fp)
    print(result)
    if direct:
        for i in private_list:
            print([int(i)])
            request = {
                "type": "private",
                "to": [int(i)],
                "content": "Check out [this picture]({}) of my castle!".format(result["uri"]),
            }
            result_ = client.send_message(request)
            if result_['result'] != 'success':
                print(f'the image was not delivered to the user with id {int(i)}', result_)
                #увед виндус что сообщение не дошло

    if stream:
        with open(image_path, "rb") as fp:
            result = client.upload_file(fp)
        request = {
                "type": "stream",
                "to": zulip_stream,
                "topic": zulip_topic,
                "content": "Check out [this picture]({}) of my castle!".format(result["uri"]),
            }
        result = client.send_message(request)
        print(result)



def make_screen():
    #надо сделать попытку подконекта и вывод если не получилось
    print('Пробуем сделать скрин из аудитории ', config.auditory)

    status = None
    if config.auditory == '435':
        rtsp = config.rtsp_435
        login = config.info_435['login']
        pwd = config.info_435['pwd']
        port = config.info_435['port']
        try:
            status = cameras_connecting.take_picture(rtsp, camera_login=login, camera_password=pwd, path=sys.path[0], camera_port=port)
        except Exception as e:
            print('not connected to 435')
    elif config.auditory == '505':
        rtsp = config.rtsp_505
        login = config.info_505['login']
        pwd = config.info_505['pwd']
        port = config.info_505['port']
        try:
            status = cameras_connecting.take_picture(rtsp, camera_login=login, camera_password=pwd, path=sys.path[0], camera_port=port)
        except Exception as e:
            print('not connected to 505')
    else:
        rtsp = config.rtsp
        login = config.info_other['login']
        pwd = config.info_other['pwd']
        port = config.info_other['port']
        try:
            status = cameras_connecting.take_picture(rtsp, camera_login=login, camera_password=pwd, path=sys.path[0],
                                                     camera_port=port)
        except Exception as e:
            print('not connected to other cam')

    if status is not None and status:
        image_path = r'\\'.join([sys.path[0],'image.jpg'])
        read_config(image_path) #читаем конфиг и отправляем везде где надо
        notifications.success_toast(r'\\'.join([sys.path[0],'image.jpg'])) #увед виндус
    else:
        notifications.bad_connection(r'\\'.join([sys.path[0],'connection_lost.png']))

def web_settings():
    command = ["streamlit", "run", r'\\'.join([sys_path[0],'web_interface.py'])]
    result = subprocess.run(command, capture_output=True, text=True)

def on_clicked(icon, item):
    threading.Thread(target=web_settings, daemon=True).start()
def app_exit():
    os._exit(1)


if __name__ == '__main__':
    sys_path = sys.path

    image = PIL.Image.open(sys_path[0]+'/inst.png')
    icon = pystray.Icon('ITStart', image, menu=pystray. \
        Menu(pystray.MenuItem('Настройки', on_clicked),
             pystray.MenuItem('Сделать скриншот', make_screen),
             pystray.MenuItem('Выход', app_exit)
    ))
    keyb.add_hotkey(' + '.join(config.hotkeys), make_screen) #автоматический тред
    icon.run() #запустили в главном потоке