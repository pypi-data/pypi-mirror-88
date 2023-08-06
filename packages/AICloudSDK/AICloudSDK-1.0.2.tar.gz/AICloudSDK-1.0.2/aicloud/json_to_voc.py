import json
import os,sys,shutil
from PIL import Image
#from aicloud.voc_xml_generator import xml_fill
import yaml
import codecs
def find_image_size(filename):
    with Image.open(filename) as img:
        img_width = img.size[0]
        img_height = img.size[1]
        img_mode = img.mode
        if img_mode == "RGB":
            img_depth = 3
        elif img_mode == "RGBA":
            img_depth = 3
        elif img_mode == "L":
            img_depth = 1
        else:
            print("img_mode = %s is neither RGB or L" % img_mode)
            eixt(0)

        return img_width, img_height, img_depth


def json2voc(yamlPath):
    yamlPath = yamlPath
    f = open(yamlPath,'r',encoding='utf=8')
    cfg = f.read()
    cfgFile = yaml.load(cfg)
    #创建所需文件夹
    tt100k_parent_dir = cfgFile['OUTPUT_DIR']
    work_sapce_dir = os.path.join(tt100k_parent_dir, "VOCdevkit/")
    if not os.path.isdir(work_sapce_dir):
        os.mkdir(work_sapce_dir)
    work_sapce_dir = os.path.join(work_sapce_dir, "VOC2007/")
    if not os.path.isdir(work_sapce_dir):
        os.mkdir(work_sapce_dir)
    jpeg_images_path = os.path.join(work_sapce_dir, 'JPEGImages')
    annotations_path = os.path.join(work_sapce_dir, 'Annotations')
    if not os.path.isdir(jpeg_images_path):
        os.mkdir(jpeg_images_path)
    if not os.path.isdir(annotations_path):
        os.mkdir(annotations_path)
    
    print('***************************数据集开始转换************************************')
    input_labels_dir = cfgFile['INPUT_LABELS_DIR']
    input_images_dir = cfgFile['INPUT_IMAGES_DIR']

    for root,dirs, files in os.walk(input_labels_dir):
        for f in files:
            print('正在转换文件',f)
            json_name = f.split(".")[0]
            #读取标注信息并写入xml
            with open(input_labels_dir+json_name +'.json', 'r',encoding='utf-8') as f:
                object_json = json.load(f)
                #打开对应图像文件
                filename = input_images_dir + json_name + ".jpg"
                width,height,channels = find_image_size(filename)
                with codecs.open(annotations_path + '/' + json_name + ".xml", "w", "utf-8") as xml:
                    xml.write('<annotation>\n')
                    xml.write('\t<folder>' + 'VOC2007' + '</folder>\n')
                    xml.write('\t<filename>' + json_name + ".jpg" + '</filename>\n')
                    xml.write('\t<source>\n')
                    xml.write('\t\t<database>The UAV autolanding</database>\n')
                    xml.write('\t\t<annotation>UAV AutoLanding</annotation>\n')
                    xml.write('\t\t<image>flickr</image>\n')
                    xml.write('\t\t<flickrid>NULL</flickrid>\n')
                    xml.write('\t</source>\n')
                    xml.write('\t<owner>\n')
                    xml.write('\t\t<flickrid>NULL</flickrid>\n')
                    xml.write('\t\t<name>NingWang</name>\n')
                    xml.write('\t</owner>\n')
                    xml.write('\t<size>\n')
                    xml.write('\t\t<width>'+ str(width) + '</width>\n')
                    xml.write('\t\t<height>'+ str(height) + '</height>\n')
                    xml.write('\t\t<depth>' + str(channels) + '</depth>\n')
                    xml.write('\t</size>\n')
                    xml.write('\t\t<segmented>0</segmented>\n')


                    num_obj=len(object_json['objects'])
                    for i in range(num_obj):
                        obj = object_json['objects'][i]
                        label = str(obj['f_code'])
                        for i in range(len(obj['obj_points'])):
                            xmin=int(obj['obj_points'][i]['x'])
                            ymin=int(obj['obj_points'][i]['y'])
                            xmax= xmin + int(obj['obj_points'][i]['w'])
                            ymax= ymin + int(obj['obj_points'][i]['h'])
                            if xmax <= xmin:
                                pass
                            elif ymax <= ymin:
                                pass
                            else:
                                xml.write('\t<object>\n')
                                xml.write('\t\t<name>'+ str(label) + '</name>\n')
                                xml.write('\t\t<pose>Unspecified</pose>\n')
                                xml.write('\t\t<truncated>1</truncated>\n')
                                xml.write('\t\t<difficult>0</difficult>\n')
                                xml.write('\t\t<difficult>0</difficult>\n')
                                xml.write('\t\t<bndbox>\n')
                                xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                                xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                                xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                                xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                                xml.write('\t\t</bndbox>\n')
                                xml.write('\t</object>\n')
                                #print(json_name,xmin,ymin,xmax,ymax,label)
                    xml.write('</annotation>')

    return 
