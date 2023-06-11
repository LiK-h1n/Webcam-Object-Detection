from cv2 import VideoCapture, imshow, waitKey
from time import sleep

video = VideoCapture(0)
sleep(1)

while True:
    check, frame = video.read()
    imshow("My Video", frame)

    key = waitKey(1)

    if key == ord("q"):
        break

video.release()