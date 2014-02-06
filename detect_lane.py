from detect_lane_houghlines import *
from detect_lane_fitline import *
from detect_lane_houghlinesP import *
from config_lane import *

gb_lane_cfg = LaneCfg

def test():
    """ test lane detection """
    global gb_lane_cfg

    capture = cv2.VideoCapture('data/road.avi')

    # register to proc manager
    proc = {    'fitline'      : detect_lane_over_fitline,
                'houghlinesP'   : detect_lane_over_houghlinesP,
                'houghlines'    : detect_lane_over_houghlines
            }

    while True:
        ret, img = capture.read()
        proc[gb_lane_cfg['set']['proc']](gb_lane_cfg['set']['proc'], img, gb_lane_cfg)

if __name__ == '__main__':
    test()
