#! /usr/bin/env python
"""main.py: The main file. The one that make it happen.

<insert long description here>
"""

__author__ = "Vinicius Guimaraes Goecks"
__copyright__ = "TBD"
__credits__ = ["Stoian Borissov", "Austin Probe", "Gregory Chamitoff"]
__license__ = "TBD"
__version__ = "0.0"
__maintainer__ = "Vinicius Guimaraes Goecks"
__email__ = "vinicius.goecks@tamu.edu"
__status__ = "Prototype"
__date__ = "May/2016"

# import modules
import sys                      # system module for cool stuff
import timeit                   # measure running time
import matplotlib.pyplot as plt # plotting
from init import *              # initialization and parameters file
from help_file import *         # help file for this project
from feature_detection import * # feature detection parameters
from plots import *             # plotting functions

# check for correct usage
if len(sys.argv) != 3:
    helpFunction()          # for usage help
    sys.exit()

# initialize program
init()
video1 = cv2.VideoCapture(sys.argv[1])
video2 = cv2.VideoCapture(sys.argv[2])

# source info
print "* Video1 *"
videoInfo(video1)
print "* Video2 *"
videoInfo(video2)

# initialize ORB detector and FLANN feature matcher
orb = cv2.ORB_create()
flann = flannStart()

# main loop
iterations = 0
while(True):

    # Capture frame-by-frame
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    # check if reached the end of input files
    if (ret1 == False) or (ret2 == False):
        print "End of input files."
        break
    else:
        # start counting running time and iterations
        start = timeit.default_timer()
        print "Iteration #", iterations

        # call ORB detector
        kp1, kp2, des1, des2, frame1, frame2 = orbUpdate(orb, frame1, frame2)

        # find matches with flann
        #   k: count of best matches
        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test
        good = lowesRatioTest(matches)

        # filter good matches using RANSAC (if have more matches than minimun)
        M, matchesMask = ransacGoodMatches(good, frame1, frame2, kp1, kp2)

        # draw matches
        output = plotMatches(frame1,kp1,frame2,kp2,good,matchesMask)

        # plot images with matched features
        cv2.namedWindow("output", cv2.WINDOW_NORMAL)
        cv2.imshow("output",output)

        # press q to abort
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # stop counting running time and add iteration
        stop = timeit.default_timer()
        iterations += 1
        print('Time elapsed: %f seconds. \n' %(stop - start))

# release videos and close windows
endProgram(video1, video2)
