# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:47:43 2020

@author: MattiaV
"""
from MTM import matchTemplates, drawBoxesOnRGB
from track import locate_templates
import matplotlib.pyplot as plt

def overlay_frame(image, template, match_features, show_templates=False):
    list_template = template.create()
    hits = locate_templates(image, list_template, match_features)
    l = len(list_template)
    if l<12 and show_templates:
        f, axarr = plt.subplots(1, l)
        for i in range(l):
            axarr[i].imshow(list_template[i][1])
            
    overlay = drawBoxesOnRGB(image, hits, boxThickness=5)
    plt.figure(figsize = (30,30))
    plt.imshow(overlay)
    
def overlay_sequence(image_sequence, template, match_features, show_templates=False):
    for i in range(min(len(image_sequence), 3)):
        overlay_frame(image_sequence[i], template, match_features, show_templates)
            
        
