import cv2
import imutils
import argparse

# Define available arguments
arguments = argparse.ArgumentParser()
arguments.add_argument("-v", "--video", help="Path to video")
arguments.add_argument("-a", "--min-area", type=int, default=500, help="Minimum area")

# Get supplied args
args = vars(arguments.parse_args())

# this will use a webcam if theres no video
if args.get("video", None) is None:
	# cv2.VideoCapture(1) would return the next device if it exists
	camera = cv2.VideoCapture(0)
else:
	camera = cv2.VideoCapture(args["video"])

# to compare frames
thefirstFrame = None

# will continue to loop 
while True:
	# Read the next frame
	(success, frame) = camera.read()
	
	# if it cant read the frame
	if not success:
		break

	# Resize, convert to grayscale, and blur the frame
	frame = imutils.resize(frame, width=600)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# Store the first frame
	if thefirstFrame is None:
		thefirstFrame = gray
		continue

	# Get the delta of the first & current frame
	#	 https://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#absdiff
	delta = cv2.absdiff(firstFrame, gray)

	# Apply a binary threshold to the frame 
	# 	https://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html
	threshold = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]

	# Dilate the threshold 
	# 	https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html#dilation
	threshold = cv2.dilate(threshold, None, iterations=2)
	
	# looks for contours in the image
	# 	https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#findcontours
	(_, contours, _) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


	# Loop through contours
	for contour in contours:	
		# Skip if the contour area is less than the minimum
		if cv2.contourArea(contour) < args["min_area"]:
			continue

		# makes that bounding rectangle 
		(x, y, w, h) = cv2.boundingRect(contour)
		
		# Draw the rectanngle over the frame
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


	# Display 
	cv2.imshow("Video", frame)
	cv2.imshow("Threshold", threshold)
	cv2.imshow("Frame Delta", delta)
	
	# Wait 1 millisecond to see if user presses key
	key = cv2.waitKey(1) & 0xFF

	# and then Break if the user presses q
	if key == ord("q"):
		break

# Close windows
cv2.destroyAllWindows()

# Release camera
camera.release()

#python cameramotiondetection.py --video videos/video name