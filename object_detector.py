import os
import sys
import subprocess
import argparse
import traceback
import urllib.request
import shutil
from urllib.parse import urlparse

from collections import OrderedDict
import numpy as np
import cv2
import imghdr


supported_images = [ "pbm", "pgm", "ppm", "tiff", "rast", "xbm", "jpeg", "bmp", "png" ]
known_classes = [ "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
                  "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
                  "pottedplant", "sheep", "sofa", "train", "tvmonitor" ]
generated_colors = np.random.uniform(0, 255, size=(len(known_classes), 3))

def input_abs_path(filename): return "/iexec_in/" + filename

def output_abs_path(filename): return "/iexec_out/" + filename

def is_supported_image(filepath):
    return os.path.isfile(filepath) and imghdr.what(filepath) in supported_images

def load_input_image(image_uri):
    parsed_url = urlparse(image_uri)
    image_name = os.path.basename(parsed_url.path)
    image_path, http_message = urllib.request.urlretrieve(image_uri)
    return image_name, image_path

def load_dnn_model(prototxt, caffe_model):
    print("Loading DNN network model")
    print("Prototxt file:" + prototxt)
    print("caffe model file:" + caffe_model, end="\n\n")
    return cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

def detect_objects(net, input_image_path, output_image_path, min_confidence):
    # load the input image and resize the blob to 300x300 pixels
    image = cv2.imread(input_image_path)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # run detector
    net.setInput(blob)
    detections = net.forward()

    objects_in_image = []
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < min_confidence:
            continue

        # get class label & compute the bounding box for the object
        class_idx = int(detections[0, 0, i, 1])
        label = "{}: {:.2f}%".format(known_classes[class_idx], confidence * 100)
        # get object coordinates
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (start_x, start_y, end_x, end_y) = box.astype("int")

        # add label to image
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), generated_colors[class_idx], 2)
        y = start_y - 15 if start_y - 15 > 15 else start_y + 15
        cv2.putText(image, label, (start_x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, generated_colors[class_idx], 2)

        prediction = "[PREDICTION] {}".format(label)
        print(prediction)
        objects_in_image.append(prediction)

    # save result image
    cv2.imwrite(output_image_path, image)
    return objects_in_image

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--image-uri",      type=str,                           help="URI of image to be processes")
    parser.add_argument("--models-dir",     type=str,   default="/iexec_in",    help="URI of image to be processes")
    parser.add_argument("--min-confidence", type=int,   default=0.2,            help="Minimum confidence to consider prediction")
    params = parser.parse_args()

    image_name, image_path = load_input_image(params.image_uri)
    save_to = output_abs_path(image_name)

    prototxt = input_abs_path("MobileNetSSD_deploy.prototxt.txt")
    caffe_model = input_abs_path("MobileNetSSD_deploy.caffemodel")
    net = load_dnn_model(prototxt, caffe_model)

    determinism_file = output_abs_path("determinism.iexec")

    if not is_supported_image(image_path):
        print("File type not supported: " + image_path, end="\n\n")
        exit(1)

    try:
        print("Processing image: " + image_name)
        objects_in_image = detect_objects(net, image_path, save_to, params.min_confidence)
        print()
        with open(determinism_file, "a") as df:
            df.write(image_name + "\n")
            df.write("\n".join(objects_in_image) + "\n\n")

    except Exception as e:
        print(traceback.format_exc(), end="\n\n")
        with open(determinism_file, "a") as df:
            df.write(image_name + "\n")
            df.write(traceback.format_exc() + "\n\n")
