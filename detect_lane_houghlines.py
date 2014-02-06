""" lane detection over houghlines """

import cv2
import numpy as np

def detect_lane_over_houghlines(name, img, cfg):
    """ detect lane over houghlines
        name : proc name or proc id
        img : img source
        cfg : lane config
    """

    def _prepare(img, cfg):
        """ prepare proc for edge collection """
        ht, wd, dp = img.shape

        # only care about the horizont block, filter out up high block
        img[0:int(ht/2),:] = cfg['color']['black']
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # gaussian smooth over standard deviation, reduce noise
        gray = cv2.GaussianBlur(gray, cfg['gaussian']['ksize'], cfg['gaussian']['border'])

        # smooth and canny edge detection
        edge = cv2.Canny(gray, cfg['canny']['threshold1'], cfg['canny']['threshold2'], cfg['canny']['apertureSize'])
        return edge

    def _detect(edge, cfg):
        """ find correlation edges for standard line detection """
        lines = cv2.HoughLines(edge, cfg['houghlines']['rho'], cfg['houghlines']['theta'], cfg['houghlines']['threshold'])
        if lines is None:
            return []
        return lines

    def __find_from_to_xy(img, obj, cfg):
        """ find from pp (x,y) and to pp (x,y) """
        ht, wd, dp = img.shape
        [rho, theta] = obj

        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho

        # y = ax + b
        x1, y1 = int(x0 + 1000*(-b)), int(y0 + 1000*(a))
        x2, y2 = int(y0 - 1000*(-b)), int(y0 - 1000*(a))

        # boundary check
        x1 = x1 if x1 <= wd else x1 if x1 >= 0 else 0
        x2 = x2 if x2 <= wd else x2 if x2 >= 0 else 0
        y1 = y1 if y1 <= ht else y1 if y1 >= int(ht/2) else int(ht/2)
        y2 = y2 if y2 <= ht else ht if y2 >= int(ht/2) else int(ht/2)
        return x1, y1, x2, y2

    def __find_angle(img, obj, cfg):
        """ angle """
        x1, y1, x2, y2 = __find_from_to_xy(img, obj, cfg)
        dx, dy = x2 - x1, y2 - y1
        angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
        return angle, x1, y1, x2, y2

    def _draw(img, lines, cfg):
        """ draw results """
        for line in lines:
            for obj in line:
                angle, x1, y1, x2, y2 = __find_angle(img, obj, cfg)
                if angle <= cfg['filter']['angle'] and angle >= - cfg['filter']['angle']:
                    return img
                cv2.line(img, (x1,y1), (x2,y2), cfg['color']['blue'], 2)
        return img

    def _show(img):
        """ show img """
        cv2.imshow('houghlines_img', img)
        cv2.waitKey(1)

    def _debug_draw(edge, lines, cfg):
        """ debug with draw """
        img = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
        ht, wd, dp = img.shape
        for line in lines:
            for obj in line:
                angle, x1, y1, x2, y2 = __find_angle(img, obj, cfg)
                if angle <= cfg['filter']['angle'] and angle >= - cfg['filter']['angle']:
                    return img
                cv2.line(img, (x1,y1), (x2,y2), cfg['color']['blue'], 2)
        return img

    def _debug_show(edge):
        cv2.imshow('houghlines_edge', edge)
        cv2.waitKey(1)

    # methods
    edge = _prepare(img.copy(), cfg)
    lines = _detect(edge, cfg)

    if cfg['set']['show'] not in [None, False]:
        img = _draw(img, lines, cfg)
        _show(img)

    if cfg['set']['debug'] not in [None, False]:
        edge = _debug_draw(edge, lines, cfg)
        _debug_show(edge)

    return img



