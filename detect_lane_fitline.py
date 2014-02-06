""" lane detection over fitline """

import cv2
import numpy as np

def detect_lane_over_fitline(name, img, cfg):
    """ detect lane over fitline
        name : proc name or proc id
        img : img source
        cfg : lane config
    """

    def _prepare(img, cfg):
        """ prepare """
        ht, wd, dp = img.shape

        # only care about the horizont block, filter out up high block
        img[0:int(ht/2),:] = cfg['color']['black']

        # threshold, remain the white or yellow line
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, cfg['threshold']['threshold1'], cfg['threshold']['threshold2'], cv2.THRESH_BINARY)
        return thresh

    def _detect(thresh, cfg):
        """ use contours and fitline to detect line """
        contours, hier = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if contours is None:
            return []
        return [cv2.fitLine(cnt,cv2.cv.CV_DIST_L2,0,0.01,0.01) for cnt in contours]

    def __find_from_to_xy(img, line, cfg):
        """ find from pp (x,y) and to pp (x,y) """
        ht, wd, dp = img.shape
        [vx, vy, x, y] = line

        # y = ax + b
        x1, y1 = int(x-vx*int(ht/2)), int(y-vy*int(ht/2))
        x2, y2 = int(x+vx*int(ht/2)), int(y+vy*int(ht/2))

        # boundary check
        x1 = x1 if x1 <= wd else x1 if x1 >= 0 else 0
        x2 = x2 if x2 <= wd else x2 if x2 >= 0 else 0
        y1 = y1 if y1 <= ht else y1 if y1 >= int(ht/2) else int(ht/2)
        y2 = y2 if y2 <= ht else y2 if y2 >= int(ht/2) else int(ht/2)
        return x1, y1, x2, y2

    def __find_angle(img, line, cfg):
        """ angle """
        x1, y1, x2, y2 = __find_from_to_xy(img, line, cfg)
        dx, dy = x2 - x1, y2 - y1
        angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
        return angle, x1, y1, x2, y2

    def __right_warning(img, (x1, x2), cfg):
        """ right side warning """
        wt, wd, dp = img.shape

        # only care about the horizont shift
        if len(cfg['sample']['right']['queue']) >= cfg['sample']['right']['size']:
            rt_std = np.std(cfg['sample']['right']['queue'])
            rt_mean = np.mean(cfg['sample']['right']['queue'])

            # warning if std is out of requirement
            if rt_std > cfg['sample']['right']['prestd'] + cfg['sample']['right']['stdoffset'] or rt_std < cfg['sample']['right']['prestd'] - cfg['sample']['right']['stdoffset']:
                cv2.putText(img, 'warning', (int(wt*3/4), int(wd/2)), cv2.FONT_HERSHEY_PLAIN, 2.0, cfg['color']['red'])

            cfg['sample']['right']['prestd'], cfg['sample']['right']['premean'] = rt_std, rt_mean
            cfg['sample']['right']['queue'].pop()

        cfg['sample']['right']['queue'].append((x1+x2)/2)
        return img

    def __left_warning(img, (x1, x2), cfg):
        """ left side warning """
        wt, wd, dp = img.shape

        # only care about the horizont shift
        if len(cfg['sample']['left']['queue']) >= cfg['sample']['left']['size']:
            lt_std = np.std(cfg['sample']['left']['queue'])
            lt_mean = np.mean(cfg['sample']['left']['queue'])

            # warning if std is out of requirement
            if lt_std > cfg['sample']['left']['prestd'] + cfg['sample']['left']['stdoffset'] or lt_std < cfg['sample']['left']['prestd'] - cfg['sample']['left']['stdoffset']:
                cv2.putText(img, 'warning', (int(wt*3/4), int(wd/2)), cv2.FONT_HERSHEY_PLAIN, 2.0, cfg['color']['red'])

            cfg['sample']['left']['prestd'], cfg['sample']['left']['premean'] = lt_std, lt_mean
            cfg['sample']['left']['queue'].pop()

        cfg['sample']['left']['queue'].append((x1+x2)/2)
        return img

    def _warning(img, lines, cfg):
        """ warning msg shows up when the crossing lane happened or std is out of requirement """
        for line in lines:
            angle, x1, y1, x2, y2 = __find_angle(img, line, cfg)
            if angle > 0:
                return __right_warning(img, (x1, x2), cfg)
            elif angle < 0:
                return __left_warning(img, (x1, x2), cfg)
        return img

    def _draw(img, lines, cfg):
        """ draw results """
        for line in lines:
            angle, x1, y1, x2, y2 = __find_angle(img, line, cfg)
            if angle <= cfg['filter']['angle'] and angle >= - cfg['filter']['angle']:
                return img
            cv2.line(img, (x1,y1), (x2,y2), cfg['color']['blue'], 2)
        return img

    def _show(img):
        """ show img """
        cv2.imshow('fitline', img)
        cv2.waitKey(1)

    def _debug_draw(thresh, lines, cfg):
        """ debug with draw """
        img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        ht, wd, dp = img.shape
        for line in lines:
            angle, x1, x2, y1, y2 = __find_angle(img, line, cfg)
            if angle <= cfg['filter']['angle'] and angle >= - cfg['filter']['angle']:
                return img
            cv2.line(img, (x1,y1), (x2,y2), cfg['color']['blue'], 2)
        return img

    def _debug_show(thresh):
        """ debug with show """
        cv2.imshow('debug_fitline', thresh)
        cv2.waitKey(1)

    # methods
    thresh = _prepare(img.copy(), cfg)
    lines = _detect(thresh, cfg)

    if cfg['set']['show'] not in [None, False]:
        img = _warning(img, lines, cfg)
        img = _draw(img, lines, cfg)
        _show(img)

    if cfg['set']['debug'] not in [None, False]:
        thresh = _debug_draw(thresh, lines, cfg)
        _debug_show(thresh)

    return img

