#!/usr/bin/env python
# ######################################################################
# Copyright (c) 2014, Brookhaven Science Associates, Brookhaven        #
# National Laboratory. All rights reserved.                            #
#                                                                      #
# Redistribution and use in source and binary forms, with or without   #
# modification, are permitted provided that the following conditions   #
# are met:                                                             #
#                                                                      #
# * Redistributions of source code must retain the above copyright     #
#   notice, this list of conditions and the following disclaimer.      #
#                                                                      #
# * Redistributions in binary form must reproduce the above copyright  #
#   notice this list of conditions and the following disclaimer in     #
#   the documentation and/or other materials provided with the         #
#   distribution.                                                      #
#                                                                      #
# * Neither the name of the Brookhaven Science Associates, Brookhaven  #
#   National Laboratory nor the names of its contributors may be used  #
#   to endorse or promote products derived from this software without  #
#   specific prior written permission.                                 #
#                                                                      #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS  #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT    #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS    #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE       #
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,           #
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES   #
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR   #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)   #
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,  #
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OTHERWISE) ARISING   #
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                          #
########################################################################
"""
This is an example script utilizing dpc.py for Differential Phase Contrast 
(DPC) imaging based on Fourier shift fitting.

This script requires a SOFC folder containing the test data in your home 
directory. The default path for the results (texts and JPEGs) is also your home 
directory. It will automatically download the data to your home directory if
you installed wget and unzip utilities. You can also manually download and
decompress the data at https://www.dropbox.com/s/963c4ymfmbjg5dm/SOFC.zip
    
Steps
-----
1. Set parameters
2. Load the reference image
3. Dimension reduction along x and y direction
4. 1-D IFFT
5. Same calculation on each diffraction pattern
    5.1. Read a diffraction pattern
    5.2. Dimension reduction along x and y direction
    5.3. 1-D IFFT
    5.4. Nonlinear fitting
6. Reconstruct the final phase image
7. Save intermediate and final results
    
"""
    
import os
from os.path import expanduser
from subprocess import call
from scipy.misc import imsave
import numpy as np
import matplotlib.pyplot as plt

import dpc


def load_image(filename):
    """
    Load an image
    
    Parameters
    ----------
    filename : string
        the location and name of an image
    
    Return
    ----------
    t : 2-D numpy array
        store the image data
        
    """ 
    
    if os.path.exists(filename):  
        t = plt.imread(filename)
    
    else:
        print('Please download and decompress the test data to your home directory\n\
               Google drive link, https://drive.google.com/file/d/0B3v6W1bQwN_AVjdYdERHUDBsMmM/edit?usp=sharing\n\
               Dropbox link, https://www.dropbox.com/s/963c4ymfmbjg5dm/SOFC.zip')
        raise Exception('File not found: %s' % filename) 
    
    return t
    
    
if not os.path.exists(expanduser("~") + '/SOFC/'):
    print('The required test data directory was not found\n\
            Start to download the test data to the home directoty')
    call('wget https://www.dropbox.com/s/963c4ymfmbjg5dm/SOFC.zip -P ~/', shell=True)
    call('unzip ~/SOFC.zip -d ~/ && rm ~/SOFC.zip', shell=True)    
   

# 1. Set parameters
file_format = expanduser("~") + '/SOFC/SOFC_%05d.tif'
start_point=[1, 0]
first_image=1
ref_image=1
pixel_size=55
focus_to_det=1.46e6
dx=0.1
dy=0.1
rows = 121
cols = 121
energy=19.5
roi=None
pad=1
w=1.
bad_pixels=None
solver='Nelder-Mead'

# Initialize a, gx, gy and phi
a = np.zeros((rows, cols), dtype='d')
gx = np.zeros((rows, cols), dtype='d')
gy = np.zeros((rows, cols), dtype='d')
phi = np.zeros((rows, cols), dtype='d')

# 2. Load the reference image
ref = load_image(file_format % ref_image)

# 3. Dimension reduction along x and y direction
refx, refy = dpc.image_reduction(ref, roi=roi)
refy = refy[46 : 61]

# 4. 1-D IFFT
ref_fx = dpc.ifft1D(refx)
ref_fy = dpc.ifft1D(refy)

# 5. Same calculation on each diffraction pattern
for i in range(rows):
    print(i)
    for j in range(cols):
        
        # Calculate diffraction pattern index and get its name
        frame_num = first_image + i * cols + j
        filename = file_format % frame_num
        
        try:
            # 5.1. Read a diffraction pattern
            im = load_image(filename)
                   
            # 5.2. Dimension reduction along x and y direction
            imx, imy = dpc.image_reduction(im, roi=roi)
            imy = imy[46 : 61]
            
            # 5.3. 1-D IFFT
            fx = dpc.ifft1D(imx)
            fy = dpc.ifft1D(imy)
                
            # 5.4. Nonlinear fitting
            _a, _gx = dpc.fit(ref_fx, fx)
            _a, _gy = dpc.fit(ref_fy, fy)
                            
            # Store one-point intermediate results
            gx[i, j] = _gx
            gy[i, j] = _gy
            a[i, j] = _a
        
        except Exception as ex:
            print('Failed to calculate %s: %s' % (filename, ex))
            gx[i, j] = 0
            gy[i, j] = 0
            a[i, j] = 0
    
# Scale gx and gy. Not necessary all the time
lambda_ = 12.4e-4 / energy
gx *= - len(ref_fx) * pixel_size / (lambda_ * focus_to_det)
gy *= len(ref_fy) * pixel_size / (lambda_ * focus_to_det)

# 6. Reconstruct the final phase image
phi = dpc.recon(gx, gy)
    
# 7. Save intermediate and final results
imsave(expanduser("~") + '/phi.jpg', phi)
np.savetxt(expanduser("~") + '/phi.txt', phi)
imsave(expanduser("~") + '/a.jpg', a)
np.savetxt(expanduser("~") + '/a.txt', a)
imsave(expanduser("~") + '/gx.jpg', gx)
np.savetxt(expanduser("~") + '/gx.txt', gx)
imsave(expanduser("~") + '/gy.jpg', gy)
np.savetxt(expanduser("~") + '/gy.txt', gy)








