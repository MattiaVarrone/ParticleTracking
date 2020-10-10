# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 15:55:30 2020

@author: MattiaV
"""
import numpy as np
import skimage.transform as t
from auxiliary import rotate, margins_image, refine_crop

def template90(temp0):
    list_template = []
    for i in np.arange(0, 360, 90):
        rotated = np.rot90(temp0, k=int(i/90)) 
        list_template.append( (str(i%120), rotated) )
    return list_template

def template_rot(temp0, degrees, max_angle=360):
    list_template = []
    for i in np.arange(0, max_angle, degrees):
        rotated1 = t.rotate(temp0, i, preserve_range=True) 
        rotated = np.rint(rotated1).astype(int)             # transforms array of float into array of int
        list_template.append((str(i), rotated))
    return list_template

#centre indicates the coords of the centre of the particle
#vertices is an iterable containing the coordinate of the most external points of the figure as elements of the form (x, y)
# the draft needs to be wider enough for the particle to rotate inside of the margins

def template_polygon(draft, vertices, degrees, max_angle=360):
    list_template = []
    origin = len(draft[0])/2-0.5, len(draft)/2-0.5
    for i in np.arange(0, max_angle, degrees):
        rotated1 = t.rotate(draft, i, preserve_range=True) 
        vertices1 = []
        for vertex in vertices:
            vertices1.append(rotate(origin, vertex, i))
        rotated = refine_crop(rotated1, vertices1)           
        list_template.append((str(i), np.rint(rotated).astype(int)))
    return list_template                           

def rotated_centres(draft, centre, vertices, degrees, max_angle=360):
    centres = {}
    origin = len(draft[0])/2-0.5, len(draft)/2-0.5
    for i in np.arange(0, max_angle, degrees):
        cx, cy = rotate(origin, centre, i)
        vertices1 = []
        for vertex in vertices:
            vertices1.append(rotate(origin, vertex, i))
        margins = margins_image(vertices1)
        xmin, ymin = margins[0][0], margins[1][0]
        centre1 = (np.rint(cx-xmin).astype(int), np.rint(cy-ymin).astype(int))
        centres[str(i)] = centre1              
    return centres                                  


# classes implementation under development
class Template():
    def __init__(self, temp0, centre=None):
        self.temp0 = temp0
        if centre is None:
            self.centre = {'template': (0, 0)}                               
        else:
            self.centre = {'template': centre}
    def create(self):
        return [("template", self.temp0)]
    def find_centres(self):
        centres = {}                                    #centres is a dictionary, not a list of tuples
        templates = self.create()
        for i in templates:
            centres[i[0]] = self.centre
        return centres
    

class Template90(Template):
    def create(self):
        return template90(self.temp0)
    

class TemplateRot(Template):
    def __init__(self, temp0, centre, angle, max_angle=360):
        super().__init__(temp0, centre)
        self.angle = angle
        self.max_angle = max_angle
    def create(self):
        draft = template_rot(self.temp0, self.angle, self.max_angle)
        return draft
    
class TemplatePolygon(Template):
    def __init__(self, temp0, centre, vertices, angle, max_angle=360):
        super().__init__(temp0, centre)
        self.centre = centre
        self.vertices = vertices
        self.angle = angle
        self.max_angle = max_angle
    def find_centres(self):
        return rotated_centres(self.temp0, self.centre, self.vertices, self.angle, self.max_angle)
        
    def create(self):
        return template_polygon(self.temp0, self.vertices, self.angle, self.max_angle)
        
     