####
# Creator: Rowan Converse (rowanconverse@unm.edu)
# Date: 2022/10/20
# Purpose: Translate raw labels generated by volunteers on the participatory science platform Zooniverse into COCO format for public release 
# Ref COCO Camera Trap Standard: https://cocodataset.org/#format-data

##Note!! This is not yet complete COCO format, do not use this script yet for public data releases
####

#Load necessary modules
import json
import pandas as pd

#Load data
path = r"" #Requires .csv workflow classification export from Zooniverse
zooniverse = pd.read_csv(path)

###Annotations: import ID, Image ID, Category ID, bounding boxes (x,y, width, height). 
images = {}
annos = []
categories = {}

for i in range(len(zooniverse)):
  image_id = None
  imgrow = json.loads(zooniverse.subject_data[i])
  for key in imgrow.keys():
      name = imgrow[key]["Filename"]
      if name not in images:
        images[name] = len(images) + 1
      image_id = images[name]
      row = json.loads(zooniverse["annotations"][i])
      for j in range(len(row)):
        if row[j]['task'] == 'T1':
            annlist = row[j]['value']
            for k in range(len(annlist)):
                ann = annlist[k]
                x = ann["x"]
                y = ann["y"]
                w = ann["width"]
                h = ann["height"]
                bbox = [x, y, w, h]
        if row[j]['task'] == 'T0': 
          labelinfo = row[j]['value']
          for k in range(len(labelinfo)):
            lbl = labelinfo[k]
            label = lbl["choice"]
            if label not in categories:
   #label class has not yet been registered; add
                  categories[label] = len(categories) + 1
                  category_id = categories[label]
      annotation = {
        'annotation_id': len(annos)+1,
        'bbox': bbox,
        'category_id': category_id,
        'class': label,
        'image_id': image_id,
        'filename': name
      }
      annos.append(annotation)

#Save in JSON format
with open("sevclean.json", "w") as outfile:
    json.dump(annos, outfile)