""" detect car speed """


def test():
    """ test lane detection """
    global gb_car_cfg
    capture = cv2.VideoCapture('data/road.avi')
    proc = {    'detect_car'      : detect_car
            }
    while True:
        ret, img = capture.read()
        proc[gb_car_cfg['set']['proc']](gb_car_cfg['set']['proc'], img, gb_car_cfg)


if __name__ == '__main__':
    test()
