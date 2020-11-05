import xml
import xml.etree.ElementTree as ET
import os, sys, glob
import argparse

def get_label_map(label_map_path):

    label_map = {}
    with open(label_map_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        for i, line in enumerate(lines):
            a = line.splitlines()[0]
            label_map[a] = i
    return label_map


def parse_xml(img, file, label_map):
    tree = ET.parse(file)
    
    root = tree.getroot()
    obs = root.findall('object')

    annotation = list()

    for i, ob in enumerate(obs):

        cnt = int()

        bndbox = ob.find('bndbox')
        name = ob.find('name').text
        name_idx = label_map[name]
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text
        
        tmp = xmin + "," + ymin + "," + xmax + "," + ymax + "," + str(name_idx)
        
        annotation.append(tmp)
    
    anno = img + " " + " ".join(annotation)

    return anno

annot_dir = "C:/Users/G/workspace/data/yolo_camera/annot/"
img_dir = "C:/Users/G/workspace/data/yolo_camera/img/"
label_map_path = "./yolo_camera.names"

imgs_name = [os.path.splitext(f.name)[0] for f in os.scandir(img_dir)]

label_map = get_label_map(label_map_path)
with open("C:/Users/G/workspace/data/yolo_camera/annot.txt",'w') as f:
    for img_name in imgs_name:

        annot_path = os.path.join(annot_dir, img_name + '.xml')
        img_path = os.path.join(img_dir, img_name + '.jpg')

        result_parse = parse_xml(img_path, annot_path, label_map)
        print(result_parse)
        f.write(result_parse + "\n")

