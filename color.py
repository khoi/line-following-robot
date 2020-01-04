# importing Modules
import os

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

low_yellow = np.array([22, 100, 20], np.uint8)
high_yellow = np.array([40, 255, 255], np.uint8)

low_green = np.array([55, 100, 20], np.uint8)
high_green = np.array([80, 255, 255], np.uint8)

low_blue = np.array([100, 100, 20], np.uint8)
high_blue = np.array([140, 255, 255], np.uint8)


while 1:
    _, img = cap.read()

    # converting frame(img) from BGR (Blue-Green-Red) to HSV (hue-saturation-value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    yellow_mask = cv2.inRange(hsv, low_yellow, high_yellow)
    yellow = cv2.bitwise_and(img, img, mask=yellow_mask)

    green_mask = cv2.inRange(hsv, low_green, high_green)
    green = cv2.bitwise_and(img, img, mask=green_mask)

    blue_mask = cv2.inRange(hsv, low_blue, high_blue)
    blue = cv2.bitwise_and(img, img, mask=blue_mask)

    # color: (contours, rectangle color)
    contours_dict = {
        "yellow": (sorted(cv2.findContours(
            yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )[0], key=cv2.contourArea)[-1:], (0, 255, 255)),
        "green": (sorted(cv2.findContours(
            green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )[0], key=cv2.contourArea)[-1:], (0, 255, 0)),
        "blue": (sorted(cv2.findContours(
            blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )[0], key=cv2.contourArea)[-1:], (255, 0, 0)),
    }

    for color_key, (contours, rec_color) in contours_dict.items():
        print(f"{color_key} {len(contours)}")
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), rec_color, 3)

    window_name = "Color Tracking"
    cv2.namedWindow(window_name)  # Create a named window
    cv2.moveWindow(window_name, 40, 30)  # Move it to (40,30)

    cv2.imshow(window_name, img)

    if cv2.waitKey(10) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()
        break