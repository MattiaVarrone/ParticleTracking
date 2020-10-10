# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 16:10:38 2020

@author: MattiaV
"""

from MTM import matchTemplates, drawBoxesOnRGB
import cv2
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

fileID = r"C:\Users\MattiaV\Desktop\università\Interships\DynamicsOfGranularShapes\ParticleTracking\Images\First frames\f1.png"
image = io.imread(fileID) 
temp_draft = image[300:500,500:670]
temp0 = temp_draft[41:113,48:123]
image2 = io.imread(r"C:\Users\MattiaV\Desktop\università\Interships\DynamicsOfGranularShapes\ParticleTracking\Images\First frames\f2.png")

listTemplate = []

# Initialise figure
f, axarr = plt.subplots(1,4)


for i in np.arange(0, 360, 90):
    #rotated1 = t.rotate(temp0, i, preserve_range=True) 
    #rotated = np.rint(rotated1).astype(int)           # transforms array of float into array of int
    rotated = np.rot90(temp0, k=int(i/90)) # NB: np.rotate not good here, turns into float!
    listTemplate.append( (str(i%120), rotated ) )
    axarr[int(i/90)].imshow(rotated)
    # We could also do some flipping with np.fliplr, flipud

Hits = matchTemplates(listTemplate, image2, N_object=50, score_threshold=0.55, method=cv2.TM_CCOEFF_NORMED, maxOverlap=0.22).sort_index()

Overlay = drawBoxesOnRGB(image, Hits, boxThickness=5)
plt.figure(figsize = (30,30))
plt.axis("off")
plt.imshow(Overlay)

