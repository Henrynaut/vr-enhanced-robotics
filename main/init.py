"""init.py: Initialize parameters.

Print initialization text and set general parameters for the program.
Define support functions.
"""
import cv2

def endProgram(video1, video2):
    print "Releasing input files..."
    video1.release()
    video2.release()
    cv2.destroyAllWindows()
    print "*** End of Program ***"

def videoInfo(inputVideo):
    inputWidth = int(inputVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
    inputHeight = int(inputVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    inputFrames = int(inputVideo.get(cv2.CAP_PROP_FRAME_COUNT))
    inputFPS = int(inputVideo.get(cv2.CAP_PROP_FPS))

    print ("Width: %i pixels" % inputWidth)
    print ("Height: %i pixels" % inputHeight)
    print ("Frame count: %i frames" % inputFrames)
    print ("FPS: %i Hz \n" % inputFPS)
    return

def greeting():
    print " "
    print "*** Welcome to <insert project name> ***\n", \
        "Prototype version: ", \
        "Video inputs are two different camera views captured using EDGE/NASA"
    print " "
    return

def hacks():
    """
    FIX (aka, hack)
    Need to disable OpenCL support to match features using knnMatch and ORB
    when you have OpenCV 3.1
    https://github.com/Itseez/opencv/issues/6055
    """
    cv2.ocl.setUseOpenCL(False)
    return

def init():
    greeting()
    hacks()
    return
