
import cv2
import numpy as np

# lane config
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
            'angle'         : 20
            },

        'color' : {
            'green'         : (0, 255, 0),
            'blue'          : (255, 0, 0),
            'red'           : (0, 0, 255),
            'black'         : (0, 0, 0)
            },

        'set'   : {
            'proc'  :   'fitline',
            'show'  :   True,
            'debug' :   False
            }

        'sample': {
            'right' : {
                'queue'     : np.array(),
                'preavg'    : 0,
                'prestd'    : 0,
                'size'      : 4
                },
            'left'  : {
                'queue'     : np.array(),
                'preavg'    : 0,
                'prestd'    : 0,
                'size'      : 4
                },
            }
    }

gb_lane_cfg = LaneCfg


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

    def _waring(img, lines, cfg):
        """ waring msg shows up when the crossing lane happened """
        ht, wd, dp = img.shape

        def _right():
            if len(cfg['sample']['right']['queue']) >= cfg['sample']['right']['size']:
                np.std(cfg['sample']['right']['queue'])
            else:
                cfg['sample']['right']['queue'].append(angle)

        def _left():
            if len(cfg
        for line in lines:
            [vx, vy, x, y] = line


    def _draw(img, lines, cfg):
        """ draw results """
        ht, wd, dp = img.shape
        for line in lines:
            [vx, vy, x, y] = line
            # y = ax + b
            x1, y1 = int(x-vx*int(ht/2)), int(y-vy*int(ht/2))
            x2, y2 = int(x+vx*int(ht/2)), int(y+vy*int(ht/2))
            # boundary check
            x1 = x1 if x1 <= wd else wd
            x1 = x1 if x1 >= 0 else 0
            x2 = x2 if x2 <= wd else wd
            x2 = x2 if x2 >= 0 else 0
            y1 = y1 if y1 <= ht else ht
            y1 = y1 if y1 >= int(ht/2) else int(ht/2)
            y2 = y2 if y2 <= ht else ht
            y2 = y2 if y2 >= int(ht/2) else int(ht/2)
            dx, dy = x2 - x1, y2 - y1
            # filter out noise if the angle is out of range
            angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
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
            [vx, vy, x, y] = line
            # y = ax + b
            x1, y1 = int(x-vx*int(ht/2)), int(y-vy*int(ht/2))
            x2, y2 = int(x+vx*int(ht/2)), int(y+vy*int(ht/2))
            # boundary check
            x1 = x1 if x1 <= wd else wd
            x1 = x1 if x1 >= 0 else 0
            x2 = x2 if x2 <= wd else wd
            x2 = x2 if x2 >= 0 else 0
            y1 = y1 if y1 <= ht else ht
            y1 = y1 if y1 >= int(ht/2) else int(ht/2)
            y2 = y2 if y2 <= ht else ht
            y2 = y2 if y2 >= int(ht/2) else int(ht/2)
            dx, dy = x2 - x1, y2 - y1
            angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
            if angle <= cfg['filter']['angle'] and angle >= - cfg['filter']['angle']:
                return img
            cv2.line(img, (x1,y1), (x2,y2), cfg['color']['blue'], 2)
        return img

    def _debug_show(thresh):
        """ debug with show """
        cv2.imshow('debug_fitline', thresh)
        cv2.waitKey(1)

    thresh = _prepare(img.copy(), cfg)
    lines = _detect(thresh, cfg)

    if cfg['set']['show'] not in [None, False]:
        _draw(img, lines, cfg)
        _show(img)

    if cfg['set']['debug'] not in [None, False]:
        thresh = _debug_draw(thresh, lines, cfg)
        _debug_show(thresh)

    return img


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

    edge = _prepare(img.copy(), cfg)
    lines = _detect(edge, cfg)

    if cfg['set']['show'] not in [None, Fasle]:
        img = _draw(img, lines, cfg)
        _show(img)

    if cfg['set']['debug'] not in [None, Fasle]:
        edge = _debug_draw(edge, lines, cfg)
        _debug_show(edge)

    return img


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

    def _draw(img, lines, cfg):
        """ draw results """
        for line in lines:
            for obj in line:
                [rho, theta] = obj
                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho
                # y = ax + b
                x1, y1 = int(x0 + 1000*(-b)), int(y0 + 1000*(a))
                x2, y2 = int(y0 - 1000*(-b)), int(y0 - 1000*(a))
                dx, dy = x2 - x1, y2 - y1
                # boundary check
                x1 = x1 if x1 <= wd else wd
                x1 = x1 if x1 >= 0 else 0
                x2 = x2 if x2 <= wd else wd
                x2 = x2 if x2 >= 0 else 0
                y1 = y1 if y1 <= ht else ht
                y1 = y1 if y1 >= int(ht/2) else int(ht/2)
                y2 = y2 if y2 <= ht else ht
                y2 = y2 if y2 >= int(ht/2) else int(ht/2)
                dx, dy = x2 - x1, y2 - y1
                angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
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
                [rho, theta] = obj
                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho
                # y = ax + b
                x1, y1 = int(x0 + 1000*(-b)), int(y0 + 1000*(a))
                x2, y2 = int(y0 - 1000*(-b)), int(y0 - 1000*(a))
                dx, dy = x2 - x1, y2 - y1
                # boundary check
                x1 = x1 if x1 <= wd else wd
                x1 = x1 if x1 >= 0 else 0
                x2 = x2 if x2 <= wd else wd
                x2 = x2 if x2 >= 0 else 0
                y1 = y1 if y1 <= ht else ht
                y1 = y1 if y1 >= int(ht/2) else int(ht/2)
                y2 = y2 if y2 <= ht else ht
                y2 = y2 if y2 >= int(ht/2) else int(ht/2)
                dx, dy = x2 - x1, y2 - y1
                angle = np.arctan2(dy, dx) * cfg['filter']['invtheta']
                if angle <= cfg['filter']['angle'] and angle >= - cfg['filter']['angle']:
                    return img
                cv2.line(img, (x1,y1), (x2,y2), cfg['color']['blue'], 2)
        return img

    def _debug_show(edge):
        cv2.imshow('houghlines_edge', edge)
        cv2.waitKey(1)

    edge = _prepare(img.copy(), cfg)
    lines = _detect(edge, cfg)

    if cfg['set']['show'] not in [None, False]:
        img = _draw(img, lines, cfg)
        _show(img)

    if cfg['set']['debug'] not in [None, False]:
        edge = _debug_draw(edge, lines, cfg)
        _debug_show(edge)

    return img


def test():
    """ test lane detection """
    global gb_lane_cfg
    capture = cv2.VideoCapture('data/road.avi')
    proc = {    'fitline'      : detect_lane_over_fitline,
                'houghlinesP'   : detect_lane_over_houghlinesP,
                'houghlines'    : detect_lane_over_houghlines
            }
    while True:
        ret, img = capture.read()
        proc[gb_lane_cfg['set']['proc']](gb_lane_cfg['set']['proc'], img, gb_lane_cfg)


if __name__ == '__main__':
    test()
