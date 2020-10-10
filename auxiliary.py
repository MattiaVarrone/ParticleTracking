# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 00:38:34 2020

@author: MattiaV
"""
import math
import numpy as np

def rotate(origin, point, degrees):
    ox, oy = origin
    px, py = point
    angle = math.radians(degrees)
    qx = ox + math.cos(angle) * (px - ox) + math.sin(angle) * (py - oy)
    qy = oy - math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def margins_image(vertices):
    xmax, ymax = 0, 0
    xmin, ymin = float('inf'), float('inf')
    for x, y in vertices:
        if xmax < x:
            xmax = x
        if ymax < y:
            ymax = y
        if xmin > x:
            xmin = x
        if ymin > y:
            ymin = y      
    return[(xmin, xmax), (ymin, ymax)]
    
    
def refine_crop(draft, vertices):
    xmin, xmax = margins_image(vertices)[0]
    ymin, ymax = margins_image(vertices)[1]
    xmax, ymax = np.rint(xmax).astype(int), np.rint(ymax).astype(int)
    xmin, ymin = np.rint(xmin).astype(int), np.rint(ymin).astype(int)
    return draft[ymin:ymax, xmin:xmax]