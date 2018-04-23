# Flann Matching with ORB Descriptors
# Vinicius Goecks - Mar. 2016
# Video source: EDGE Software - NASA
# --------------------------------------------------------------------------- #

# Import required libraries and modules
import numpy as np
import cv2
from matplotlib import pyplot as plt
import timeit
import os

# FIX (aka, hack)
# Need to disable OpenCL support to match features using knnMatch and ORB
# when you have OpenCV 3.1
# https://github.com/Itseez/opencv/issues/6055
cv2.ocl.setUseOpenCL(False)

# --------------------------------------------------------------------------- #
## PARAMETERS

# Define number of minimum matches desired
MIN_MATCH_COUNT = 10

# --------------------------------------------------------------------------- #
## MAIN

# *** DO NOT FORGET THE STUFF ABOUT FUNDAMENTAL MATRIX

# Start counting running time
start = timeit.default_timer()

# Import input videos
baseFolder = '/home/vinicius/Projects/nasa-vr-robotics/'
video1 = cv2.VideoCapture(baseFolder + 'edgeEditVideoData/cp_7_edit.m4v')
video2 = cv2.VideoCapture(baseFolder + 'edgeEditVideoData/cp_9_edit.m4v')

video1_frameCount = int(video1.get(cv2.CAP_PROP_FRAME_COUNT))
video2_frameCount = int(video2.get(cv2.CAP_PROP_FRAME_COUNT))

print ("Video 1 frame count: %i frames" % video1_frameCount)
print ("Video 2 frame count: %i frames" % video2_frameCount)

while(True):

    # Capture frame-by-frame
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Initiate ORB detector
    # ORB - Oriented FAST and Rotated BRIEF
    #   ORB is basically a fusion of FAST keypoint detector and
    #   BRIEF descriptor with many modifications to enhance the performance.
    orb = cv2.ORB_create()

    # Find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(frame1,None)
    kp2, des2 = orb.detectAndCompute(frame2,None)

    # FLANN Matcher
    # FLANN - Fast Approximate Nearest Neighbor Search
    #   FLANN is a library for performing fast approximate nearest neighbor
    #   searches in high dimensional spaces. Also, automatically choosing
    #   the best algorithm and optimum parameters depending on the dataset.

    # FLANN parameters while using ORB
    #   FLANN Index parameters
    #       # algorithm: FLANN_INDEX_LSH (number 6)
    #       # table_number: number of hash tables to use (10~30)
    #       # key_size: size of hash keys in bits (10~20)
    #       # multi_probe_level: number of bits to shift to check for neighboring
    #                            buckets (0 is regular LSH, 2 is recommended)
    FLANN_INDEX_LSH = 6
    index_params= dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 6,
                       key_size = 12,
                       multi_probe_level = 1)

    # FLANN Search parameters
    #   checks: number of times the trees in the index should be recursively
    #           traversed. Higher values gives better precision, but also takes
    #           more time.
    search_params = dict(checks = 50)

    # Call FLANN based on the above parameters and store matches
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Find matches:
    #   # des1: query descriptors
    #   # des2: train descriptors
    #   # k: count of best matches
    matches = flann.knnMatch(des1,des2,k=2)

    # Store all the good matches as per Lowe's ratio test.
    good = []
    for m_n in matches:
        if len(m_n) != 2:
            continue
        (m,n) = m_n
        if m.distance < 0.7*n.distance:
            good.append(m)

    # Filter good matches using RANSAC (if we have more matches than the minimun)
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        # print M

        h,w = frame1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        frame2 = cv2.polylines(frame2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
        matchesMask = None

    # Define parameters and draw matches
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
    singlePointColor = None,
    matchesMask = matchesMask, # draw only inliers
    flags = 2) # do not draw single keypoints

    img3 = cv2.drawMatches(frame1,kp1,frame2,kp2,good,None,**draw_params)

    # Plot images with matched features
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image",img3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the captures
video1.release()
video2.release()
cv2.destroyAllWindows()

# Stop counting running time
stop = timeit.default_timer()
total_time = stop - start
print('Time elapsed: %f seconds.' %total_time)
