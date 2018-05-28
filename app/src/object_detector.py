import numpy as np
import cv2

import custom_exceptions as customExceptions


class ObjectDetector:

    CLASSES = [ "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
    "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor" ]
    
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    prototxt = "MobileNetSSD_deploy.prototxt.txt"
    model = "MobileNetSSD_deploy.caffemodel"

    def run(self, path, minConfidence):

        # load our serialized model from disk
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

        # load the input image and construct an input blob for the image by resizing to a fixed
        #  300x300 pixels and then normalizing it (note: normalization is done via the authors
        # of the MobileNet SSD implementation)
        image = cv2.imread(path)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and predictions
        print("[INFO] computing object detections...")
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the prediction
            confidence = detections[0, 0, i, 2]

            # `confidence` is greater than the minimum confidence
            if confidence > minConfidence:
                # extract the index of the class label from the `detections`, then compute the
                # (x, y)-coordinates of the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # display the prediction
                label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                print("[INFO] {}".format(label))
                cv2.rectangle(image, (startX, startY), (endX, endY), self.COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)

        # show the output image
        cv2.imshow("Output", image)
        cv2.imwrite("IMAGE_NAME.png", image)
        # cv2.waitKey(0)

        try:
            pass
        except Exception as e:
            raise customExceptions.CanNotDetectObjectsError(e, path)