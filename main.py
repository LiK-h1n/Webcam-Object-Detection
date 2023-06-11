from cv2 import VideoCapture, imshow, waitKey, cvtColor, COLOR_BGR2GRAY, GaussianBlur, absdiff, threshold, \
    THRESH_BINARY, dilate, findContours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, contourArea, boundingRect, rectangle
from time import sleep

video = VideoCapture(0)
sleep(1)

first_frame = None

while True:
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
        rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    imshow("Video", frame)

    key = waitKey(1)

    if key == ord("q"):
        break

video.release()