#coding:utf-8
import os
import json
import time
from PIL import Image
import numpy as np
import cv2
import yaml


def json2mapillary(yamlPath):
    yamlPath = yamlPath
    f = open(yamlPath,'r',encoding='utf=8')
    cfg = f.read()
    cfgFile = yaml.load(cfg)
    print('***************************数据集开始转换*****************************')
    input_labels_dir = cfgFile['INPUT_LABELS_DIR']
    input_images_dir = cfgFile['INPUT_IMAGES_DIR']
    output_dir = cfgFile['OUTPUT_DIR']
    class_type  = cfgFile['CLASS_TYPE']

    for root,dirs, files in os.walk(input_labels_dir):
        for f in files:
            print('正在转换文件',f)
            json_name = f.split(".")[0]
            with open(input_labels_dir+json_name +'.json', 'r',encoding='utf-8') as f:
                object_json = json.load(f)
                num_obj=len(object_json['objects'])
                image = Image.open(input_images_dir+json_name +'.jpg')
                image = np.array(image)
                image_h, image_w = image.shape[:2]
                image_temp =np. zeros((image_h,image_w),dtype=np.uint8)
                
                #print('num_obj=',num_obj)
                for i in range(num_obj):
                    obj = object_json['objects'][i]
                    class_name = str(obj['f_code']).lower()
                    for item in class_type:
                        if class_name == str(item):
                            label_polygon = []
                            for i in range(len(obj['obj_points'])):
                                x=int(obj['obj_points'][i]['x'])
                                y=int(obj['obj_points'][i]['y'])
                                label_xy = [x,y]
                                label_polygon.append(label_xy)
                                a = np.array(label_polygon)
                                                       
                            cv2.fillPoly(image_temp, [a], class_type[item])
                            
                cv2.imwrite(output_dir + json_name +'.png', image_temp)
              
