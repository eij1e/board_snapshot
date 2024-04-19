from win11toast import toast
import sys

def success_toast(image_path):
    toast('Boardsnapshot', 'Success! Sending an image', image=f'{sys.path[0]}/image.jpg', duration='short')


def bad_connection(icon_path):
    toast('Boardsnapshot', 'The connection to the camera is not established, check the correctness of the data, VPN, or your Internet connection', icon=f'{sys.path[0]}/connection_lost.png', duration='long')