
CarCfg = {

    'gaussian'  :   {
        'ksize'     : (5, 5),
        'border'    : 3
        },

    'cascade'   :   {
        'train_ptr'     : None,
        'train_data'    : 'data/haarcascade_cars3.xml',
        'scale_factor'  : 1.05,
        'min_neighbors' : 2
        },

    'set'   :   {
        'resize'        : 0.5,
        'proc'          : 'detect_car',
        'debug'         : False,
        'show'          : True
        },

    'color' : {
        'green'         : (0, 255, 0),
        'blue'          : (255, 0, 0),
        'red'           : (0, 0, 255),
        'black'         : (0, 0, 0)
        }
    }


