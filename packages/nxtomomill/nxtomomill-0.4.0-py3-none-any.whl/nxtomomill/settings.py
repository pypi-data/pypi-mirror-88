# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

"""
module to convert from (bliss) .h5 to (nexus tomo compliant) .nx
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "13/05/2020"


### HDF5 settings

H5_VALID_CAMERA_NAMES = None
# now camera names are deduce using converter `get_nx_detectors`
# and `guess_nx_detector` functions. But you can provide A LIST of
# detector name (unix shell-style wildcards are managed) like
# ("pcolinux*", "basler", "frelon*", ...)

H5_ROT_ANGLE_KEYS = (
    "rotm",
    "hsrot",
    "mrsrot",
    "hrsrot",
    "srot",
    "diffrz",
)

H5_X_TRANS_KEYS = ("sx", "d3tx")
"""Keys used to find the x translation"""

H5_Y_TRANS_KEYS = ("sy", "d3ty")
"""Keys used to find the y translation"""

H5_Z_TRANS_KEYS = ("sz", "d3tz")
"""Keys used to find the z translation"""

H5_Y_ROT_KEY = "instrument/positioners/yrot"
"""Key used to find the estimated center of rotation for half acquisition"""

H5_ACQ_EXPO_TIME_KEYS = ("acq_expo_time",)

H5_INIT_TITLES = (
    "pcotomo:basic",
    "tomo:basic",
    "tomo:fullturn",
    "sequence_of_scans",
    "tomo:halfturn",
)
"""if a scan starts by one of those string then is considered as
initialization scan"""

H5_ZSERIE_INIT_TITLES = ("tomo:zseries",)
"""specific titles for zserie. Will extend H5_INIT_TITLES"""

H5_DARK_TITLES = ("dark images", "dark")
"""if a scan starts by one of those string then is considered as
dark scan"""
H5_REF_TITLES = ("reference images", "ref", "refend")
"""if a scan starts by one of those string then is considered as
reference scan"""
H5_PROJ_TITLES = ("projections", "ascan diffrz 0 180 1600 0.1")
"""if a scan starts by one of those string then is considered as
projection scan"""
H5_ALIGNMENT_TITLES = ("static images", "ascan diffrz 180 0 4 0.1")
"""if a scan starts by one of those string then is considered as
alignment scan"""

H5_X_PIXEL_SIZE = (
    "technique/optic/sample_pixel_size ",
    "technique/optic/sample_pixel_size",
    "technique/detector/pixel_size",
)
"""Possible path to th pixel size."""
# warning: we can have two cases: one with an empty space at the end or not

H5_Y_PIXEL_SIZE = (
    "technique/optic/sample_pixel_size ",
    "technique/optic/sample_pixel_size",
    "technique/detector/pixel_size",
)

### EDF settings

EDF_MOTOR_POS = "motor_pos"

EDF_MOTOR_MNE = "motor_mne"

EDF_ROT_ANGLE = "srot"

EDF_X_TRANS = "sx"

EDF_Y_TRANS = "sy"

EDF_Z_TRANS = "sz"

# EDF_TO_IGNORE = ['HST', '_slice_']
EDF_TO_IGNORE = ("_slice_",)

EDF_DARK_NAMES = ("darkend", "dark")

EDF_REFS_NAMES = ("ref", "refHST")
