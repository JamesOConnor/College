#!\Users\k1454695\AppData\Local\Continuum\Anaconda\python
#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

print """
<html>

<head><title>Sample CGI Script</title></head>

<body>

  <h3> Sample CGI Script </h3>
"""

form = cgi.FieldStorage()
imgL = form.getvalue("imgL", "(no message)")
imgR = form.getvalue("imgR", "(no message)")

print """

  <p>Previous message: %s</p>

  <p>form

  <form method="post" action="index.cgi">
    <div>imgL: <input type="text" name="imgL"/></div>
	<div>imgR: <input type="text" name="imgR"/></div>
	<div><input type="submit" value="GO!"/></div>

  </form>

</body>

</html>
"""



if imgL.split('.')[-1] in ['png', 'jpg', 'jpeg']:
	import numpy as np
	import cv2
	from skimage import io
	from PIL import Image
	import os
	ims=[]
	imgL=io.imread(imgL)
	imgR=io.imread(imgR)

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

	print "<html><img src='imgs/res.png'></html>"
	
	
