## purpose
car and lane detection example

[![ScreenShot](https://raw.github.com/funningboy/carCV/master/img/result.png)](http://youtu.be/5SPXba1lwIU)

##method
-lane detection
  - houghlines
  - houghlinesP
  - fitlines

-car detection
  - haar cascades

##how to run it?
step1. get video source
`%python get_video.py`

step2. lane detection
`%python detect_lane.py`

step3. car detection
`%python detect_car.py`

Ref
- using color segmentation/background subtraction
  http://www.prodigyproductionsllc.com/articles/programming/lane-detection-with-opencv-and-c/

- car lane detection
http://code.google.com/p/opencv-lane-vehicle-track/source/browse/trunk/main.cpp

- circle and line detection
https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html

-contour features
https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html
Lane Detection as (line detection)
