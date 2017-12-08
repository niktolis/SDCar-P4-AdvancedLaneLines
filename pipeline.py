import matplotlib.image as mpimg
import glob
import os
from cal_camera import cal_getObjPointsImgPoints, cal_undistort
from color_grad import color_grad
from utils import show_images
import numpy as np

def pipeline():

    # The path with camera calibration images
    cal_img_path = './camera_cal/calibration*.jpg'
    # The path with the test images
    test_img_path = './test_images/*.jpg'

    # The first step is to calibrate the camera
    # I need to find the object points and image points on the given calibration images
    objpoints, imgpoints = cal_getObjPointsImgPoints(cal_img_path)

    #



    # Make a list of test images



    # Step through the list apply the color gradient to detect lines
    for fname in images:

        img = mpimg.imread(fname)
        result = color_grad(img, s_thresh=(150, 255), sx_thresh=(15, 100), DEBUG=True)


pipeline()
