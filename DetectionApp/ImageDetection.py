import cv2
from darkflow.net.build import TFNet
# import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import json

#%config InlineBackend.figure_format = 'svg'

def getItemName(img_url, params):

    if params == 'clean':
        print('clean')
        options = {
            'model' : './DetectionApp/darkflow/cfg/yolo-clean2.cfg',
            'labels' : './labels-clean.txt',
            'load' : 53562,
            'threshold' : 0.3,
            'batch' : 1,
            # 'gpu' : 0.7
        }
    elif params == 'detection':
        print('detection')
        options = {
            'model' : './DetectionApp/darkflow/cfg/yolo-cap3.cfg',
            'labels': './labels.txt',
            'load' : 158991,
            'threshold' : 0.3,
            'batch': 1,
            # 'gpu' : 0.7
        }

    tfnet = TFNet(options)
    tfnet.load_from_ckpt()
    img = cv2.imread('./'+img_url, cv2.IMREAD_COLOR)
    # img = cv2.imread('C:/data/dataset/5.jpg')

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = tfnet.return_predict(img)
    result_sorted = sorted(result, key=itemgetter('confidence'), reverse=True)
    print('sort: ', result_sorted)

    if params == 'detection':
        result_removed_deduplication = list({result_sorted['label']: result_sorted for result_sorted in result_sorted}.values())
        print("result: ",  result_removed_deduplication)
        return result_removed_deduplication

    return result_sorted