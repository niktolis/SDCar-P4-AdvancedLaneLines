import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def cal_getObjPointsImgPoints(cal_img_path, x=9, y=6, DEBUG=False):

    # prepare object imgpoints
    objp = np.zeros((x*y, 3), np.float32)
    objp[:,:2] = np.mgrid[0:x, 0:y].T.reshape(-1, 2)

    # Arrays to store object points and image image points
    objpoints = [] # 3D points in real world space
    imgpoints = [] # 2D points in image plane

    # Make a list of calibration images
    images = glob.glob(cal_img_path)

    # Step through the list and search for chessboard corners
    for fname in images:

        img = mpimg.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Find chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (x, y), None)

        # If found, add object points and image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Draw and display the corners
            if DEBUG == True:
                img = cv2.drawChessboardCorners(img, (x, y), corners, ret)
                print(fname)
                imagename = fname.split("calibration")[-1]
                imagename = 'chessboard'+imagename
                print(imagename)
                cv2.imshow(imagename,img)
                # Save images for the report
                cv2.imwrite(os.path.join('./output_images/calibration_output/',imagename), img)
                cv2.waitKey(500)

    cv2.destroyAllWindows()

    # Return ret and corners the object points and image points
    return objpoints, imgpoints

def cal_undistort(img, objpoints, imgpoints):

    # Change to grayscale color space
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # calibrate camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    # undistort image
    undist_img = cv2.undistort(img, mtx, dist, None, mtx)

    if DEBUG == True:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))
        f.tight_layout()
        ax1.imshow(img)
        ax1.set_title('Original Image', fontsize=50)
        ax2.imshow(undist_img)
        ax2.set_title('Undistorted Image', fontsize=50)
        plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
        plt.show()

    return ret, mtx, dist, rvecs, tvecs, undist_img
