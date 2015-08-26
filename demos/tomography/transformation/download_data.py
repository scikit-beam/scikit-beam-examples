"""
Run this file to download and unzip the data files for the
segmentation demonstration.

If you have already downloaded the file shale_demo_data.zip, no need to
run this script. Just unzip that file and place the data in this
directory.

In total there are four files included in the .zip. These files include two
tomography data sets, collected above and below the K-shell absorption edge
for iron (Fe), and a .yaml file for each data set. The .yaml files contain
metadata pertinent to the corresponding tomography data set.

The data sets were collected by Gabriel C. Iltis at the National Synchrotron
Light Source (NSLS), Brookhaven National Laboratory (BNL), in March of 2014.

"""

from __future__ import print_function

import sys
import os
import zipfile
import requests
from clint.textui import progress
import tempfile

def download_zip(url, path):
    r = requests.get(url, stream=True)
    temp = tempfile.NamedTemporaryFile(suffix='.zip')
    print('Downloading url --> %s\nto --> %s' % (url, temp.name))
    with open(temp.name, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                  expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    z = zipfile.ZipFile(temp)
    print("extracting to --> %s" % path)
    z.extractall(path=path)

# download to this folder
current_folder = os.sep.join(__file__.split(os.sep)[:-1])
url = 'https://www.dropbox.com/s/xpxuy9t2e9f4c9i/shale_demo_data.zip?dl=1'

if os.path.isfile('NSLS_shale_smpl-2_AbvFe.tiff') and os.path.isfile(
        'NSLS_shale_smpl-2_BlwFe.tiff'):
    conf = input('data file already exists. Delete? [y/n]')
    if conf.upper() == 'Y':
        print('deleting existing file.')
        os.remove('NSLS_shale_smpl-2_AbvFe.tiff')
        os.remove('NSLS_shale_smpl-2_BlwFe.tiff')
    else:
        sys.exit(1)

download_zip(url, current_folder)
