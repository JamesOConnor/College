#!\Users\k1454695\AppData\Local\Continuum\Anaconda\python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()
import numpy as np
import cv2
from skimage import io
from PIL import Image
import os
ims=[]
for i in range(2):
	image=io.imread("http://vision.middlebury.edu/stereo/data/scenes2014/datasets/Umbrella-perfect/im%d.png"%(i))
	ims.append(image)
	
#!/usr/bin/env python

'''
Simple example of stereo image matching and point cloud generation.

Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net/ )
'''

y=os.getcwd()
print y
Image.fromarray(ims[0]).save("imgs/ImgL.jpeg")
Image.fromarray(ims[1]).save("imgs/ImgR.jpeg")

imgL = cv2.pyrDown( cv2.imread('imgs/ImgL.jpeg') )
imgR = cv2.pyrDown( cv2.imread('imgs/ImgR.jpeg') )

window_size = 3
min_disp = 16
num_disp = 112-min_disp
stereo = cv2.StereoSGBM(minDisparity = min_disp,
	numDisparities = num_disp,
	SADWindowSize = window_size,
	uniquenessRatio = 10,
	speckleWindowSize = 100,
	speckleRange = 32,
	disp12MaxDiff = 1,
	P1 = 8*3*window_size**2,
	P2 = 32*3*window_size**2,
	fullDP = False
)

disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
Image.fromarray((disp-min_disp)/num_disp).save("imgs/res.tiff")
cmd="convert imgs/res.tiff imgs/res.png"
os.system(cmd)

print "Content-Type: text/html;charset=utf-8"
print
print "<html><img src='imgs/res.png'></html>"



