"""plots.py: Plotting functions and test plots.

<insert long description>.
"""
import cv2

def plotMatches(frame1,kp1,frame2,kp2,good,matchesMask):
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
    singlePointColor = None,
    matchesMask = matchesMask, # draw only inliers
    flags = 2) # do not draw single keypoints

    img3 = cv2.drawMatches(frame1,kp1,frame2,kp2,good,None,**draw_params)

    return img3
