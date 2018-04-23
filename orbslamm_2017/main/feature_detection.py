"""feature_detection.py: Parameters and functions for feature detection.

Here you will be able to define and set parameters for the ORB descriptor and
FLANN feature matching.
"""
import cv2
import numpy as np

def orbUpdate(orb, frame1, frame2):
    """
    Initiate ORB detector
    ORB - Oriented FAST and Rotated BRIEF
        ORB is basically a fusion of FAST keypoint detector and
        BRIEF descriptor with many modifications to enhance the performance.

    Find the keypoints and descriptors with ORB
    """
    # need to be grayscale to use ORB
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    kp1, des1 = orb.detectAndCompute(frame1, None)
    kp2, des2 = orb.detectAndCompute(frame2, None)
    return kp1, kp2, des1, des2, frame1, frame2

def flannStart():
    """
    FLANN Matcher
    FLANN - Fast Approximate Nearest Neighbor Search
      FLANN is a library for performing fast approximate nearest neighbor
      searches in high dimensional spaces. Also, automatically choosing
      the best algorithm and optimum parameters depending on the dataset.

    FLANN parameters while using ORB
      FLANN Index parameters
          # algorithm: FLANN_INDEX_LSH (number 6)
          # table_number: number of hash tables to use (10~30)
          # key_size: size of hash keys in bits (10~20)
          # multi_probe_level: number of bits to shift to check for neighboring
                               buckets (0 is regular LSH, 2 is recommended)
    """
    FLANN_INDEX_LSH = 6
    index_params= dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 6,
                       key_size = 12,
                       multi_probe_level = 1)

    """
    FLANN Search parameters
      checks: number of times the trees in the index should be recursively
              traversed. Higher values gives better precision, but also takes
              more time.
    """
    search_params = dict(checks = 50)

    # Call FLANN based on the above parameters and store matches
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    return flann

def lowesRatioTest(matches):
    good = []
    ratioValue = 0.7
    for m_n in matches:
        if len(m_n) != 2:
            continue
        (m,n) = m_n
        if m.distance < ratioValue*n.distance:
            good.append(m)

    return good

def ransacGoodMatches(good, frame1, frame2, kp1, kp2):
    """
    Filter good matches using RANSAC (if we have more matches than the minimun)
    """
    # Define number of minimum matches desired
    MIN_MATCH_COUNT = 10

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        # print M

        h,w = frame1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        #frame2 = cv2.polylines(frame2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        matchesMask = None
        M = np.zeros((3,3))
        print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
        print "M = ", M

    return M, matchesMask
