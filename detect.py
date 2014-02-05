
import cv2
import numpy as np
import detect_car
import detect_lane


def test():
    """ detect car speed """
    capture = cv2.VideoCapture('data/road.avi')
    while True:
        ret, img = capture.read()

if __name__ == '__main__':
    test()
