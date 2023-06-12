from cv2 import VideoCapture, imshow, waitKey, cvtColor, COLOR_BGR2GRAY, GaussianBlur, absdiff, threshold, \
    THRESH_BINARY, dilate, findContours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, contourArea, boundingRect, rectangle, \
    imwrite
from time import sleep
from glob import glob
from os.path import getmtime, join
from os import listdir, remove
from emailing import send_email


def delete_old_images():
    directory_path = "images"

    for image in listdir(directory_path):
        image_path = join(directory_path, image)
        remove(image_path)


delete_old_images()
video = VideoCapture(0)
sleep(1)

first_frame = None
status_list = []
count = 1

while True:
    status = 0
    check, frame = video.read()
    gray_scale = cvtColor(frame, COLOR_BGR2GRAY)
    gray_scale_gau = GaussianBlur(gray_scale, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_scale_gau

    delta_frame = absdiff(first_frame, gray_scale_gau)

    thresh_frame = threshold(delta_frame, 45, 255, THRESH_BINARY)[1]
    dil_frame = dilate(thresh_frame, None, iterations=2)

    contours, check = findContours(dil_frame, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if contourArea(contour) < 5000:
            continue
        x, y, w, h = boundingRect(contour)
        rect = rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rect.any():
            status = 1
            imwrite(f"images/{count}.png", frame)
            count += 1

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        all_images = sorted(glob("images/*.png"), key=getmtime)
        index = int(len(all_images) / 2)
        image_with_object = all_images[index]
        # send_email(image_with_object)

    imshow("Video", frame)

    key = waitKey(1)

    if key == ord("q"):
        break

video.release()
