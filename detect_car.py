""" car detection """

import cv2
import numpy as np
from config_car import *

gb_car_cfg = CarCfg

def detect_car(name, img, cfg):
    """ detect car """

    global gb_car_cfg

    def _train_data(cfg):
        """ training data """
        if cfg['cascade']['train_ptr'] is None:
            cfg['cascade']['train_ptr'] = cv2.CascadeClassifier(cfg['cascade']['train_data'])

    def _prepare(img, cfg):
        """ prepare analysis proc for alg input """
        ht, wd, dp = img.shape

        # only care about the horizont block, filter out up high block
        img[0:int(ht/2),:] = cfg['color']['black']
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # gaussian smooth over standard deviation, reduce noise
        gray = cv2.GaussianBlur(gray, cfg['gaussian']['ksize'], cfg['gaussian']['border'])

        # resize for fast factor detection
        new_ht, new_wd = np.int32(np.around(ht*cfg['set']['resize'])), np.int32(np.around(wd*cfg['set']['resize']))
        gray = cv2.resize(gray, (new_ht, new_wd), interpolation = cv2.INTER_LINEAR)

        # histogram sample
        gray = cv2.equalizeHist(gray)
        return gray

    def _detect(gray, cfg):
        """ haarcascascade alg to find target obj """
        cascade = cfg['cascade']['train_ptr']
        rects = cascade.detectMultiScale(gray, scaleFactor=cfg['cascade']['scale_factor'], minNeighbors=cfg['cascade']['min_neighbors'], flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        if rects is None:
            return []
        return rects

    def _draw(img, gray, rects, cfg):
        """ draw results """
        i_ht, i_wd, i_dp = img.shape
        g_ht, g_wd = gray.shape
        for x1, y1, x2, y2 in rects:
            ht_resize, wd_resize = float(i_ht)/g_ht,  float(i_wd)/g_wd

            # circle centre point and radios
            x, y = np.int32(np.around((2*x1+x2)/2*wd_resize)), np.int32(np.around((2*y1+y2)/2*ht_resize))
            radius = np.int32(np.around(x2*wd_resize*0.5)) if x2 < y2 else np.int32(np.around(y2*ht_resize*0.5))
            cv2.circle(img, (x,y), radius, cfg['color']['red'], 2)
        return img

    def _show(img):
        """ show img """
        cv2.imshow('cascade', img)
        cv2.waitKey(1)

    def _debug_draw(gray, rects, cfg):
        """ debug with draw """
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        for x1, y1, x2, y2 in rects:

            # circle centre point and radious
            x, y = np.int32(np.around((2*x1+x2)/2)), np.int32(np.around((2*y1+y2)/2))
            radius = np.int32(np.around(x2*0.5)) if x2 < y2 else np.int32(np.around(y2*0.5))
            cv2.circle(img, (x,y), radius, cfg['color']['red'], 2)
        return img

    def _debug_show(img):
        """ debug whith show """
        cv2.imshow('debug_cascade', img)
        cv2.waitKey(1)

    # methods
    _train_data(cfg)

    gray = _prepare(img.copy(), cfg)
    rects = _detect(gray, cfg)

    if cfg['set']['show'] not in [None, False]:
        img = _draw(img, gray, rects, cfg)
        _show(img)

    if cfg['set']['debug'] not in [None, False]:
        gray = _debug_draw(gray, rects, cfg)
        _debug_show(gray)

    return img


def test():
    """ test lane detection """
    global gb_car_cfg

    capture = cv2.VideoCapture('data/road.avi')

    # register proc to manager
    proc = {    'detect_car'      : detect_car
            }

    while True:
        ret, img = capture.read()
        proc[gb_car_cfg['set']['proc']](gb_car_cfg['set']['proc'], img, gb_car_cfg)


if __name__ == '__main__':
    test()
