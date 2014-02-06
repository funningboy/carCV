
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
            },

        'sample': {
            'right' : {
                'queue'     : [],
                'premean'   : 0,
                'prestd'    : 0,
                'size'      : 4,
                'stdoffset' : 100
                },
            'left'  : {
                'queue'     : [],
                'premean'   : 0,
                'prestd'    : 0,
                'size'      : 4,
                'stdoffset' : 100
                },
            }
    }


