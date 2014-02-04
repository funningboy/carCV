
import cv2
import numpy as np


LaneCfg = {

        'canny'     : {
            'threshold1'    : 1,
            'threshold2'    : 200,
            'apertureSize'  : 3
            },

        'gaussian'  : {
            'ksize'         : (5, 5),
            'border'        : 3
            },

        'houghlinesp' : {
            'rho'           : 1,
            'theta'         : np.pi/180,
            'threshold'     : 100,
            'minlinelength' : 1,
            'maxlinegap'    : 10
            },

        'houghlines' : {
            'rho'           : 1,
            'theta'         : np.pi/180,
            'threshold'     : 100
            },

        'threshold' : {
            'threshold1'    : 200,
            'threshold2'    : 255
            },

        'filter'    :   {
            'invtheta'      : 180 / np.pi,
            'angle'         : 20,
            'green'         : (255, 0, 0),
            'blue'          : (0, 255, 0),
            'black'         : (0, 0, 0)
            }
    }

gb_lane_cfg = LaneCfg

def update_lane():
    """ update lane cfg """
    pass

def detect_lane_over_fitline(name, img, cfg):

    def _prepare(img, cfg):
        ht, wd, dp = img.shape
         # only care about the horizont block, filter out up high block
        img[0:int(ht/2),:] = cfg['filter']['black']
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        return thresh

    def _detect(thresh, cfg):
        contours, hier = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if contours is None:
            return []
        return [cv2.fitLine(cnt,cv2.cv.CV_DIST_L2,0,0.01,0.01) for cnt in contours]

    def _draw(img, lines, cfg):
        ht, wd, dp = img.shape
        for line in lines:
            [vx, vy, x, y] = line
            # y = ax + b
            x1, y1 = int(x-vx*int(ht/2)), int(y-vy*int(ht/2))
            x2, y2 = int(x+vx*int(ht/2)), int(y+vy*int(ht/2))
            dx, dy = x2 - x1, y2 - y1
            angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
            if angle <= cfg['filter']['angle'] and angle >= - cfg['filter']['angle']:
                return img
            cv2.line(img, (x1,y1), (x2,y2), cfg['filter']['blue'], 2)
        return img

    def _show(img):
        cv2.imshow('fitline', img)
        cv2.waitKey(1)

    def _debug_draw(thresh, lines, cfg):
        if len(lines) > 0:
            [vx, vy, x, y] = lines
            # y = ax + b
            x1, y1 = int(x-vx*1000), int(y-vy*1000)
            x2, y2 = int(x+vx*1000), int(y+vy*1000)
            dx, dy = x2 - x1, y2 - y1
            angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
            if angle <= cfg['filter']['angle'] and angle >= - cfg['filter']['angle']:
                return thresh
            cv2.line(thresh, (x1,y1), (x2,y2), cfg['filter']['blue'], 2)
        return thresh

    def _debug_show(thresh):
        cv2.imshow('debug_fitline', thresh)
        cv2.waitKey(1)

    thresh = _prepare(img, cfg)
    lines = _detect(thresh, cfg)
    _draw(img, lines, cfg)
    _show(img)

#    thresh = _debug_draw(thresh, lines, cfg)
#    _debug_show(thresh)

def detect_lane_over_houghlinesP(name, img, cfg):

    def _prepare(img, cfg):
        """ prepare proc for edge collection """
        ht, wd, dp = img.shape
        # only care about the horizont block, filter out up high block
        img[0:int(ht/2),:] = cfg['filter']['black']
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
                cv2.line(img, (x1,y1), (x2,y2), cfg['filter']['green'], 2)
        return img

    def _show(img):
        cv2.imshow('houghlinesP_img', img)
        cv2.waitKey(1)

    def _debug_draw(edge, lines, cfg):
        for line in lines:
            for obj in line:
                [x1, y1, x2, y2] = obj
                dx, dy = x2 - x1, y2 - y1
                angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
                if angle <= cfg['filter']['angle']  and angle >= - cfg['filter']['angle']:
                    return edge
                cv2.line(edge, (x1,y1), (x2,y2), cfg['filter']['green'], 2)
        return edge

    def _debug_show(edge):
        cv2.imshow('houghlinesP_edge', edge)
        cv2.waitKey(1)

    edge = _prepare(img, cfg)
    lines = _detect(edge, cfg)
    img = _draw(img, lines, cfg)
    _show(img)

    edge = _debug_draw(edge, lines, cfg)
    _debug_show(edge)


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
        img[0:int(ht/2),:] = cfg['filter']['black']
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

    def _draw(img, lines, cfg):
        for line in lines:
            for obj in line:
                [rho, theta] = obj
                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho
                # y = ax + b
                x1, y1 = int(x0 + 1000*(-b)), int(y0 + 1000*(a))
                x2, y2 = int(y0 - 1000*(-b)), int(y0 - 1000*(a))
                dx, dy = x2 - x1, y2 - y1
                angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
                if angle <= cfg['filter']['angle'] and angle >= - cfg['filter']['angle']:
                    return img
                cv2.line(img, (x1,y1), (x2,y2), cfg['filter']['blue'], 2)
        return img

    def _show(img):
        cv2.imshow('houghlines_img', img)
        cv2.waitKey(1)

    def _debug_show(edge, lines, cfg):
        cv2.imshow('houghlines_edge', edge)
        cv2.waitKey(1)

    edge = _prepare(img, cfg)
    lines = _detect(edge, cfg)
    img = _draw(img, lines, cfg)

    _show(img)
    _debug_show(edge, lines, cfg)


def test():
    """ test lane detection """
    global gb_lane_cfg
    capture = cv2.VideoCapture('data/road.avi')
    while True:
        ret, img = capture.read()
        detect_lane_over_fitline('lane', img, gb_lane_cfg)
        #detect_lane_over_houghlinesP('lane', img, gb_lane_cfg)
        #detect_lane_over_houghlines('lane', img, gb_lane_cfg)



if __name__ == '__main__':
    test()
