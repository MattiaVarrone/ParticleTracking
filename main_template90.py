# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 17:04:49 2020

@author: MattiaV
"""

from MTM import matchTemplates
import cv2
from skimage import io
import matplotlib.pyplot as plt
from template_opt import Template90
from track import make_batch
import trackpy as tp

fileID = r"C:\Users\MattiaV\Desktop\università\Interships\DynamicsOfGranularShapes\ParticleTracking\Images\First frames\*.png"
images = io.imread_collection(fileID) 
temp_draft1 = images[0][320:433,520:650]
temp0 = temp_draft1[23:92,28:105]

Temp = Template90(temp0)
list_template = Temp.create()

features_match = {'N_obj':50, 'threshold':0.55, 'method':cv2.TM_CCOEFF_NORMED, 'max_overlap':0.22}
batch = make_batch(images, list_template, features_match)

t0 = tp.link(batch, 50, memory = 3)

t1 = tp.filter_stubs(t0, 4)
# Compare the number of particles in the unfiltered and filtered data.
print('Before:', t0['particle'].nunique())
print('After:', t1['particle'].nunique())

plt.figure()
tp.plot_traj(t1);