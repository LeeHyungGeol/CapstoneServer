import cv2
from darkflow.net.build import TFNet
# import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

#%config InlineBackend.figure_format = 'svg'

def getItemName(img_url):


    options = {
        'model' : './DetectionApp/darkflow/cfg/my-tiny-yolo.cfg',
        'load' : 142000,
        'threshold' : 0.01,
        #    'batch' : 1
        # 'gpu' : 0.7
    }

    tfnet = TFNet(options)
    tfnet.load_from_ckpt()
    img = cv2.imread('./'+img_url, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = tfnet.return_predict(img)
    result_sorted = sorted(result, key=itemgetter('confidence'), reverse=True)

    return result_sorted
