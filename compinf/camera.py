import cv2 as cv
import subprocess

def get_available_cameras():
    available_cameras = []
    for i in range(2):
        cap = cv.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras
cameras = get_available_cameras()

# hacky way to get camera name
def cam_list():
    cam = []
    result = subprocess.run(
        ["ffmpeg", "-f", "avfoundation", "-list_devices", "true", "-i", ""],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    
    for line in result.stderr.splitlines():
        if "Camera" in line:
            cam.append(line.split("] ")[-1])

    for i,x in enumerate(cam):
        print(i, f"{x}")

if cameras:
    print(f"Available cameras: {cameras}")
    cam_list()
else:
    print("No cameras found")
    
