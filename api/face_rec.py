
# https://z4spb7cvssd-496ff2e9c6d22116-8000-colab.googleusercontent.com/

# USAGE
# python recognize_faces_image.py --encodings encodings.pickle --image examples/bg1.JPG

# import the necessary packages
import face_recognition
import argparse
import pickle
import cv2
from PIL import Image as im
# import xlsxwriter


# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-e", "--encodings", required=True,
# 	help="path to serialized db of facial encodings")
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# ap.add_argument("-d", "--detection-method", type=str, default="hog",
# 	help="face detection model to use: either `hog` or `cnn`")
# args = vars(ap.parse_args())


# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open("/content/drive/MyDrive/Colab Notebooks/encodings_fyp.pickle", "rb").read())

# load the input image and convert it from BGR to RGB
image = cv2.imread("/content/drive/MyDrive/Colab Notebooks/myfoto_6ykp5mU.jpg")

##########################################################
  
# # Read the input image
# img = cv2.imread('bg1.JPG')
  
# Convert into grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt2.xml')
  
# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 4)


  
# Draw rectangle around the faces and crop the faces
images = []
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    faces = image[y:y + h, x:x + w]
    images.append(faces)
    cv2_imshow(faces)





#############################################
for image in images:
  # image = cv2.imread("/content/drive/MyDrive/Colab Notebooks/myfoto_0pFgl4S.jpg")
  rgb = image
  print("that",rgb)
  
  # detect the (x, y)-coordinates of the bounding boxes corresponding
  # to each face in the input image, then compute the facial embeddings for each face
  print("[INFO] recognizing faces...")
  boxes = face_recognition.face_locations(rgb,model="hog")
  encodings = face_recognition.face_encodings(rgb, boxes)

  # initialize the list of names for each face detected
  names = []

  # loop over the facial embeddings
  for encoding in encodings:
	  # attempt to match each face in the input image to our known encodings
	  matches = face_recognition.compare_faces(data["encodings"],encoding,tolerance=0.8)
	  name = "Unknown"

	  # check to see if we have found a match
	  if True in matches:
		  # find the indexes of all matched faces then initialize a
		  # dictionary to count the total number of times each face
		  # was matched
		  matchedIdxs = [i for (i, b) in enumerate(matches) if b]
		  counts = {}

		  # loop over the matched indexes and maintain a count for each recognized face face
		  for i in matchedIdxs:
			  name = data["names"][i]
			  counts[name] = counts.get(name, 0) + 1
       
		  # determine the recognized face with the largest number of
		  # votes (note: in the event of an unlikely tie Python will
		  # select first entry in the dictionary)
		  name = max(counts, key=counts.get)
	
	  # update the list of names
	  names.append(name)
 
	  # print(name)




  # # loop over the recognized faces
  # for ((top, right, bottom, left), name) in zip(boxes, names):
	#   # draw the predicted face name on the image
	#   cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
	#   y = top - 15 if top - 15 > 15 else top + 15
	#   cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
	# 	  0.75, (0, 255, 0), 2)
  print(name)
  # show the output image
  cv2_imshow(image)
  cv2.waitKey(0)