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

    This is an example of using real experimental XPCS(X-ray Photon
    Correlation Spectroscopy) data for calculate one time correlation
    functions.

"""


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six
import numpy as np
import logging
logger = logging.getLogger(__name__)
import time
import nsls2.recip as recip
import nsls2.timecorr as timecorr
import matplotlib.pyplot as plt


def plot_q_rings(q_inds, detector_size):
    """
    Parameters
    ----------
    q_inds : ndarray
        indices of the Q values for the required rings

    detector_size : tuple
        2 element tuple defining the number of pixels in the detector.
        Order is (num_columns, num_rows)

    Return
    ------
    Plot of  Q rings
    """
    q_inds = q_inds.reshape(detector_size[0], detector_size[1])
    plt.title(" Required Q Rings  ")
    plt.imshow(q_inds)
    plt.show()


def plot_g2(g2):
    """
    Parameters
    ----------
    g2: ndarray
        matrix of one-time correlation

    Return
    ------
    Plot of 1 time correlation plots for each Q ring
    """

    plt.title(" 1 time correlation plots ")
    for i in range(0, num_qs):
        plt.plot(g2(i) + (i*10))
    plt.show()
    return


if __name__ == "__main__":
    #  image data as a stack
    img_stack = np.load("img_stack5301_5401.npy")

    detector_size = (256, 256)
    pixel_size = (0.0135*8, 0.0135*8)
    calibrated_center = (143, 123)  # (mm)
    dist_sample = 2230  # (mm)
    wavelength = 1.546  # (Angstrom )

    first_q = 0.0016  # (1/ Angstrom)
    delta_q = 2e-4  # (1/ Angstrom)
    step_q = 2e-4  # (1/ Angstrom)
    tolerance = 0
    num_qs = 8  # number of Q rings
    lag_time = 0.00130068  # (s)

    # for multiple tau analysis num_levels and num_channels
    num_levels = 3
    num_channels = 8

    # setting angles of the diffractometer
    # delta=40, theta=15, chi = 90, phi = 30, mu = 10.0, gamma=5.0
    setting_angles = np.array([0., 0., 0., 0., 0., 0.])

    # UB matrix (orientation matrix) 3x3 matrix
    ub_mat = np.identity(3)

    # hkl values for all the pixels
    hkl_val = recip.process_to_q(setting_angles, detector_size,
                                 pixel_size, calibrated_center,
                                 dist_sample, wavelength, ub_mat,
                                 frame_mode=None)

    # Q values, Q indices for all pixels and Q ring edge values
    # for each ring and number of pixels for each Q ring
    q_values, q_inds, q_ring_val , \
    num_pixels = recip.q_data(hkl_val, num_qs, first_q,
                           step_q, delta_q, detector_size)

    plot_q_rings(q_inds, detector_size)

    g2 = timecorr.one_time_corr(num_levels, num_channels, num_qs, img_stack,
                                q_inds, num_pixels)
