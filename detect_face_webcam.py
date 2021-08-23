import warnings #we don't like warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
import imutils
from keras import models
from keras.preprocessing.image import img_to_array
import tensorflow as tf
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import np

def face_webcam(nume):
    nume2 = nume
    model = models.load_model("./_mini_XCEPTION.102-0.66.hdf5")
    cascName = 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascName)
    emotion_dict= ["Angry" ,"Disgust","Scared", "Happy", "Sad", "Surprised","Neutral"]


    cv2.namedWindow("Webcam",cv2.WINDOW_KEEPRATIO)
    vidcapt = cv2.VideoCapture(0)

    if vidcapt.isOpened(): # try to get the first frame
       rval, frame = vidcapt.read()
    else:
       rval = False

    while rval:

       cv2.namedWindow("Webcam",cv2.WINDOW_KEEPRATIO)
       cv2.imshow("Webcam", frame)
       #cv2.setWindowProperty('Webcam',cv2.WND_PROP_ASPECT_RATIO,cv2.WINDOW_KEEPRATIO)
       # Capture frame-by-frame
       rval, frame = vidcapt.read()
       image = frame
       frame = imutils.resize(frame, width=450)
       #frame_duplicate = frame
       gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       canvas = np.zeros((250, 300, 3), dtype="uint8")
       faces = faceCascade.detectMultiScale(
            gray_scale,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
       )
       for (x, y, w, h) in faces:
           cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
       if(len(faces)) :
          faces = sorted(faces, reverse=True,key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
          (fX, fY, fW, fH) = faces
                # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
        # the ROI for classification via the CNN
          roi = gray_scale[fY:fY + fH, fX:fX + fW]
          roi = cv2.resize(roi, (64, 64))
          roi = roi.astype("float") / 255.0
          roi = img_to_array(roi)
          roi = np.expand_dims(roi, axis=0)

          preds = model.predict(roi)[0]
          emotion_probability = np.max(preds)
          label = emotion_dict[preds.argmax()]
          cv2.putText(frame, nume2 + " is " + label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
          for (i, (emotion, prob)) in enumerate(zip(emotion_dict, preds)):
                # construct the label text
                text = "{}: {:.2f}%".format(emotion, prob * 100)

                w = int(prob * 300)
                cv2.putText(frame,text , (5, 25*i+25),  cv2.FONT_HERSHEY_SIMPLEX, 0.45,  (0, 255, 255),  2,  cv2.LINE_4)
                #cv2.rectangle(canvas, (7, (i * 35) + 5),(w, (i * 35) + 35), (0, 0, 255), -1)
                #cv2.putText(canvas, text, (10, (i * 35) + 23),cv2.FONT_HERSHEY_SIMPLEX, 0.45,(255, 255, 255), 2)

          key = cv2.waitKey(20)
          if key == 27: # exit on ESC
             break
           #cv2.destroyAllWindows()

    cv2.destroyAllWindows()
