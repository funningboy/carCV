
import cv2
import numpy as np

gb_cascade = None

def detect_car(name, img):
    """ detect car """

    global gb_cascade

    scale = 2
    scale_factor = 1.05
    min_neighbors = 2

    def _train_data(cascade_fn='data/haarcascade_cars3.xml'):
        """ training data """
        cascade = cv2.CascadeClassifier(cascade_fn)
        return cascade

    def _prepare(img, scale=2.0):
        """ prepare analysis proc for alg input """
        ht, wd, dp = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 3)
        gray = cv2.resize(gray, (np.int32(np.around(ht/scale)), np.int32(np.around(wd/scale))), interpolation = cv2.INTER_LINEAR)
        gray = cv2.equalizeHist(gray)
        return gray

    def _factor(img, gray):
        """ caculate the resize factor """
        ht, wd = float(img.shape[0]) / gray.shape[0], float(img.shape[1]) / gray.shape[1]
        return (ht, wd)

    def _detect(gray, cascade, factor=(), scale_factor=1.05, min_neighbors=2):
        """ haarcascascade alg to find target obj """
        rects = cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        for i in [0, 2]:
            rects[:,i] = np.int32(np.around(rects[:,i] * factor[1]))
        for i in [1, 3]:
            rects[:,i] = np.int32(np.around(rects[:,i] * factor[0]))
        rects[:,2:] += rects[:,:2]
        return rects

    def _draw_rects(img, rects, color):
        """ draw results """
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        return img

    if gb_cascade == None:
        gb_cascade = _train_data(cascade_fn='data/haarcascade_cars3.xml')

    gray = _prepare(img, scale)
    factor = _factor(img, gray)
    rects = _detect(gray, gb_cascade, factor, scale_factor, min_neighbors)
    _draw_rects(img, rects, (0, 255, 0))
    return name, img


def detect_lane(name, img):
    """ detect lane """

    def _prepare(img):
        pass

    def _detect():
        pass

    def _draw_lines():
        pass

def test():

    capture = cv2.VideoCapture('data/road.avi')
    while True:
        ret, img = capture.read()
        name, img = detect_car('car', img)
        name, img = detect_lane('lane', img)
        cv2.imshow('tesy', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    test()
