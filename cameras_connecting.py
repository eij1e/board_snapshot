import requests
from onvif import ONVIFCamera
import re
import time
import sys
from requests.auth import HTTPDigestAuth


def check_ping(rtsp:str, camera_login:str, camera_password:str, camera_port:int): #сделать чтобы из конфига парсился порт и лог с паролем
    status = 1
    while True:
        ip_address = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', string=rtsp)
        camera_ip = ip_address[0]
        try:
            ONVIFCamera(camera_ip, camera_port, camera_login, camera_password)
            print('mycam is connected')
            if status == 0:
                status = 1
                #сменить картинку в трее
        except Exception as e:
            print('Error:', e)
            if status == 1:
                status = 0
                #сменить картинку в трее
        time.sleep(5)

def home_rotation(camera_ip:str, camera_login:str, camera_password:str, camera_port:int):
    try:
        mycam = ONVIFCamera(camera_ip, camera_port, camera_login, camera_password)
        print('mycam is connected')
        ptz = mycam.create_ptz_service()
        media = mycam.create_media_service()
        profiles = media.GetProfiles()
        token = profiles[0].token
        ptz.GotoHomePosition({'ProfileToken': token})
        return True
    except Exception as e:
        print('Error:', e)
        return False

def take_picture(rtsp:str, camera_login:str, camera_password:str, camera_port:int, path:str = ''):
    ip_address = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', string=rtsp)
    camera_ip = ip_address[0]
    if home_rotation(camera_ip=camera_ip, camera_port=camera_port, camera_password=camera_password, camera_login=camera_login):
        try:
            mycam = ONVIFCamera(camera_ip, camera_port, camera_login, camera_password)
            media = mycam.create_media_service()
            profiles = media.GetProfiles()
            token = profiles[0].token
            uri = media.GetSnapshotUri({'ProfileToken': token})['Uri']
            resp = requests.get(uri, auth=HTTPDigestAuth(camera_login, camera_password))
            #resp = requests.get(uri, auth=(camera_login, camera_password))
            print(path+r'\image.jpg')
            print('stat code: in ',resp.status_code)
            with open(path+r'\image.jpg', 'wb') as f:
                f.write(resp.content)
                print('saved image')
            return True
        except Exception as e:
            print('Error:', e)
            return False
    else:
        return False

if __name__ == '__main__':
    rtsp = 'rtsp://admin:Supervisor@172.18.212.15/onvif-media/media.amp?profile=profile_1_h264&sessiontimeout=60&streamtype=unicast'
    camera_port = 80
    camera_login = 'admin'
    camera_password = 'Supervisor'
    take_picture(rtsp=rtsp, camera_login=camera_login, camera_password=camera_password,camera_port=camera_port,path = sys.path[0])
