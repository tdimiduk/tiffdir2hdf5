#!/usr/bin/python

# tiffdir2hdf5.py

# Copyright (c) 2008-2014, Christoph Gohlke
# Copyright (c) 2008-2014, The Regents of the University of California
# Produced at the Laboratory for Fluorescence Dynamics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the names of any
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""
Convert a directory of tiffs into a compressed hdf5 file

Usage: tiffdir2hdf5.py directory

"""


import numpy as np
import h5py
from glob import glob
import tifffile
import os
import sys

def load_tiff(name):
    t = tifffile.TIFFfile(name)
    d = t.asarray()
    t.close()
    return d

def load_dir(dir, g="*.tif"):
    imgs = [load_tiff(f) for f in glob(os.path.join(dir, g))]
    return np.dstack(imgs)

def save_h5(data, name):
    f = h5py.File(name, 'w')
    chunkz = min(100, data.shape[2])
    f.create_dataset('images', data=data, chunks=(64,64,chunkz), compression='gzip')

if __name__ == '__main__':
    dir = sys.argv[1]
    if len(sys.argv) > 2:
        to = sys.argv[2]
        ext = os.path.splitext(to)[1]
        if ext not in ['h5', 'hdf5']:
            to = to+'.h5'
    else:
        to = dir+'.h5'

    dir = dir.rstrip('/')
    path, name = os.path.split(dir)
    imgs = load_dir(dir)
    save_h5(imgs, os.path.join(path, name+'.h5'))
