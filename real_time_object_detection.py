# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from imutils.video import VideoStream 
from imutils.video import FPS
import cv2
import numpy as np
import argparse
import imutils
import time
import sys
sys.path.append("C:\Users\Raza\Downloads\asd\AR.drone-master\windowsARdrone\libardrone")
from FoxDemo2 import *


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
#vs = VideoStream(src = 0).start()

foo = ShowImages()
#foo.userKeyResponse('u')
foo.userKeyResponse(' ')
#foo.userKeyResponse('1')
#time.sleep(2.0)
#fps = FPS().start()
count = 0
k = 1
#Area_f=0
#Area = 0
#X_current = 0
#X_next = 0
#ith_frame = 1

def goto(linenum):
    global line
    line = linenum
    
def track():
     if (Area_f  > Area_frame   ):
                
                dir = "moving backward"
                foo.userKeyResponse('s')
                track_left_right()

                label_1 = label + dir
                goto(20)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                
                cv2.putText(frame, label_1 , (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                

     elif (Area_f  < (Area_frame - 3000) ):
                
                dir = "moving forward"
                foo.userKeyResponse('w')
                track_left_right()
                label_1 = label + dir
                goto(20)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                print Area_f
                cv2.putText(frame, label_1 , (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                

     else:
                foo.userKeyResponse('h')
                track_left_right()
                dir = "Not moving"
                label_1 = label + dir
                goto(20)
                y = startY - 15 if startY - 15 > 15 else startY + 15
 
                cv2.putText(frame, label_1 , (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                

def track_left_right():
    if ( (centroid_X - 35) > ((startX + endX)/2)):
          dir = "Left"
          foo.userKeyResponse('j')
          cen_box  = ((startX + endX)/2)
          label = "{}: {:.2f}%".format(CLASSES[idx],
          confidence * 100)

          label_2 = label + dir
          goto(22)
          y = startY - 15 if startY - 15 > 15 else startY + 15
 
          cv2.putText(frame, label_2 , (startX, y),
          cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
          
          #foo.userKeyResponse('3')
          

    elif ((centroid_X + 35) < ((startX + endX)/2)):
          dir = "Right"
          foo.userKeyResponse('l')
          cen_box  = ((startX + endX)/2)
          
          label = "{}: {:.2f}%".format(CLASSES[idx],
          confidence * 100)

          label_2 = label + dir
          goto(22)
          y = startY - 15 if startY - 15 > 15 else startY + 15
 
          cv2.putText(frame, label_2 , (startX, y),
          cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
          
          #foo.userKeyResponse('3')
          
    else:
          if ((Area_f  > (Area_frame + 500)) or (Area_f  < (Area_frame + 500))  ):
              print("")
          else:
              #print("not moving")
              foo.userKeyResponse('h')
                                        
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	

	count = count + 1
	
        # RAza's changes
        frame = foo.nextPicture() 
	

	#print("Frames ",frame)
	
	#ith_frame = ith_frame + 1
	frame = imutils.resize(frame, width=400)

	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	centroid_X = w/2
        Area = h * w
        Area_frame = Area / 4
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	# pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()

	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			idx = int(detections[0, 0, i, 1])
			
			if (idx == 15):
                                if (count == 1):
                                         box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                                         (startX, startY, endX, endY) = box.astype("int")

                                         x_cordinate = [startX,endX]
                                         y_cordinate = [startY,endY]
                                         X_current = startX
                                        
                                         label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
        
                                         cv2.rectangle(frame, (startX, startY), (endX, endY),
                                         COLORS[idx], 2)
                                         y = startY - 15 if startY - 15 > 15 else startY + 15
                                         cv2.putText(frame, label, (startX, y),
                                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                                         width_f = endX - startX
                                         height_f = endY - startY
                                         Area_f = height_f * width_f 
                                         
                                         track()
                                         track_left_right()
                                         


                                

                                        
                                
                                        
                               
                                        
                                       
                                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                                (startX, startY, endX, endY) = box.astype("int")
                                x_cordinate = [startX,endX]
                                width_f = endX - startX
                                height_f = endY - startY
                                Area_f = height_f * width_f
                            
                               
                    
                                label = "{}: {:.2f}%".format(CLASSES[idx],
                                confidence * 100)
            
                                cv2.rectangle(frame, (startX, startY), (endX, endY),
                                COLORS[idx], 2)
                                y = startY - 15 if startY - 15 > 15 else startY + 15
                                cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                                
                                track()
                                track_left_right()
                                
			

	# show the output frame
	cv2.imshow("Frame", frame)
					
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	#fps.update()

# stop the timer and display FPS information
#fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
#vs.stop()
