# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 13:08:38 2020

@author: MattiaV
"""
import pandas as pd
from MTM import matchTemplates
import cv2


features_match = {'N_obj':50, 'threshold':0.55, 'method':cv2.TM_CCOEFF_NORMED, 'max_overlap':0.22}

#WATCH OUT: maybe floats are needed
features = [("mass", 5000.), ("size", 72.), ("ecc", 0.), ("signal", 100.), ("raw_mass", 20000.), ("ep", 0.)]


def locate_templates(frame, list_template, match_features=features_match):
    return matchTemplates(list_template, frame, N_object=match_features.get('N_obj'), score_threshold=match_features.get('threshold'), method=cv2.TM_CCOEFF_NORMED, maxOverlap=match_features.get('max_overlap')).sort_index()

def locate_particles(frame, template, match_features=features_match):
    hits = matchTemplates(template.create(), frame, N_object=match_features.get('N_obj'), score_threshold=match_features.get('threshold'), method=cv2.TM_CCOEFF_NORMED, maxOverlap=match_features.get('max_overlap')).sort_index()
    hits.index = range(len(hits))                                   #WARNING: this tris to solve the problem with matchTemplate, as it produces a dataframe with missing indices
    if template.find_centres() is None:
        return hits
    else:
        centres = template.find_centres()
        hits1 = hits['BBox']
        bbox = []
        for i in range(len(hits)):                                  
            x = hits1[i][0] + centres.get(hits.TemplateName[i])[0]
            y = hits1[i][1] + centres.get(hits.TemplateName[i])[1]
            wx = hits1[i][2]
            wy = hits1[i][3]
            bbox.append((x,y,wx,wy))
        hits.BBox = bbox
        return hits
            

def get_coord(hits):
    x, y = [], []
    for i in hits.BBox:
        x.append(i[0])
        y.append(i[1])
    d = {'x' : x, 'y' : y}
    return pd.DataFrame(d)
        

def make_trackable(hits):
    trackable = get_coord(hits)
    i = 0
    while(i < len(features)):
        trackable.insert(i+2, features[i][0], features[i][1])
        i += 1
    return trackable
  

def make_batch(image_sequence, template, match_features):
    frames = []
    for i in range(len(image_sequence)):
        hits = locate_particles(image_sequence[i], template, match_features)
        frame = make_trackable(hits)
        frame.insert(7, "frame", i)
        frames.append(frame)
    return pd.concat(frames)
  
        