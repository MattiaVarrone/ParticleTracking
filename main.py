# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 17:25:02 2020

@author: MattiaV
"""
import cv2
from skimage import io
import matplotlib.pyplot as plt
from template_opt import TemplatePolygon
from track import make_batch
import trackpy as tp
from test_template import overlay_sequence as over

fileImages = r"C:\Users\MattiaV\Desktop\università\Interships\DynamicsOfGranularShapes\ParticleTracking\Images\3V\*.bmp"
file_template = r"C:\Users\MattiaV\Desktop\università\Interships\DynamicsOfGranularShapes\ParticleTracking\Images\templates\particleY.png"
images = io.imread_collection(fileImages)[:20]
temp_draft = io.imread(file_template)
#temp_draft = imag[310:433,520:650]
#temp0 = temp_draft[33:92,27:105]

vertices = [(27,43),(34,33),(53,102),(66,102),(95,38),(104,50)]
centre = (62,48)
angle = 10
max_angle = 120

Temp = TemplatePolygon(temp_draft, centre, vertices, angle, max_angle)
list_template = Temp.create()

features_match = {'N_obj':80, 'threshold':0.70, 'method':cv2.TM_CCOEFF_NORMED, 'max_overlap':0.35}
batch = make_batch(images, Temp, features_match)


t0 = tp.link(batch, 70, memory = 4)

t1 = tp.filter_stubs(t0, 10)
# Compare the number of particles in the unfiltered and filtered data.
print('Before:', t0['particle'].nunique())
print('After:', t1['particle'].nunique())

plt.figure()
tp.plot_traj(t1);


over(images, Temp, features_match)