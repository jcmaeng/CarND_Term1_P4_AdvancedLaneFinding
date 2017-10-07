import os
import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
#%matplotlib win32

##### Functions
def cal_undistort(src_img, obj_points, img_points):
    # Use cv2.calibrateCamera() and cv2.undistort()
    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1],None,None)
    undist = cv2.undistort(src_img, mtx, dist, None, mtx)
    return undist

def find_chessboard_corners(src_img, cshape):
    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    return cv2.findChessboardCorners(gray, cshape, None)

##### Main Procedure

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
nx = 9
ny = 5
objp = np.zeros((ny*nx,3), np.float32)
objp[:,:2] = np.mgrid[0:nx,0:ny].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane.

# read image from file
img = cv2.imread('.\\camera_cal\\calibration1.jpg')

# Find the chessboard corners
ret, corners = find_chessboard_corners(img, (nx,ny))
# print("ret=", ret)
# print("corners=", corners)

if ret is False:
    print("find chessboard corners failed!!")
    os.exit()

objpoints.append(objp)
imgpoints.append(corners)

undistorted = cal_undistort(img, objpoints, imgpoints)

# save output result of camera calibration and image undistortion
cv2.imwrite('./output_images/cal1-undistorted.jpg', undistorted)

ret, corners2 = find_chessboard_corners(undistorted, (nx,ny))
if ret is False:
    print("find chessboard corners failed!!")
    os.exit()

# Draw and display the corners
undistorted_drawn = undistorted.copy()
cv2.drawChessboardCorners(undistorted_drawn, (nx,ny), corners2, ret)

offset = 60
img_size = (undistorted.shape[1], undistorted.shape[0])
src_p = np.float32([corners2[0], corners2[nx-1], corners2[-1], corners2[-nx]])
dst_p = np.float32([[offset,offset], [img_size[0]-offset, offset], [img_size[0]-offset, img_size[1]-offset], [offset, img_size[1]-offset]])
M = cv2.getPerspectiveTransform(src_p, dst_p)
warped = cv2.warpPerspective(undistorted, M, img_size)

# save output result of warp perspective
cv2.imwrite('./output_images/cal1-warped.jpg', warped)

cv2.imshow('warped',warped)
cv2.waitKey()

cv2.destroyAllWindows()