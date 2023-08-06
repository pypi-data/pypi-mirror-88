# -*- coding: utf-8 -*-
import os
from os import path
import json
import numpy as np
import pandas as pd
import glob
import cv2
import os
import yaml
import shutil
from IPython import embed
from sklearn.model_selection import train_test_split
np.random.seed(41)


class Csv2CoCo:

    def __init__(self,image_dir,total_annos, classname_to_id):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0
        self.image_dir = image_dir
        self.total_annos = total_annos
        self.classname_to_id = classname_to_id

    def save_coco_json(self, instance, save_path):
        json.dump(instance, open(save_path, 'w'), ensure_ascii=False, indent=2)  # indent=2 更加美观显示

    # 由txt文件构建COCO
    def to_coco(self, keys, classname_to_id):
        self._init_categories(classname_to_id)
        for key in keys:
            self.images.append(self._image(key))
            shapes = self.total_annos[key]
            for shape in shapes:
                bboxi = []
                for cor in shape[:-1]:
                    bboxi.append(int(cor))
                label = shape[-1]
                # if label != '16007' or label != '16008':
                #     continue
                annotation = self._annotation(bboxi,label, classname_to_id)
                self.annotations.append(annotation)
                self.ann_id += 1
            self.img_id += 1
        instance = {}
        instance['info'] = 'spytensor created'
        instance['license'] = ['license']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance

    # 构建类别
    def _init_categories(self, classname_to_id):
        for k, v in classname_to_id.items():
            category = {}
            category['id'] = v
            category['name'] = k
            self.categories.append(category)

    # 构建COCO的image字段
    def _image(self, path):
        image = {}
        #print(self.image_dir + path)
        print('正在转换:', path)
        img = cv2.imread(self.image_dir + path)
        image['height'] = img.shape[0]
        image['width'] = img.shape[1]
        image['id'] = self.img_id
        image['file_name'] = path
        return image

    # 构建COCO的annotation字段
    def _annotation(self, shape,label, classname_to_id):
        # label = shape[-1]
        points = shape[:4]
        annotation = {}
        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        annotation['category_id'] = int(classname_to_id[label])
        annotation['segmentation'] = self._get_seg(points)
        annotation['bbox'] = self._get_box(points)
        annotation['iscrowd'] = 0
        annotation['area'] = self._get_area(points)
        return annotation

    # COCO的格式： [x1,y1,w,h] 对应COCO的bbox格式
    def _get_box(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        return [min_x, min_y, max_x - min_x, max_y - min_y]
    # 计算面积
    def _get_area(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        return (max_x - min_x+1) * (max_y - min_y+1)
    # segmentation
    def _get_seg(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        h = max_y - min_y
        w = max_x - min_x
        a = []
        a.append([min_x,min_y, min_x,min_y+0.5*h, min_x,max_y, min_x+0.5*w,max_y, max_x,max_y, max_x,max_y-0.5*h, max_x,min_y, max_x-0.5*w,min_y])
        return a
   


def json_to_csv(path, img_path):
    json_list = []
    for json_file in glob.glob(path + '/*.json'):  #返回所有匹配的文件路径列表
        fp_json_file = json.load(open(json_file, "r"))
        filename = os.path.basename(json_file)
        for multi in fp_json_file["objects"]:
            points = multi["obj_points"][0]
            xmin = points["x"]
            ymin = points["y"]
            xmax = points["x"]+points["w"]-1
            ymax = points["y"]+points["h"]-1
            label = multi["f_code"]
            if xmax <= xmin: pass
            elif ymax <= ymin: pass
            value = (img_path +'/' + filename[:-5] + '.jpg',
                    int(xmin),
                    int(ymin),
                    int(xmax),
                    int(ymax),
                    str(label))
            json_list.append(value)
    column_name = ['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class']
    xml_df = pd.DataFrame(json_list, columns=column_name)
                    
    return xml_df



def json2coco(yamlPath):
    yamlPath = yamlPath
    f = open(yamlPath,'r',encoding='utf=8')
    cfg = f.read()
    cfgFile = yaml.load(cfg)
 
    img_path = cfgFile['INPUT_IMAGES_DIR']
    print('输入图像路径:',  img_path)
    output_path = cfgFile['OUTPUT_DIR']
    print('输出结果路径:', output_path)
    #print('数据集开始转换')
    xml_df = json_to_csv(cfgFile['INPUT_LABELS_DIR'], img_path)
    ## 修改文件名称
    xml_df.to_csv('./scratches.csv', index=None)
    #print('Successfully converted xml to csv.')

    # 标注路径
    label_path = cfgFile['INPUT_LABELS_DIR']
    print('输入标注路径:', label_path)
    csv_file= "./scratches.csv"
    classname_to_id =  cfgFile['CLASS_ID']
    print('对象ID:', classname_to_id)
    print('********************数据集开始转换*************************')
    # 整合csv格式标注文件
    total_csv_annotations = {}
    annotations = pd.read_csv(csv_file,header=None).values
    for annotation in annotations:
        key = annotation[0].split(os.sep)[-1]
        value = np.array([annotation[1:]])
        if key in total_csv_annotations.keys():
            total_csv_annotations[key] = np.concatenate((total_csv_annotations[key],value),axis=0)
        else:
            total_csv_annotations[key] = value
    # 按照键值划分数据
    total_keys = list(total_csv_annotations.keys())
    train_keys, val_keys = train_test_split(total_keys[1:], test_size=0.2) #去掉第一行
    print('*******************训练集和验证集划分**********************')
    print("训练集数目:", len(train_keys), '验证集数目:', len(val_keys))
    # 创建必须的文件夹
    #print('转换后数据保存在datasets目录')

    if not os.path.exists(output_path + 'datasets/annotations/ark/'):
        os.makedirs(output_path + 'datasets/annotations/ark/')
    if not os.path.exists(output_path+ 'datasets/train/'):
        os.makedirs(output_path + 'datasets/train/')
    if not os.path.exists(output_path + 'datasets/test/'):
        os.makedirs(output_path + 'datasets/test/')
    # 把训练集转化为COCO的json格式
    print('*********************训练集转换中，请稍后**************************')
    l2c_train = Csv2CoCo(image_dir=img_path, total_annos=total_csv_annotations, classname_to_id=classname_to_id)
    train_instance = l2c_train.to_coco(train_keys, classname_to_id)
    l2c_train.save_coco_json(train_instance, output_path + 'datasets/annotations/ark/instances_train2020.json')
    print('**********************训练集转换完成*******************************')
    print('***********************验证集转换中,请稍后*************************')
    #for file in train_keys:
    #    shutil.copy(img_path+file,output_path + "datasets/train/")
    #for file in val_keys:
    #    shutil.copy(img_path+file,output_path + "datasets/test/")
    # 把验证集转化为COCO的json格式
    l2c_val = Csv2CoCo(image_dir=img_path,total_annos=total_csv_annotations, classname_to_id=classname_to_id)
    val_instance = l2c_val.to_coco(val_keys, classname_to_id)
    l2c_val.save_coco_json(val_instance, output_path + 'datasets/annotations/ark/instances_val2020.json')
    print('************************验证集转换完成****************************')
    print('************************正在进行图片拷贝**************************')
    for file in train_keys:
        shutil.copy(img_path+file,output_path + "datasets/train/")
    for file in val_keys:
        shutil.copy(img_path+file,output_path + "datasets/test/")
    print('************************数据集转换完成****************************')

     

