import os

import numpy as np
import cv2

import custom_exceptions as customExceptions


class ObjectDetector:

    CLASSES = [ "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
    "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor" ]

    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    dirname = os.path.dirname(os.path.realpath(__file__))

    prototxt = '{}/{}'.format(dirname, 'model/MobileNetSSD_deploy.prototxt.txt')
    caffeModel = '{}/{}'.format(dirname, 'model/MobileNetSSD_deploy.caffemodel')

    def run(self, imgPath, outPath, minConfidence):
        # print("[INFO] loading model...")
        try: net = cv2.dnn.readNetFromCaffe(self.prototxt, self.caffeModel)
        except Exception as e: raise customExceptions.Error(e, 'CantLoadModel')

        try:
            # load the input image and resize the blob to 300x300 pixels
            image = cv2.imread(imgPath)
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
        except Exception as e:
            raise customExceptions.Error(e, 'CantLoadImage')

        # print("[INFO] computing object detections...")
        try:
            net.setInput(blob)
            detections = net.forward()
        except Exception as e:
            raise customExceptions.Error(e, 'DnnNetworkError')

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            ##
            # print('confidence=' + str(confidence))
            # print('min confidence=' + str(minConfidence))
            ## 
            if confidence > minConfidence:
                try:
                    # get index of the class label then compute the bounding box for the object
                    idx = int(detections[0, 0, i, 1])
                    label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                    print("[PREDICTION] {}".format(label))
                except Exception as e:
                    raise customExceptions.Error(e, 'CantGetClassIndex')

                try:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                except Exception as e:
                    raise customExceptions.Error(e, 'CantGetObjCoordinates')

                try:
                    cv2.rectangle(image, (startX, startY), (endX, endY), self.COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)
                except Exception as e:
                    raise customExceptions.Error(e, 'CantAddLabelToImage')

        # print("[INFO] saving labeled image...")
        try: cv2.imwrite(outPath, image)
        except Exception as e: raise customExceptions.Error(e, 'CantSaveOutputImage')