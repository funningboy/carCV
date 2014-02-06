""" lane detection over houghlinesP """

import cv2
import numpy as np

def detect_lane_over_houghlinesP(name, img, cfg):
    """ detect lane over houghlinesP
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

        # canny edge detection
        edge = cv2.Canny(gray, cfg['canny']['threshold1'], cfg['canny']['threshold2'], cfg['canny']['apertureSize'])
        return edge

    def _detect(edge, cfg):
        """ find correlation edges for probabilistic line detection """
        lines = cv2.HoughLinesP(edge, cfg['houghlinesp']['rho'], cfg['houghlinesp']['theta'], cfg['houghlinesp']['threshold'], minLineLength=cfg['houghlinesp']['minlinelength'], maxLineGap=cfg['houghlinesp']['maxlinegap'])
        if lines is None:
            return []
        return lines

    def _draw(img, lines, cfg):
        """ draw results """
        for line in lines:
            for obj in line:
                [x1, y1, x2, y2] = obj
                dx, dy = x2 - x1, y2 - y1
                angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
                if angle <= cfg['filter']['angle']  and angle >= - cfg['filter']['angle']:
                    return img
                cv2.line(img, (x1,y1), (x2,y2), cfg['color']['green'], 2)
        return img

    def _show(img):
        """ show img """
        cv2.imshow('houghlinesP_img', img)
        cv2.waitKey(1)

    def _warning(img, lines, cfg):
        """ warning """
        pass

    def _debug_draw(edge, lines, cfg):
        """ debug with draw """
        img = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
        for line in lines:
            for obj in line:
                [x1, y1, x2, y2] = obj
                dx, dy = x2 - x1, y2 - y1
                angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
                if angle <= cfg['filter']['angle']  and angle >= - cfg['filter']['angle']:
                    return img
                cv2.line(img, (x1,y1), (x2,y2), cfg['color']['green'], 2)
        return img

    def _debug_show(edge):
        """ debug with show """
        cv2.imshow('houghlinesP_edge', edge)
        cv2.waitKey(1)

    # methods
    edge = _prepare(img.copy(), cfg)
    lines = _detect(edge, cfg)

    if cfg['set']['show'] not in [None, Fasle]:
        img = _draw(img, lines, cfg)
        _show(img)

    if cfg['set']['debug'] not in [None, Fasle]:
        edge = _debug_draw(edge, lines, cfg)
        _debug_show(edge)

    return img


