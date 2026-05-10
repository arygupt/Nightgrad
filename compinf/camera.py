from queue import Empty
from zoneinfo import available_timezones
import cv2 as cv
import glob
import os
from cv2_enumerate_cameras import enumerate_cameras


def get_available_cameras():
    available_cameras = []
    for i in range(5):
        cap = cv.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
            print(width, height)
    return available_cameras

'''
def cameras_generator(ca=cv.CAP_ANY):
    for path in glob.glob('/dev/video*'):
        device_name = os.path.basename(path):
'''          

cameras = get_available_cameras()

if cameras != Empty:
    print(f"Available cameras: {cameras}")
else:
    print("No cameras found")

for camera_info in enumerate_cameras():
    print(f'{camera_info.index - 1200}: {camera_info.name}')

