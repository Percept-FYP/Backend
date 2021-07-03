# USAGE
# python recognize_faces_image.py --encodings encodings.pickle --image examples/example_01.png

# import the necessary packages
import face_recognition
import argparse
import pickle
import cv2
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def func(img):
    # construct the argument parser and parse the arguments
    print(str(img))

    # load the known faces and embeddings
    print("[INFO] loading encodings...")
    data = pickle.loads(
        open(os.path.join(BASE_DIR, 'api/encodings_fyp.pickle'), "rb").read())

    # load the input image and convert it from BGR to RGB
    # image = cv2.imread(
    #     "D:/FYP/main/backend/_backend/static/images" + str(img) )
     if img != "":
        image = cv2.imread(
            os.path.join(BASE_DIR, 'static\\images\\')+str(img))
    else:
            image = cv2.imread(
            os.path.join(BASE_DIR, 'static\\images\\syed.png'))
    # image = cv2.imread(
    #     "D:/FYP/face-recognition-opencv/examples/bg1.jpg"  )

    # D:\FYP\face-recognition-opencv\examples

    # D:\FYP\main\backend\_backend\static\images\Images

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(
        rgb, model="cnn")
    encodings = face_recognition.face_encodings(rgb, boxes)

    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(
            data["encodings"], encoding, tolerance=0.5)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

    # show the output image

    # cv2.imshow("Image", image)
    cv2.waitKey(0)
    return names
