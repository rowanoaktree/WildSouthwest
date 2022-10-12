#Rowan Converse
#10/12/2022
#Pull camera info from Zooniverse: IMPORTANT, this only works if subject set correspond to individual cameras (ie, were initially uploaded in separate sets)
#This script requires two inputs: the subject export and the COCO format annotations pulled from Zooniverse (see Drones4Ducks /utils/Zooniverse2COCO for example)

import json 
import pandas as pd

#Load data
annotations = r"" #path to downloaded csv classification export from Zooniverse
subjects = r"" #path to downloaded csv subject export from Zooniverse
zooniverse = pd.read_csv(annotations)
subjectinfo = pd.read_csv(subjects)


camanno = []
set_id = None
subjs = {}
cams = {}

for y in range(len(subjectinfo)):
    setsub = subjectinfo["subject_id"][y]
    set = subjectinfo["subject_set_id"][y]
    if setsub not in subjs:
        subjs[setsub] = len(subjs) + 1
        subject_id = subjs[setsub]
        cams[set] = len(cams) + 1
        camera_id = cams[set]
    camera_annotation = {
        'annotation_id': len(camanno)+1,
        'image_id': setsub,
        'camera': set,
      }
    camanno.append(camera_annotation)

df1 = pd.DataFrame(zooniverse)
df2 = pd.DataFrame(camanno)

new3 = pd.merge(df1, df2, how='left', on=["image_id"])