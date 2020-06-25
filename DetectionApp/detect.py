import cv2
import numpy as np
from operator import itemgetter


def load_yolo(params):
    if params == 'detection':
        print(params)
        net = cv2.dnn.readNet("cfg/yolov3-416_18000.weights", "cfg/yolov3-416.cfg")
        classes = []
        with open("./cfg/obj.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layers_names = net.getLayerNames()
        output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
    else :
        net = cv2.dnn.readNet("cfg/yolov3-416-clean_5000.weights", "cfg/yolov3-416-clean.cfg")
        classes = []
        with open("./cfg/obj-clean.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layers_names = net.getLayerNames()
        output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

    return net, classes, colors, output_layers


def load_image(img_path):
    # image loading
    print(img_path)
    img = cv2.imread('./' + img_path)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape
    return img, height, width, channels


def detect_objects(img, net, outputLayers):
    blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(416, 416), mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(outputLayers)
    return blob, outputs


def get_box_dimensions(outputs, height, width):
    confs = []
    class_ids = []
    for output in outputs:
        for detect in output:
            scores = detect[5:]
            class_id = np.argmax(scores)
            conf = scores[class_id]
            if conf > 0.01:

                confs.append(float(conf))
                class_ids.append(class_id)
    print(confs, class_ids)
    return confs, class_ids


def draw_labels(params, confs, colors, class_ids, classes, img):

    print('label size: ', len(class_ids))
    print('score size: ',len(confs))
    result = list()

    for i in range(len(class_ids)):
        result.append({
            'label' : classes[class_ids[i]],
            'confidence' : confs[i]
        })
    print('result: ',result)

    if params == 'detection':
        result_removed_deduplication = list(
            {result['label']: result for result in result}.values())
        print("duplicate removed: ", result_removed_deduplication)
        result_sorted = sorted(result_removed_deduplication, key=itemgetter('confidence'), reverse=True)

    else :
        result_sorted = sorted(result, key=itemgetter('confidence'), reverse=True)
        print('sort: ', result_sorted)

    print('return result: ', result_sorted)
    return result_sorted

def image_detect(params, img_path):
    model, classes, colors, output_layers = load_yolo(params)
    image, height, width, channels = load_image(img_path)
    blob, outputs = detect_objects(image, model, output_layers)
    confs, class_ids = get_box_dimensions(outputs, height, width)
    result = draw_labels(params, confs, colors, class_ids, classes, image)

    return result
