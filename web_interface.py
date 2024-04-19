import time

import streamlit as st
from config import config
import re
import subprocess
import sys
import keyboard
import threading


def rtsp_address(auditory): #обрабатываем rtsp адрес
    #вывести здесь картинку полученную с камеры (ну или статус подключения)
    if auditory == '435':
        st.warning('Если вы измените этот адрес, он будет сохранен за этой аудиторией')
        return config.rtsp_435
    elif auditory == '505':
        st.warning('Если вы измените этот адрес, он будет сохранен за этой аудиторией')
        return config.rtsp_505
    else:
        st.write('Введите адрес камеры, к которой хотите подключиться')
        return config.rtsp


def save_config(auditory, rtsp, zulip_private_status, zulip_stream_status, zulip_private_list, zulip_stream_name, zulip_stream_topic, \
                mail_status, mail_list, hotkeys, port, login, pwd):

    #обработка списков конфига. Нужно добавить обработку ввода stream_name и stream_topic
    zulip_private_list = re.findall(r'\d+', zulip_private_list)
    email_compile = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}',re.IGNORECASE)
    mail_list = email_compile.findall(mail_list)


    config.auditory = auditory
    if auditory == '435':
        config.rtsp_435 = rtsp
        config.info_435['port'] = port
        config.info_435['login'] = login
        config.info_435['pwd'] = pwd
    elif auditory == '505':
        config.rtsp_505 = rtsp
        config.info_505['port'] = port
        config.info_505['login'] = login
        config.info_505['pwd'] = pwd
    else:
        config.rtsp = rtsp
        config.info_other['port'] = port
        config.info_other['login'] = login
        config.info_other['pwd'] = pwd

    config.zulip_private_status = zulip_private_status
    config.zulip_stream_status = zulip_stream_status
    config.zulip_private_list = zulip_private_list
    config.zulip_stream.stream = zulip_stream_name
    config.zulip_stream.topic = zulip_stream_topic

    config.mail_status = mail_status
    config.mail_list = mail_list

    if len(hotkeys) == 0:
        config.hotkeys = ['ctrl','h']
    else:
        config.hotkeys = hotkeys
    config.hotkeys_interim = []
    config.dump()

def add_info(auditory):

    dict = {
        '435': config.info_435,
        '505': config.info_505,
        'other': config.info_other
    }

    port = st.text_input('Port камеры : ', dict[auditory]['port'])
    login = st.text_input('Login : ', dict[auditory]['login'])
    pwd = st.text_input('Password : ', dict[auditory]['pwd'])

    return port, login, pwd


def page_create():
    print('старт программы')

    if 'keyb' not in st.session_state:
        st.session_state['keyb'] = 0

    st.title('Настройка конфига')
    st.subheader('RSTP адрес')
    auditory = st.selectbox('Аудитория :', ['435','505','other'])
    rtsp = st.text_input('RTSP адрес или ip камеры :', rtsp_address(auditory))
    port, login, pwd = add_info(auditory)
    st.write('')
    st.write('')
    st.write('')


    st.subheader('Рассылка зулип')
    zulip_private_status = st.checkbox('Личные сообщения', value=config.zulip_private_status)
    if zulip_private_status:
        zulip_private_list = st.text_input("Введите ID пользователей", value=', '.join(config.zulip_private_list))
    else:
        zulip_private_list = ', '.join(config.zulip_private_list)
    zulip_stream_status = st.checkbox('Сообщения в канал', value=config.zulip_stream_status)
    if zulip_stream_status:
        zulip_stream_name = st.text_input("Название канала", value=config.zulip_stream.stream)
        zulip_stream_topic = st.text_input("Название топика", value=config.zulip_stream.topic)
    else:
        zulip_stream_name = config.zulip_stream.stream
        zulip_stream_topic = config.zulip_stream.topic
    st.write('')
    st.write('')
    st.write('')


    st.subheader('Рассылка на почту')
    mail_status = st.checkbox('Отправить на почту', value=config.mail_status)
    if mail_status:
        mail_list = st.text_input("Введите список email адресов", value=', '.join(config.mail_list))
    else:
        mail_list = ', '.join(config.mail_list)
    st.write('')
    st.write('')
    st.write('')


    st.subheader('Горячие клавиши')
    st.warning(f"Сделать скриншот: {' + '.join(config.hotkeys)}")
    set_hotkey = st.checkbox('Изменить горячие клавиши')
    if set_hotkey:
        st.warning(f'нажимайте по одной: {" + ".join(config.hotkeys_interim)}')
        if st.session_state['keyb'] == 0:
            if st.button('слушать', type='primary'):
                config.hotkeys_interim = [] #сбрасываем из конфига установленные хк
                config.stop_flag = True
                config.dump()
                st.session_state['keyb'] = 1
                start_listener()
                st.rerun()
            else:
                config.stop_flag = False
                config.dump()
        else:
            if st.button('стоп'):
                config.stop_flag = True
                config.dump()
                print('s f = ', config.stop_flag)
                st.session_state['keyb'] = 0
                st.rerun() #перезагрузили чтобы отобразились кнопки
            else:
                config.stop_flag = True
                config.dump()



    st.write('')
    st.write('')

    if st.button('Сохранить', type='primary'):
        print('вы нажали сохранить, убираю флаг, запускаю проверку потока')
        #global stop_flag
        #stop_flag = False

        config.dump()
        save_config(auditory, rtsp, zulip_private_status, zulip_stream_status, zulip_private_list, zulip_stream_name, zulip_stream_topic, mail_status, mail_list, config.hotkeys_interim, port, login, pwd)
        st.success('Изменения сохранены. Перезапустите программу, чтобы они вошли в силу')
        time.sleep(1)
        st.rerun()
    print('stop flag in main funct2', config.stop_flag)

def key_listener():
    print('мы в лисенере')
    while config.stop_flag:
        print('stop flag = ', config.stop_flag)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_UP:
            print(event.name)
            config.hotkeys_interim.append(event.name)
            config.dump()
            print('я тут')
    print('выключение потока')


def start_listener():
    key_thread = None
    for thread in threading.enumerate():
        if thread.name == "key_listener" and thread.is_alive():
            key_thread = thread
            break
    if key_thread is None:
        key_thread = threading.Thread(target=key_listener, name="key_listener",daemon=True)
        key_thread.start()
if __name__ == '__main__':
    page_create()