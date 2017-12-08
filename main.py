import matplotlib.pyplot as plt
import cv2

DebugFlag=[False,False]

print(DebugFlag[0], DebugFlag[1])

from cal_camera import cal_getObjPointsImgPoints, cal_undistort

objpoints, imgpoints = cal_getObjPointsImgPoints('./camera_cal/calibration*.jpg', DEBUG=DebugFlag[0])

img = cv2.imread('./camera_cal/calibration1.jpg')
undist_img = cal_undistort(img, objpoints, imgpoints, DEBUG=DebugFlag[1])
