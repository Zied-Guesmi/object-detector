import os
import argparse
import traceback
import urllib.request
from urllib.parse import urlparse

import numpy as np
import cv2
import imghdr


supported_images = [ "pbm", "pgm", "ppm", "tiff", "rast", "xbm", "jpeg", "bmp", "png" ]
known_classes = [ "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
                  "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
                  "pottedplant", "sheep", "sofa", "train", "tvmonitor" ]
generated_colors = np.random.uniform(0, 255, size=(len(known_classes), 3))
input_dir = ""
output_dir = ""

def input_abs_path(filename): return input_dir + "/" + filename

def output_abs_path(filename): return output_dir + "/" + filename

def is_supported_image(filepath):
    return os.path.isfile(filepath) and imghdr.what(filepath) in supported_images

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("image-uri",        type=str,                           help="URI of image to be processes")
    parser.add_argument("--input-dir",      type=str,   default="/iexec_in",    help="Trained models folder path")
    parser.add_argument("--output-dir",     type=str,   default="/iexec_out",   help="Output folder path")
    parser.add_argument("--min-confidence", type=float, default=0.2,            help="Minimum confidence to consider prediction")
    params = vars(parser.parse_args())
    return params["image-uri"], params["input_dir"], params["output_dir"], params["min_confidence"]

def load_input_image(image_uri):
    parsed_url = urlparse(image_uri)
    image_name = os.path.basename(parsed_url.path)
    image_path, http_message = urllib.request.urlretrieve(image_uri)
    return image_name, image_path

def load_dnn_model():
    print("Loading DNN network model")
    prototxt = input_abs_path("MobileNetSSD_deploy.prototxt.txt")
    print("Prototxt file:" + prototxt)
    caffe_model = input_abs_path("MobileNetSSD_deploy.caffemodel")
    print("caffe model file:" + caffe_model, end="\n\n")
    return cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

def detect_objects(net, input_image_path, output_image_path, min_confidence):
    # load the input image and resize the blob to 300x300 pixels
    image = cv2.imread(input_image_path)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass image throw model
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

    image_uri, input_dir, output_dir, min_confidence = parse_args()
    image_name, image_path = load_input_image(image_uri)
    save_to = output_abs_path(image_name)
    determinism_file = output_abs_path("determinism.iexec")

    if not is_supported_image(image_path):
        print("File type not supported: " + image_path)
        exit(1)

    # clean output folder if needed
    for f in os.listdir(output_dir): os.remove(output_abs_path(f))

    # load model
    net = load_dnn_model()

    # run detector
    print("Processing image: " + image_name)
    objects_in_image = detect_objects(net, image_path, save_to, min_confidence)

    # save determinism output
    with open(determinism_file, "w") as df:
        df.write(image_name + "\n")
        df.write("\n".join(objects_in_image))