from PIL import Image
import numpy as np
import sklearn.decomposition as dc
import matplotlib.pyplot as plt
import Tkinter as tk
from tkFileDialog import *

fn=askopenfilename()

e=raw_input("Which PC?")
e=int(e)
pca=dc.RandomizedPCA(n_components=e)
e=int(e)-1

x=Image.open(fn)
x=np.array(x)

r=x[:,:,0]
g=x[:,:,1]
b=x[:,:,2]

rr=r.flatten()
gg=g.flatten()
bb=b.flatten()

rows,cols=r.shape
row=float(rows)
col=float(cols)
print row/col
t=np.zeros((rr.shape[0], 3))
t[:,0]=rr
t[:,1]=gg
t[:,2]=bb

t2=pca.fit_transform(t)
t2=t2[:,e].reshape((rows,cols))
plt.imshow(t2)
plt.show()
