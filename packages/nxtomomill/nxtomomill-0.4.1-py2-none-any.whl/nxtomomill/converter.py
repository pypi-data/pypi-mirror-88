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

__authors__ = ["C. Nemoz", "H. Payno", "A.Sole"]
__license__ = "MIT"
__date__ = "28/02/2020"


from silx.utils.enum import Enum as _Enum
from tomoscan.esrf.edfscan import EDFTomoScan
from nxtomomill.utils import Progress
from nxtomomill.plugins import (
    get_plugins_instances_frm_env_var,
    get_plugins_positioners_resources,
)
from nxtomomill.settings import (
    H5_ROT_ANGLE_KEYS,
    H5_VALID_CAMERA_NAMES,
    H5_X_TRANS_KEYS,
    H5_Y_TRANS_KEYS,
    H5_Z_TRANS_KEYS,
    H5_ALIGNMENT_TITLES,
    H5_ACQ_EXPO_TIME_KEYS,
    H5_X_PIXEL_SIZE,
    H5_Y_PIXEL_SIZE,
    H5_DARK_TITLES,
    H5_INIT_TITLES,
    H5_ZSERIE_INIT_TITLES,
    H5_PROJ_TITLES,
    H5_REF_TITLES,
    H5_Y_ROT_KEY,
)
from nxtomomill.settings import (
    EDF_DARK_NAMES,
    EDF_MOTOR_MNE,
    EDF_MOTOR_POS,
    EDF_REFS_NAMES,
    EDF_ROT_ANGLE,
    EDF_TO_IGNORE,
    EDF_X_TRANS,
    EDF_Y_TRANS,
    EDF_Z_TRANS,
)
from collections import namedtuple
from tomoscan.unitsystem import metricsystem
from tomoscan.io import HDF5File
import os
import typing
import h5py

try:
    import hdf5plugin
except ImportError:
    pass
import numpy
import fabio
from nxtomomill import utils
from nxtomomill.utils import ImageKey
import fnmatch
from silx.io.utils import h5py_read_dataset
import logging

_logger = logging.getLogger(__name__)


CURRENT_OUTPUT_VERSION = 1.0


H5ScanTitles = namedtuple(
    "H5ScanTitles",
    [
        "init_titles",
        "init_zserie_titles",
        "dark_titles",
        "ref_titles",
        "proj_titles",
        "align_titles",
    ],
)

DEFAULT_SCAN_TITLES = H5ScanTitles(
    H5_INIT_TITLES,
    H5_ZSERIE_INIT_TITLES,
    H5_DARK_TITLES,
    H5_REF_TITLES,
    H5_PROJ_TITLES,
    H5_ALIGNMENT_TITLES,
)

H5FileKeys = namedtuple(
    "H5FileKeys",
    [
        "acq_expo_time_keys",
        "rot_angle_keys",
        "valid_camera_names",
        "x_trans_keys",
        "y_trans_keys",
        "z_trans_keys",
        "y_rot_key",
        "x_pixel_size",
        "y_pixel_size",
    ],
)


DEFAULT_H5_KEYS = H5FileKeys(
    H5_ACQ_EXPO_TIME_KEYS,
    H5_ROT_ANGLE_KEYS,
    H5_VALID_CAMERA_NAMES,
    H5_X_TRANS_KEYS,
    H5_Y_TRANS_KEYS,
    H5_Z_TRANS_KEYS,
    H5_Y_ROT_KEY,
    H5_X_PIXEL_SIZE,
    H5_Y_PIXEL_SIZE,
)
EDFFileKeys = namedtuple(
    "EDFFileKeys",
    [
        "motor_pos_key",
        "motor_mne_key",
        "rot_angle_key",
        "x_trans_key",
        "y_trans_key",
        "z_trans_key",
        "to_ignore",
        "dark_names",
        "ref_names",
    ],
)

DEFAULT_EDF_KEYS = EDFFileKeys(
    EDF_MOTOR_POS,
    EDF_MOTOR_MNE,
    EDF_ROT_ANGLE,
    EDF_X_TRANS,
    EDF_Y_TRANS,
    EDF_Z_TRANS,
    EDF_TO_IGNORE,
    EDF_DARK_NAMES,
    EDF_REFS_NAMES,
)


class AcquisitionStep(_Enum):
    # Warning: order of acquisition step should be same as H5ScanTitles
    INITIALIZATION = "initialization"
    DARK = "darks"
    REFERENCE = "references"
    PROJECTION = "projections"
    ALIGNMENT = "alignment projections"


def _ask_for_file_removal(file_path):
    res = input("Overwrite %s ? (Y/n)" % file_path)
    return res == "Y"


def edf_to_nx(
    scan: EDFTomoScan,
    output_file: str,
    file_extension: str,
    file_keys: EDFFileKeys = DEFAULT_EDF_KEYS,
):

    # in old data, rot ange is unknown. Compute it as a function of the proj number
    compute_rotangle = True

    fileout_h5 = utils.get_file_name(
        file_name=output_file, extension=file_extension, check=True
    )
    _logger.info("Output file will be " + fileout_h5)

    DARK_ACCUM_FACT = True
    with HDF5File(fileout_h5, "w") as h5d:
        proj_urls = scan.get_proj_urls(scan=scan.path)

        for dark_to_find in file_keys.dark_names:
            dk_urls = scan.get_darks_url(scan_path=scan.path, prefix=dark_to_find)
            if len(dk_urls) > 0:
                if dark_to_find == "dark":
                    DARK_ACCUM_FACT = False
                break
        _edf_to_ignore = list(file_keys.to_ignore)
        for refs_to_find in file_keys.ref_names:
            if refs_to_find == "ref":
                _edf_to_ignore.append("HST")
            else:
                _edf_to_ignore.remove("HST")
            refs_urls = scan.get_refs_url(
                scan_path=scan.path, prefix=refs_to_find, ignore=_edf_to_ignore
            )
            if len(refs_urls) > 0:
                break

        n_frames = len(proj_urls) + len(refs_urls) + len(dk_urls)

        # TODO: should be managed by tomoscan as well
        def getExtraInfo(scan):
            projections_urls = scan.projections
            indexes = sorted(projections_urls.keys())
            first_proj_file = projections_urls[indexes[0]]
            fid = fabio.open(first_proj_file.file_path())
            if hasattr(fid, "header"):
                hd = fid.header
            else:
                hd = fid.getHeader()
            try:
                rotangle_index = (
                    hd[file_keys.motor_mne_key]
                    .split(" ")
                    .index(file_keys.rot_angle_key)
                )
            except:
                rotangle_index = -1
            try:
                xtrans_index = (
                    hd[file_keys.motor_mne_key].split(" ").index(file_keys.x_trans_key)
                )
            except:
                xtrans_index = -1
            try:
                ytrans_index = (
                    hd[file_keys.motor_mne_key].split(" ").index(file_keys.y_trans_key)
                )
            except:
                ytrans_index = -1
            try:
                ztrans_index = (
                    hd[file_keys.motor_mne_key].split(" ").index(file_keys.z_trans_key)
                )
            except:
                ztrans_index = -1

            if hasattr(fid, "bytecode"):
                frame_type = fid.bytecode
            else:
                frame_type = fid.getByteCode()
            return frame_type, rotangle_index, xtrans_index, ytrans_index, ztrans_index

        (
            frame_type,
            rot_angle_index,
            x_trans_index,
            y_trans_index,
            z_trans_index,
        ) = getExtraInfo(scan=scan)

        data_dataset = h5d.create_dataset(
            "/entry/instrument/detector/data",
            shape=(n_frames, scan.dim_2, scan.dim_1),
            dtype=frame_type,
        )

        keys_dataset = h5d.create_dataset(
            "/entry/instrument/detector/image_key", shape=(n_frames,), dtype=numpy.int32
        )

        keys_control_dataset = h5d.create_dataset(
            "/entry/instrument/detector/image_key_control",
            shape=(n_frames,),
            dtype=numpy.int32,
        )

        h5d["/entry/sample/name"] = os.path.basename(scan.path)

        proj_angle = scan.scan_range / scan.tomo_n

        distance = scan.retrieve_information(
            scan=os.path.abspath(scan.path),
            ref_file=None,
            key="Distance",
            type_=float,
            key_aliases=["distance"],
        )

        h5d["/entry/instrument/detector/distance"] = distance
        h5d["/entry/instrument/detector/distance"].attrs["unit"] = u"m"

        pixel_size = scan.retrieve_information(
            scan=os.path.abspath(scan.path),
            ref_file=None,
            key="PixelSize",
            type_=float,
            key_aliases=["pixelSize"],
        )
        h5d["/entry/instrument/detector/x_pixel_size"] = (
            pixel_size * metricsystem.millimeter.value
        )
        h5d["/entry/instrument/detector/x_pixel_size"].attrs["unit"] = u"m"
        h5d["/entry/instrument/detector/y_pixel_size"] = (
            pixel_size * metricsystem.millimeter.value
        )
        h5d["/entry/instrument/detector/y_pixel_size"].attrs["unit"] = u"m"

        energy = scan.retrieve_information(
            scan=os.path.abspath(scan.path),
            ref_file=None,
            key="Energy",
            type_=float,
            key_aliases=["energy"],
        )
        h5d["/entry/beam/incident_energy"] = energy
        h5d["/entry/beam/incident_energy"].attrs["unit"] = u"keV"

        # rotations values
        rotation_dataset = h5d.create_dataset(
            "/entry/sample/rotation_angle", shape=(n_frames,), dtype=numpy.float32
        )
        h5d["/entry/sample/rotation_angle"].attrs["unit"] = "degree"

        # provision for centering motors
        x_dataset = h5d.create_dataset(
            "/entry/sample/x_translation", shape=(n_frames,), dtype=numpy.float32
        )
        h5d["/entry/sample/x_translation"].attrs["unit"] = "m"
        y_dataset = h5d.create_dataset(
            "/entry/sample/y_translation", shape=(n_frames,), dtype=numpy.float32
        )
        h5d["/entry/sample/y_translation"].attrs["unit"] = "m"
        z_dataset = h5d.create_dataset(
            "/entry/sample/z_translation", shape=(n_frames,), dtype=numpy.float32
        )
        h5d["/entry/sample/z_translation"].attrs["unit"] = "m"

        #  --------->  and now fill all datasets!

        nf = 0

        def read_url(url) -> tuple:
            data_slice = url.data_slice()
            if data_slice is None:
                data_slice = (0,)
            if data_slice is None or len(data_slice) != 1:
                raise ValueError(
                    "Fabio slice expect a single frame, " "but %s found" % data_slice
                )
            index = data_slice[0]
            if not isinstance(index, int):
                raise ValueError(
                    "Fabio slice expect a single integer, " "but %s found" % data_slice
                )

            try:
                fabio_file = fabio.open(url.file_path())
            except Exception:
                _logger.debug(
                    "Error while opening %s with fabio", url.file_path(), exc_info=True
                )
                raise IOError(
                    "Error while opening %s with fabio (use debug"
                    " for more information)" % url.path()
                )

            if fabio_file.nframes == 1:
                if index != 0:
                    raise ValueError(
                        "Only a single frame available. Slice %s out of range" % index
                    )
                data = fabio_file.data
                header = fabio_file.header
            else:
                data = fabio_file.getframe(index).data
                header = fabio_file.getframe(index).header

            fabio_file.close()
            fabio_file = None
            return data, header

        progress = Progress("write dark")
        progress.set_max_advancement(len(dk_urls))

        def ignore(file_name):
            for forbid in _edf_to_ignore:
                if forbid in file_name:
                    return True
            return False

        # darks

        # dark in acumulation mode?
        norm_dark = 1.0
        if scan.dark_n > 0 and DARK_ACCUM_FACT is True:
            norm_dark = len(dk_urls) / scan.dark_n
        dk_indexes = sorted(dk_urls.keys())
        progress.set_max_advancement(len(dk_urls))
        for dk_index in dk_indexes:
            dk_url = dk_urls[dk_index]
            if ignore(os.path.basename(dk_url.file_path())):
                _logger.info("ignore " + dk_url.file_path())
                continue
            data, header = read_url(dk_url)
            data_dataset[nf, :, :] = data * norm_dark
            keys_dataset[nf] = ImageKey.DARK_FIELD.value
            keys_control_dataset[nf] = ImageKey.DARK_FIELD.value

            if file_keys.motor_pos_key in header:
                str_mot_val = header[file_keys.motor_pos_key].split(" ")
                if rot_angle_index == -1:
                    rotation_dataset[nf] = 0.0
                else:
                    rotation_dataset[nf] = float(str_mot_val[rot_angle_index])
                if x_trans_index == -1:
                    x_dataset[nf] = 0.0
                else:
                    x_dataset[nf] = (
                        float(str_mot_val[x_trans_index])
                        * metricsystem.millimeter.value
                    )
                if y_trans_index == -1:
                    y_dataset[nf] = 0.0
                else:
                    y_dataset[nf] = (
                        float(str_mot_val[y_trans_index])
                        * metricsystem.millimeter.value
                    )
                if z_trans_index == -1:
                    z_dataset[nf] = 0.0
                else:
                    z_dataset[nf] = (
                        float(str_mot_val[z_trans_index])
                        * metricsystem.millimeter.value
                    )

            nf += 1
            progress.increase_advancement(i=1)

        ref_indexes = sorted(refs_urls.keys())

        ref_projs = []
        for irf in ref_indexes:
            pjnum = int(irf)
            if pjnum not in ref_projs:
                ref_projs.append(pjnum)

        # refs
        def store_refs(
            refIndexes,
            tomoN,
            projnum,
            refUrls,
            nF,
            dataDataset,
            keysDataset,
            keysCDataset,
            xDataset,
            yDataset,
            zDataset,
            rotationDataset,
            raix,
            xtix,
            ytix,
            ztix,
        ):
            nfr = nF
            progress = Progress("write refs")
            progress.set_max_advancement(len(refIndexes))
            for ref_index in refIndexes:
                int_rf = int(ref_index)
                test_val = 0
                if int_rf == projnum:
                    refUrl = refUrls[ref_index]
                    if ignore(os.path.basename(refUrl.file_path())):
                        _logger.info("ignore " + refUrl.file_path())
                        continue
                    data, header = read_url(refUrl)
                    dataDataset[nfr, :, :] = data + test_val
                    keysDataset[nfr] = ImageKey.FLAT_FIELD.value
                    keysCDataset[nfr] = ImageKey.FLAT_FIELD.value
                    if file_keys.motor_pos_key in header:
                        str_mot_val = header[file_keys.motor_pos_key].split(" ")
                        if raix == -1:
                            rotationDataset[nfr] = 0.0
                        else:
                            rotationDataset[nfr] = float(str_mot_val[raix])
                        if xtix == -1:
                            xDataset[nfr] = 0.0
                        else:
                            xDataset[nfr] = float(str_mot_val[xtix])
                        if ytix == -1:
                            yDataset[nfr] = 0.0
                        else:
                            yDataset[nfr] = float(str_mot_val[ytix])
                        if ztix == -1:
                            zDataset[nfr] = 0.0
                        else:
                            zDataset[nfr] = float(str_mot_val[ztix])

                    nfr += 1
                    progress.increase_advancement(i=1)
            return nfr

        # projections
        import datetime

        proj_indexes = sorted(proj_urls.keys())
        progress = Progress("write projections")
        progress.set_max_advancement(len(proj_indexes))
        nproj = 0
        iref_pj = 0

        for proj_index in proj_indexes:
            proj_url = proj_urls[proj_index]
            if ignore(os.path.basename(proj_url.file_path())):
                _logger.info("ignore " + proj_url.file_path())
                continue

            # store refs if the ref serial number is = projection number
            if iref_pj < len(ref_projs) and ref_projs[iref_pj] == nproj:
                nf = store_refs(
                    ref_indexes,
                    scan.tomo_n,
                    ref_projs[iref_pj],
                    refs_urls,
                    nf,
                    data_dataset,
                    keys_dataset,
                    keys_control_dataset,
                    x_dataset,
                    y_dataset,
                    z_dataset,
                    rotation_dataset,
                    rot_angle_index,
                    x_trans_index,
                    y_trans_index,
                    z_trans_index,
                )
                iref_pj += 1
            data, header = read_url(proj_url)

            data_dataset[nf, :, :] = data
            keys_dataset[nf] = ImageKey.PROJECTION.value
            keys_control_dataset[nf] = ImageKey.PROJECTION.value
            if nproj >= scan.tomo_n:
                keys_control_dataset[nf] = ImageKey.ALIGNMENT.value

            if file_keys.motor_pos_key in header:
                str_mot_val = header[file_keys.motor_pos_key].split(" ")

                # continuous scan - rot angle is unknown. Compute it
                if compute_rotangle is True and nproj < scan.tomo_n:
                    rotation_dataset[nf] = nproj * proj_angle
                else:
                    if rot_angle_index == -1:
                        rotation_dataset[nf] = 0.0
                    else:
                        rotation_dataset[nf] = float(str_mot_val[rot_angle_index])

                if x_trans_index == -1:
                    x_dataset[nf] = 0.0
                else:
                    x_dataset[nf] = float(str_mot_val[x_trans_index])
                if y_trans_index == -1:
                    y_dataset[nf] = 0.0
                else:
                    y_dataset[nf] = float(str_mot_val[y_trans_index])
                if z_trans_index == -1:
                    z_dataset[nf] = 0.0
                else:
                    z_dataset[nf] = float(str_mot_val[z_trans_index])

            nf += 1
            nproj += 1

            progress.increase_advancement(i=1)

        # store last flat if any remaining in the list
        if iref_pj < len(ref_projs):
            nf = store_refs(
                ref_indexes,
                scan.tomo_n,
                ref_projs[iref_pj],
                refs_urls,
                nf,
                data_dataset,
                keys_dataset,
                keys_control_dataset,
                x_dataset,
                y_dataset,
                z_dataset,
                rotation_dataset,
                rot_angle_index,
                x_trans_index,
                y_trans_index,
                z_trans_index,
            )

        # we can add some more NeXus look and feel
        h5d["/entry"].attrs["NX_class"] = u"NXentry"
        h5d["/entry"].attrs["definition"] = u"NXtomo"
        h5d["/entry"].attrs["version"] = CURRENT_OUTPUT_VERSION
        h5d["/entry/instrument"].attrs["NX_class"] = u"NXinstrument"
        h5d["/entry/instrument/detector"].attrs["NX_class"] = u"NXdetector"
        h5d["/entry/instrument/detector/data"].attrs["interpretation"] = u"image"
        h5d["/entry/sample"].attrs["NX_class"] = u"NXsample"

        h5d.flush()


def h5_to_nx(
    input_file_path: str,
    output_file: str,
    single_file: bool,
    file_extension: typing.Union[str, None],
    ask_before_overwrite=True,
    request_input=False,
    entries: typing.Union[typing.Iterable, None] = None,
    input_callback=None,
    file_keys=DEFAULT_H5_KEYS,
    scan_titles=DEFAULT_SCAN_TITLES,
    param_already_defined=None,
    show_progress=True,
    raise_error_if_issue=False,
    detector_sel_callback=None,
):
    """

    :param str input_file_path: file to be converted from .h5 to tomo .nx
    :param str output_file: output NXtomo compliant file
    :param bool single_file: split each sequence in a dedicated file or merge
                             them all together
    :param Union[str,None] file_extension: file extension.
    :param bool request_input: if True can ask the user some missing
                               information
    :param Union[Iterable,None]: set of entries to convert. If None will
                                 convert all the entries
    :param input_callback: possible callback function to call if an entry is
                           missing. If so should take (missing_entry, desc) as
                           parameters and return a text (that might be casted
                           according to the expected input type).
    :param detector_sel_callback: possible callback to request user to select
                                  a detector if several are provided. Should
                                  take a list of possible h5py.Group as entry.
                                  Independent of `request_input` value
    :param H5FileKeys file_keys: name of cameras, translation keys ...
    :param Union[None,dict]: parameters for which the value has been defined
                              manually by the user. Like 'energy'...
    :param bool show_progress: if True create and update an instance of
                               `Progress`
    :param bool raise_error_if_issue: if True then raise an error when
                                      the converter cannot reach some
                                      requested data. If False an warning
                                      will be write and a default value will
                                      be provided.
    :return: tuple of tuples (file_name, entry_name)
    :rtype: tuple
    :raises ValueError: if some requested data cannot be found and
                        raise_error_if_issue is True
    """
    if param_already_defined is None:
        param_already_defined = {}

    if not os.path.isfile(input_file_path):
        raise ValueError(
            "Given input file does not exists: {}" "".format(input_file_path)
        )
    if not h5py.is_hdf5(input_file_path):
        raise ValueError("Given input file is not an hdf5 file")

    if input_file_path == output_file:
        raise ValueError("input and output file are the same")

    # insert missing z entry title in the common entry title
    scan_init_titles = list(scan_titles.init_titles)
    for title in scan_titles.init_zserie_titles:
        if title not in scan_init_titles:
            scan_init_titles.append(title)
    scan_titles = H5ScanTitles(
        init_titles=scan_init_titles,
        init_zserie_titles=scan_titles.init_zserie_titles,
        dark_titles=scan_titles.dark_titles,
        ref_titles=scan_titles.ref_titles,
        proj_titles=scan_titles.proj_titles,
        align_titles=scan_titles.align_titles,
    )

    dir_name = os.path.dirname(os.path.abspath(output_file))
    if not os.path.exists(dir_name):
        os.makedirs(os.path.dirname(os.path.abspath(output_file)))
    elif os.path.exists(output_file):
        if ask_before_overwrite is False:
            _logger.warning("{} will be removed".format(output_file))
            _logger.info("remove {}".format(output_file))
            os.remove(output_file)
        elif not _ask_for_file_removal(output_file):
            _logger.info("unable to overwrite {}, exit".format(output_file))
            exit(0)
        else:
            os.remove(output_file)
    if not os.access(dir_name, os.W_OK):
        _logger.error("You don't have rights to write on {}" "".format(dir_name))
        exit(0)
    try:
        plugins = get_plugins_instances_frm_env_var()
    except Exception as e:
        _logger.info(e)
        plugins = []

    res = []
    with HDF5File(input_file_path, "r") as h5d:

        def sort_fct(node):
            node_to_treat = h5d.get(node, getlink=True)
            if isinstance(node_to_treat, (h5py.ExternalLink, h5py.SoftLink)):
                return float(node_to_treat.path.split("/")[-1])
            return float(node)

        groups = list(h5d.keys())
        groups.sort(key=sort_fct)
        # step 1: deduce acquisitions
        if show_progress:
            progress = Progress("parse sequences")
            progress.set_max_advancement(len(h5d.keys()))
        else:
            progress = None

        # step 1: pre processing: group scan together
        acquisitions = []
        # list of acquisitions. Once process each of those acquisition will
        # create one 'scan'
        current_acquisition = None
        for group_name in groups:
            _logger.debug("parse {}".format(group_name))
            entry = h5d[group_name]
            entry_type = _get_entry_type(entry=entry, scan_titles=scan_titles)

            if entry_type is AcquisitionStep.INITIALIZATION:
                if _is_z_series(entry=entry, scan_titles=scan_titles):
                    current_acquisition = _ZSeriesBaseAcquisition(
                        entry,
                        file_keys,
                        scan_titles=scan_titles,
                        param_already_defined=param_already_defined,
                        raise_error_if_issue=raise_error_if_issue,
                        detector_sel_callback=detector_sel_callback,
                    )
                else:
                    current_acquisition = _StandardBaseAcquisition(
                        entry,
                        file_keys,
                        scan_titles=scan_titles,
                        param_already_defined=param_already_defined,
                        raise_error_if_issue=raise_error_if_issue,
                        detector_sel_callback=detector_sel_callback,
                    )
                acquisitions.append(current_acquisition)
            elif current_acquisition is not None:
                current_acquisition.register_step(entry)
            if progress is not None:
                progress.increase_advancement()
        # step 2: get _StandardAcquisition from Zseries if any
        tmp_acquisitions = acquisitions
        acquisitions = []
        for acquisition in tmp_acquisitions:
            if isinstance(acquisition, _StandardBaseAcquisition):
                acquisitions.append(acquisition)
            elif isinstance(acquisition, _ZSeriesBaseAcquisition):
                acquisitions.extend(acquisition.getStandardSubAcquisitions())
            else:
                raise TypeError(
                    "Acquisition type {} not handled".foramt(type(acquisition))
                )

        # step2: processing
        possible_extensions = (".hdf5", ".h5", ".nx", ".nexus")
        output_file_basename = os.path.basename(output_file)
        file_extension_ = None
        for possible_extension in possible_extensions:
            if output_file_basename.endswith(possible_extension):
                output_file_basename.rstrip(possible_extension)
                file_extension_ = possible_extension

        # step 2: check validity of all the acquisition sequence (consistency)
        # or write output
        if show_progress:
            progress = Progress("write sequences")
            progress.set_max_advancement(len(acquisitions))
        for i_acquisition, acquisition in enumerate(acquisitions):
            if (
                entries is not None
                and acquisition.initialization_entry.name not in entries
            ):
                continue
            entry = "entry" + str(i_acquisition).zfill(4)
            if single_file or len(acquisitions) == 1:
                en_output_file = output_file
            else:
                ext = file_extension_ or file_extension
                file_name = (
                    output_file_basename + "_" + str(i_acquisition).zfill(4) + ext
                )
                en_output_file = os.path.join(os.path.dirname(output_file), file_name)

                if os.path.exists(en_output_file):
                    if ask_before_overwrite is False:
                        _logger.warning(en_output_file + " will be removed")
                        _logger.info("remove " + en_output_file)
                        os.remove(en_output_file)
                    elif _ask_for_file_removal(en_output_file) is False:
                        _logger.info(
                            "unable to overwrite {}, exit".format(en_output_file)
                        )
                        exit(0)
                    else:
                        os.remove(en_output_file)

            try:
                acquisition.write_as_nxtomo(
                    output_file=en_output_file,
                    data_path=entry,
                    input_file_path=input_file_path,
                    request_input=request_input,
                    input_callback=input_callback,
                    plugins=plugins,
                )
                # if split files create a master file with link to those entries
                if single_file is False and len(acquisitions) > 1:
                    _logger.info("create link in %s" % output_file)
                    with HDF5File(output_file, "a") as master_file:
                        link_file = os.path.relpath(
                            en_output_file, os.path.dirname(output_file)
                        )
                        master_file[entry] = h5py.ExternalLink(link_file, entry)
                    res.append((en_output_file, entry))
                else:
                    res.append((en_output_file, entry))
            except Exception as e:
                if raise_error_if_issue:
                    raise e
                else:
                    _logger.error(
                        "Fails to write %s. Error is %s"
                        % (acquisition.initialization_entry.name, str(e))
                    )
            if progress is not None:
                progress.increase_advancement()
    return tuple(res)


def get_nx_detectors(node: h5py.Group) -> tuple:
    """

    :param h5py.Group node: node to inspect
    :return: tuple of NXdetector (h5py.Group) contained in `node`
             (expected to be the `instrument` group)
    :rtype: tuple
    """
    if not isinstance(node, h5py.Group):
        raise TypeError("node should be an instance of h5py.Group")
    nx_detectors = []
    for _, subnode in node.items():
        if isinstance(subnode, h5py.Group) and "NX_class" in subnode.attrs:
            if subnode.attrs["NX_class"] == "NXdetector":
                if "data" in subnode and hasattr(subnode["data"], "ndim"):
                    if subnode["data"].ndim == 3:
                        nx_detectors.append(subnode)
    nx_detectors = sorted(nx_detectors, key=lambda det: det.name)
    return tuple(nx_detectors)


def guess_nx_detector(node: h5py.Group) -> tuple:
    """
    Try to guess what can be an nx_detector without using the "NXdetector"
    NX_class attribute. Expect to find a 3D dataset named 'data' under
    a subnode
    """
    if not isinstance(node, h5py.Group):
        raise TypeError("node should be an instance of h5py.Group")
    nx_detectors = []
    for _, subnode in node.items():
        if isinstance(subnode, h5py.Group) and "data" in subnode:
            if isinstance(subnode["data"], h5py.Dataset) and subnode["data"].ndim == 3:
                nx_detectors.append(subnode)

    nx_detectors = sorted(nx_detectors, key=lambda det: det.name)
    return tuple(nx_detectors)


def _get_entry_type(
    entry: h5py.Group, scan_titles
) -> typing.Union[None, AcquisitionStep]:
    try:
        title = h5py_read_dataset(entry["title"])
    except Exception as e:
        _logger.error("fail to find title for %s, skip this group" % entry.name)

    init_titles = list(scan_titles.init_titles)
    init_titles.extend(scan_titles.init_zserie_titles)

    step_titles = {
        AcquisitionStep.INITIALIZATION: init_titles,
        AcquisitionStep.DARK: scan_titles.dark_titles,
        AcquisitionStep.REFERENCE: scan_titles.ref_titles,
        AcquisitionStep.PROJECTION: scan_titles.proj_titles,
        AcquisitionStep.ALIGNMENT: scan_titles.align_titles,
    }

    for step, titles in step_titles.items():
        for title_start in titles:
            if title.startswith(title_start):
                return step
    return None


def _is_z_series(entry: h5py.Group, scan_titles) -> bool:
    try:
        title = h5py_read_dataset(entry["title"])
    except Exception as e:
        return False
    else:
        return title in scan_titles.init_zserie_titles


def get_bliss_tomo_entries(input_file_path, scan_titles):
    """Util function. Used by tomwer for example"""

    with HDF5File(input_file_path, "r") as h5d:
        acquisitions = []

        for group_name in h5d.keys():
            _logger.debug("parse %s" % group_name)
            entry = h5d[group_name]
            entry_type = _get_entry_type(entry=entry, scan_titles=scan_titles)

            if entry_type is AcquisitionStep.INITIALIZATION:
                acquisitions.append(entry.name)
        return acquisitions


class _BaseAcquisition:
    """
    Util class to group hdf5 group together and to write the data
    Nexus / NXtomo compliant
    """

    _SCAN_NUMBER_PATH = "measurement/scan_numbers"

    _ENERGY_PATH = "technique/scan/energy"

    _DISTANCE_PATH = "technique/scan/sample_detector_distance"

    _NAME_PATH = "technique/scan/name"

    _FOV_PATH = "technique/scan/field_of_view"

    def __init__(
        self,
        entry: h5py.Group,
        file_keys: H5FileKeys,
        scan_titles,
        param_already_defined,
        raise_error_if_issue,
        detector_sel_callback,
    ):
        self._raise_error_if_issue = raise_error_if_issue
        self._detector_sel_callback = detector_sel_callback
        self._initialization_entry = entry
        self._indexes = entry[_BaseAcquisition._SCAN_NUMBER_PATH]
        self._indexes_str = tuple(
            [str(index) for index in entry[_BaseAcquisition._SCAN_NUMBER_PATH]]
        )
        self._file_keys = file_keys
        self._scan_titles = scan_titles
        self._param_already_defined = param_already_defined
        """user can have defined already some parameter values as energy.
        The idea is to avoid asking him if """

    @property
    def raise_error_if_issue(self):
        """
        Should we raise an error if we encounter or an issue or should we
        just log an error message
        """
        return self._raise_error_if_issue

    @property
    def initialization_entry(self):
        return self._initialization_entry

    def register_step(self, entry: h5py.Group) -> None:
        """
        Add a bliss entry to the acquisition
        :param entry:
        """
        raise NotImplementedError("Base class")

    @staticmethod
    def _get_unit(node: h5py.Dataset, default_unit):
        """Simple process to retrieve unit from an attribute"""
        if "unit" in node.attrs:
            return node.attrs["unit"]
        elif "units" in node.attrs:
            return node.attrs["units"]
        else:
            _logger.info(
                "no unit found for %s, take default unit: %s"
                "" % (node.name, default_unit)
            )
            return default_unit

    def _get_instrument_node(self, entry_node) -> h5py.Group:
        return entry_node["instrument"]

    def _get_positioners_node(self, entry_node):
        return self._get_instrument_node(entry_node)["positioners"]

    def _get_rotation_angle(self, root_node, n_frame) -> tuple:
        """return the list of rotation angle for each frame"""
        for grp in self._get_positioners_node(root_node), root_node:
            try:
                angles, unit = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=self._file_keys.rot_angle_keys,
                    info_retrieve="rotation angle",
                    expected_unit="degree",
                )
            except (ValueError, KeyError):
                pass
            else:
                return angles, unit

        mess = "Unable to find rotation angle on entry {}" "".format(
            self.initialization_entry
        )
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return [0] * n_frame, "degree"

    def _get_x_translation(self, root_node, n_frame) -> tuple:
        """return the list of translation for each frame"""
        for grp in self._get_positioners_node(root_node), root_node:
            try:
                x_tr, unit = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=self._file_keys.x_trans_keys,
                    info_retrieve="x translation",
                    expected_unit="mm",
                )
                x_tr = (
                    numpy.asarray(x_tr)
                    * metricsystem.MetricSystem.from_value(unit).value
                )
            except (ValueError, KeyError):
                pass
            else:
                return x_tr, "m"

        mess = "Unable to find x translation on entry {}" "".format(
            self.initialization_entry
        )
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, "m"

    def _get_y_translation(self, root_node, n_frame) -> tuple:
        """return the list of translation for each frame"""
        for grp in self._get_positioners_node(root_node), root_node:
            try:
                y_tr, unit = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=self._file_keys.y_trans_keys,
                    info_retrieve="y translation",
                    expected_unit="mm",
                )
                y_tr = (
                    numpy.asarray(y_tr)
                    * metricsystem.MetricSystem.from_value(unit).value
                )
            except (ValueError, KeyError):
                pass
            else:
                return y_tr, "m"

        mess = "Unable to find y translation on entry {}" "".format(
            self.initialization_entry
        )
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, "m"

    def _get_z_translation(self, root_node, n_frame) -> tuple:
        """return the list of translation for each frame"""
        for grp in self._get_positioners_node(root_node), root_node:
            try:
                z_tr, unit = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=self._file_keys.z_trans_keys,
                    info_retrieve="z translation",
                    expected_unit="mm",
                )
                z_tr = (
                    numpy.asarray(z_tr)
                    * metricsystem.MetricSystem.from_value(unit).value
                )
            except (ValueError, KeyError):
                pass
            else:
                return z_tr, "m"

        mess = "Unable to find z translation on entry {}" "".format(
            self.initialization_entry
        )
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, "m"

    def _get_expo_time(self, root_node, n_frame, detector_node) -> tuple:
        """return expo time for each frame"""
        for grp in detector_node["acq_parameters"], root_node:
            try:
                expo, unit = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=self._file_keys.acq_expo_time_keys,
                    info_retrieve="exposure time",
                    expected_unit="s",
                )
            except (ValueError, KeyError):
                pass
            else:
                return expo, unit

        mess = "Unable to find frame exposure time on entry {}" "".format(
            self.initialization_entry
        )
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, "s"

    def _get_plugin_pos_resource(self, root_node, resource_name, n_frame):
        """Reach a path provided by a plugin. In this case units are not
        managed"""
        for grp in self._get_positioners_node(root_node), root_node:
            try:
                values, _ = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=(resource_name,),
                    info_retrieve=resource_name,
                    expected_unit=None,
                )
            except (ValueError, KeyError):
                pass
            else:
                return values, None
        mess = "Unable to find {} on entry {}".format(
            resource_name, self.initialization_entry
        )
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, None

    @staticmethod
    def _get_node_values_for_frame_array(
        node: h5py.Group,
        n_frame: typing.Union[int, None],
        keys: typing.Iterable,
        info_retrieve,
        expected_unit,
    ):
        def get_values():
            for possible_key in keys:
                if possible_key in node:
                    values = h5py_read_dataset(node[possible_key])
                    unit = _BaseAcquisition._get_unit(
                        node[possible_key], default_unit=expected_unit
                    )
                    if isinstance(values, str) and values == "*DIS*":
                        continue
                    return values, unit

            return None, None

        values, unit = get_values()
        if values is None:
            raise ValueError(
                "Unable to retrieve %s for %s" % (info_retrieve, node.name)
            )
        elif numpy.isscalar(values):
            if n_frame is None:
                return (values,), unit
            return numpy.array([values] * n_frame), unit
        elif n_frame is not None and len(values) == n_frame:
            return values.tolist(), unit
        elif n_frame is not None and len(values) == (n_frame + 1):
            # for now we can have one extra position for rotation, x_translation...
            # because saved after the last projection. It is recording the
            # motor position. For example in this case: 1 is the motor movement
            # (saved) and 2 is the acquisition
            #
            #  1     2    1    2     1
            #      -----     -----
            # -----     -----     -----
            #
            return values[:-1].tolist(), unit
        elif n_frame is None:
            return values[:-1].tolist(), unit
        else:
            raise ValueError(
                "incoherent number of angle position compare to " "the number of frame"
            )


class _StandardBaseAcquisition(_BaseAcquisition):
    """
    A standard acquisition where all registered scan are connected to
    group an NXtomo entry
    """

    def __init__(
        self,
        entry: h5py.Group,
        file_keys: H5FileKeys,
        scan_titles,
        param_already_defined,
        raise_error_if_issue,
        detector_sel_callback,
    ):
        super().__init__(
            entry=entry,
            file_keys=file_keys,
            scan_titles=scan_titles,
            param_already_defined=param_already_defined,
            raise_error_if_issue=raise_error_if_issue,
            detector_sel_callback=detector_sel_callback,
        )
        self._registered_entries = []

        # variables set by the `_preprocess_frames` function
        self._data = None
        """frames as a virtual dataset"""
        self._image_key = None
        """list of image keys"""
        self._image_key_control = None
        """list of image keys"""
        self._rotation_angle = None
        """list of rotation angles"""
        self._x_translation = None
        """x_translation"""
        self._y_translation = None
        """y_translation"""
        self._z_translation = None
        """z_translation"""
        self._n_frames = None
        self._dim_1 = None
        self._dim_2 = None
        self._data_type = None
        self._virtual_sources = None
        self._acq_expo_time = None
        self._input_fct = None
        self._plugins = []
        self._plugins_pos_resources = {}

    def set_plugins(self, plugins):
        """

        :param list plugins: list of plugins to call
        """
        self._plugins = plugins
        _plugins_req_resources = get_plugins_positioners_resources(plugins)
        self._plugins_pos_resources = {}
        for requested_resource in _plugins_req_resources:
            self._plugins_pos_resources[requested_resource] = []

    @property
    def image_key(self):
        return self._image_key

    @property
    def image_key_control(self):
        return self._image_key_control

    @property
    def rotation_angle(self):
        return self._rotation_angle

    @property
    def x_translation(self):
        return self._x_translation

    @property
    def y_translation(self):
        return self._y_translation

    @property
    def z_translation(self):
        return self._z_translation

    @property
    def n_frames(self):
        return self._n_frames

    @property
    def dim_1(self):
        return self._dim_1

    @property
    def dim_2(self):
        return self._dim_2

    @property
    def data_type(self):
        return self._data_type

    @property
    def expo_time(self):
        return self._acq_expo_time

    def register_step(self, entry: h5py.Group) -> None:
        """

        :param entry:
        """
        assert (
            _get_entry_type(entry=entry, scan_titles=self._scan_titles)
            is not AcquisitionStep.INITIALIZATION
        )
        if entry.name.startswith(self._indexes_str):
            raise ValueError("The %s entry is not part of this sequence" % entry.name)

        if _get_entry_type(entry=entry, scan_titles=self._scan_titles) is None:
            _logger.info("%s not recognized, skip it" % entry.name)
        else:
            self._registered_entries.append(entry)

    def _preprocess_frames(self, input_file_path, output_file):
        """parse all frames of the different steps and retrieve data,
        image_key..."""
        # TODO: make sure those are ordered or use the 'scan_numbers' ?
        n_frames = 0
        dim_1 = None
        dim_2 = None
        data_type = None
        _x_translation = []
        _y_translation = []
        _z_translation = []
        _image_key = []
        _image_key_control = []
        _rotation_angle = []
        _virtual_sources = []
        _virtual_sources_len = []
        # list of data virtual source for the virtual dataset
        _acq_expo_time = []

        for entry in self._registered_entries:
            type_ = _get_entry_type(entry, self._scan_titles)
            if type_ is AcquisitionStep.INITIALIZATION:
                raise RuntimeError(
                    "no initialization should be registered."
                    "There should be only one per acquisition."
                )
            if type_ is AcquisitionStep.PROJECTION:
                image_key_control = ImageKey.PROJECTION
                image_key = ImageKey.PROJECTION
            elif type_ is AcquisitionStep.ALIGNMENT:
                image_key_control = ImageKey.ALIGNMENT
                image_key = ImageKey.PROJECTION
            elif type_ is AcquisitionStep.DARK:
                image_key_control = ImageKey.DARK_FIELD
                image_key = ImageKey.DARK_FIELD
            elif type_ is AcquisitionStep.REFERENCE:
                image_key_control = ImageKey.FLAT_FIELD
                image_key = ImageKey.FLAT_FIELD
            else:
                raise ValueError("entry not recognized: " + entry.name)

            if "instrument" not in entry:
                _logger.error(
                    "no measurement group found in %s, unable to"
                    "retrieve frames" % entry.name
                )
                continue

            instrument_grp = entry["instrument"]

            # if we need to guess detector name(s)
            if self._file_keys.valid_camera_names is None:
                det_grps = get_nx_detectors(instrument_grp)
                det_grps = [grp.name.split("/")[-1] for grp in det_grps]
                if len(det_grps) > 0:
                    _logger.info(
                        "{} detector found from NX_class attribute".format(
                            len(det_grps)
                        )
                    )
                    if len(det_grps) > 1:
                        # if an option: pick the first one once orderered
                        # else ask user
                        if self._detector_sel_callback is None:
                            sel_det = det_grps[0]
                            _logger.warning(
                                "several detector found. Only one"
                                "is managed for now. Will pick {}"
                                "".format(sel_det)
                            )
                        else:
                            sel_det = self._detector_sel_callback(det_grps)
                            if sel_det is None:
                                _logger.warning("no detector given, avoid conversion")
                            elif not isinstance(sel_det, h5py.Group):
                                raise TypeError(
                                    "Return detector should be " "a h5py.Group"
                                )
                        det_grps = (sel_det,)
                else:
                    det_grps = guess_nx_detector(instrument_grp)
                    det_grps = [grp.name.split("/")[-1] for grp in det_grps]
                    if len(det_grps) > 1:
                        # if an option: pick the first one once orderered
                        # else ask user
                        raise NotImplementedError()
                # update valid camera names
                self._file_keys = H5FileKeys(
                    acq_expo_time_keys=self._file_keys.acq_expo_time_keys,
                    rot_angle_keys=self._file_keys.rot_angle_keys,
                    valid_camera_names=det_grps,
                    x_trans_keys=self._file_keys.x_trans_keys,
                    y_trans_keys=self._file_keys.y_trans_keys,
                    z_trans_keys=self._file_keys.z_trans_keys,
                    y_rot_key=self._file_keys.y_rot_key,
                    x_pixel_size=self._file_keys.x_pixel_size,
                    y_pixel_size=self._file_keys.y_pixel_size,
                )

            for key, det_grp in instrument_grp.items():
                if (
                    "NX_class" in instrument_grp[key].attrs
                    and instrument_grp[key].attrs["NX_class"] == "NXdetector"
                ):
                    _logger.debug(
                        "Found one detector at %s for %s." "" % (key, entry.name)
                    )

                    def detector_is_valid(det_name):
                        assert isinstance(det_name, str)
                        for vcm in self._file_keys.valid_camera_names:
                            if fnmatch.fnmatch(det_name, vcm):
                                return True
                        return False

                    if not detector_is_valid(key):
                        _logger.info("ignore %s, not a `valid` camera name" % key)
                        continue

                    detector_node = instrument_grp[key]
                    if "data_cast" in detector_node:
                        _logger.warning(
                            "!!! looks like this data has been cast. Take cast data for %s!!!"
                            % detector_node
                        )
                        data_dataset = detector_node["data_cast"]
                    else:
                        data_dataset = detector_node["data"]
                        data_name = "/".join((detector_node.name, "data"))
                    if data_dataset.ndim == 2:
                        shape = (1, data_dataset.shape[0], data_dataset.shape[1])
                    elif data_dataset.ndim != 3:
                        raise ValueError(
                            "dataset %s is expected to be 3D when %sD found"
                            % (data_name, data_dataset.ndim)
                        )
                    else:
                        shape = data_dataset.shape
                    n_frame = shape[0]
                    n_frames += n_frame
                    if dim_1 is None:
                        dim_2 = shape[1]
                        dim_1 = shape[2]
                    else:
                        if dim_1 != shape[2] or dim_2 != shape[1]:
                            raise ValueError("Inconsistency in detector shapes")
                    if data_type is None:
                        data_type = data_dataset.dtype
                    elif data_type != data_dataset.dtype:
                        raise ValueError(
                            "detector frames have incoherent " "data types"
                        )

                    # update image_key and image_key_control
                    # Note: for now there is no image_key on the master file
                    # should be added later.
                    _image_key_control.extend([image_key_control.value] * n_frame)
                    _image_key.extend([image_key.value] * n_frame)
                    # create virtual source (getting ready for writing)
                    rel_input = os.path.relpath(
                        input_file_path, os.path.dirname(output_file)
                    )

                    v_source = h5py.VirtualSource(
                        rel_input, data_dataset.name, data_dataset.shape
                    )
                    _virtual_sources.append(v_source)
                    _virtual_sources_len.append(n_frame)
                    # store rotation
                    rots = self._get_rotation_angle(root_node=entry, n_frame=n_frame)[0]
                    _rotation_angle.extend(rots)
                    # store translation
                    _x_translation.extend(
                        self._get_x_translation(root_node=entry, n_frame=n_frame)[0]
                    )
                    _y_translation.extend(
                        self._get_y_translation(root_node=entry, n_frame=n_frame)[0]
                    )
                    _z_translation.extend(
                        self._get_z_translation(root_node=entry, n_frame=n_frame)[0]
                    )

                    # store acquisition time
                    _acq_expo_time.extend(
                        self._get_expo_time(
                            root_node=entry,
                            detector_node=detector_node,
                            n_frame=n_frame,
                        )[0]
                    )
                    for resource_name in self._plugins_pos_resources:
                        self._plugins_pos_resources[resource_name].extend(
                            self._get_plugin_pos_resource(
                                root_node=entry,
                                resource_name=resource_name,
                                n_frame=n_frame,
                            )[0]
                        )

        # store result if processing go through
        self._x_translation = _x_translation
        self._y_translation = _y_translation
        self._z_translation = _z_translation
        self._image_key = tuple(_image_key)
        self._image_key_control = tuple(_image_key_control)
        self._rotation_angle = _rotation_angle
        self._n_frames = n_frames
        self._data_type = data_type
        self._virtual_sources = _virtual_sources
        self._dim_1 = dim_1
        self._dim_2 = dim_2
        self._virtual_sources_len = _virtual_sources_len
        self._acq_expo_time = _acq_expo_time
        for plugin in self._plugins:
            plugin.set_positioners_infos(self._plugins_pos_resources)

    def _write_beam(self, root_node, request_input, input_callback):
        beam_node = root_node.create_group("beam")
        if "energy" in self._param_already_defined:
            energy = self._param_already_defined["energy"]
            unit = "kev"
        else:
            energy, unit = self._get_energy(
                ask_if_0=request_input, input_callback=input_callback
            )
        if energy is not None:
            beam_node["incident_energy"] = energy
            beam_node["incident_energy"].attrs["unit"] = unit

    def _write_instrument(self, root_node):
        instrument_node = root_node.create_group("instrument")
        instrument_node.attrs["NX_class"] = "NXinstrument"
        instrument_node.attrs["default"] = "detector"

        detector_node = instrument_node.create_group("detector")
        detector_node.attrs["NX_class"] = "NXdetector"
        # write data
        if self._virtual_sources is not None:
            self._create_data_virtual_dataset(detector_node)
        if self.image_key is not None:
            detector_node["image_key"] = self.image_key
        if self.image_key_control is not None:
            detector_node["image_key_control"] = self.image_key_control
        if self._acq_expo_time is not None:
            detector_node["count_time"] = self._acq_expo_time
            detector_node["count_time"].attrs["unit"] = "s"
        # write distance
        distance, unit = self._get_distance()
        if distance is not None:
            detector_node["distance"] = distance
            detector_node["distance"].attrs["unit"] = unit
        # write x and y pixel size
        # if magnified pixel size is found then we right this value.
        # otherwise will take pixel size (if found)
        x_pixel_size, unit = self._get_pixel_size("x")
        if x_pixel_size is not None:
            detector_node["x_pixel_size"] = x_pixel_size
            detector_node["x_pixel_size"].attrs["unit"] = unit

        y_pixel_size, unit = self._get_pixel_size("y")
        if y_pixel_size is not None:
            detector_node["y_pixel_size"] = y_pixel_size
            detector_node["y_pixel_size"].attrs["unit"] = unit
        # write field of view
        fov = self._get_field_of_fiew()
        if fov is not None:
            detector_node["field_of_view"] = fov
            if fov.lower() == "half":
                estimated_cor, unit = self._get_estimated_cor_from_motor(
                    pixel_size=y_pixel_size
                )
                if estimated_cor is not None:
                    detector_node["estimated_cor_from_motor"] = estimated_cor
                    detector_node["estimated_cor_from_motor"].attrs["unit"] = unit

    def _create_data_virtual_dataset(self, detector_node):
        if (
            self.n_frames is None
            or self.dim_1 is None
            or self.dim_2 is None
            or self.data_type is None
        ):
            if self.n_frames is None:
                _logger.error("unable to get the number of frames")
            if self.dim_1 is None:
                _logger.error("unable to get frame dim_1")
            if self.dim_2 is None:
                _logger.error("unable to get frame dim_2")
            if self.data_type is None:
                _logger.error("unable to get data type")
            raise ValueError(
                "Preprocessing could not deduce all information "
                "for creating the `data` virtual dataset"
            )
        layout = h5py.VirtualLayout(
            shape=(self.n_frames, self.dim_2, self.dim_1), dtype=self.data_type
        )
        last = 0
        for v_source, vs_len in zip(self._virtual_sources, self._virtual_sources_len):
            layout[last : vs_len + last] = v_source
            last += vs_len

        detector_node.create_virtual_dataset("data", layout)
        detector_node.attrs["NX_class"] = "NXdata"
        detector_node.attrs["signal"] = "data"
        detector_node["data"].attrs["interpretation"] = "image"

    def _check_has_metadata(self):
        if self._initialization_entry is None:
            raise ValueError(
                "no initialization entry specify, unable to" "retrieve energy"
            )

    def _write_sample(self, root_node):
        sample_node = root_node.create_group("sample")
        sample_node.attrs["NX_class"] = u"NXsample"
        name = self._get_name()
        if name:
            sample_node["name"] = name
        if self.rotation_angle is not None:
            sample_node["rotation_angle"] = self.rotation_angle
            sample_node["rotation_angle"].attrs["unit"] = "degree"
        if self.x_translation is not None:
            sample_node["x_translation"] = self.x_translation
            sample_node["x_translation"].attrs["unit"] = "m"
        if self.y_translation is not None:
            sample_node["y_translation"] = self.y_translation
            sample_node["y_translation"].attrs["unit"] = "m"
        if self.z_translation is not None:
            sample_node["z_translation"] = self.z_translation
            sample_node["z_translation"].attrs["unit"] = "m"

    def _write_plugins_output(self, root_node):
        for plugin in self._plugins:
            instrument_node = root_node["instrument"]
            detector_node = instrument_node["detector"]
            detector_node.attrs["NX_class"] = u"NXdetector"
            plugin.write(
                root_node=root_node,
                sample_node=root_node["sample"],
                detector_node=detector_node,
                beam_node=root_node["beam"],
            )

    def _get_name(self):
        """return name of the acquisition"""
        self._check_has_metadata()
        if self._NAME_PATH in self._initialization_entry:
            return h5py_read_dataset(self._initialization_entry[self._NAME_PATH])
        else:
            _logger.warning(
                "No name describing the acquisition has been found,"
                " Name dataset will be skip"
            )
            return None

    def _get_energy(self, ask_if_0, input_callback):
        """return tuple(energy, unit)"""
        self._check_has_metadata()
        if self._ENERGY_PATH in self._initialization_entry:
            energy = h5py_read_dataset(self._initialization_entry[self._ENERGY_PATH])
            unit = self._get_unit(
                self._initialization_entry[self._ENERGY_PATH], default_unit="kev"
            )
            if energy == 0 and ask_if_0:
                desc = (
                    "Energy has not been registered. Please enter "
                    "incoming beam energy (in kev):"
                )
                if input_callback is None:
                    en = input(desc)
                else:
                    en = input_callback("energy", desc)
                if energy is not None:
                    energy = float(en)
            return energy, unit
        else:
            mess = "unable to find energy for entry {}.".format(
                self.initialization_entry
            )
            if self.raise_error_if_issue:
                raise ValueError(mess)
            else:
                mess += " Default value will be set (19kev)"
                _logger.warning(mess)
                return 19.0, "kev"

    def _get_distance(self):
        """return tuple(distance, unit)"""
        self._check_has_metadata()
        if self._DISTANCE_PATH in self._initialization_entry:
            node = self.initialization_entry[self._DISTANCE_PATH]
            distance = h5py_read_dataset(node)
            unit = self._get_unit(node, default_unit="cm")
            # convert to meter
            distance = distance * metricsystem.MetricSystem.from_value(unit).value
            return distance, "m"
        else:
            mess = "unable to find distance for entry {}.".format(
                self.initialization_entry
            )
            if self.raise_error_if_issue:
                raise ValueError(mess)
            else:
                mess += "Default value will be set (1m)"
                _logger.warning(mess)
                return 1.0, "m"

    def _get_pixel_size(self, axis):
        """return tuple(pixel_size, unit)"""
        assert axis in ("x", "y")
        self._check_has_metadata()
        keys = (
            self._file_keys.x_pixel_size
            if axis == "x"
            else self._file_keys.y_pixel_size
        )
        for key in keys:
            if key in self._initialization_entry:
                node = self.initialization_entry[key]
                node_item = h5py_read_dataset(node)
                # if the pixel size is provided as x, y
                if isinstance(node_item, numpy.ndarray):
                    if len(node_item) > 1 and axis == "y":
                        size_ = node_item[1]
                    else:
                        size_ = node_item[0]
                # if this is a single value
                else:
                    size_ = node_item
                unit = self._get_unit(node, default_unit="micrometer")
                # convert to meter
                size_ = size_ * metricsystem.MetricSystem.from_value(unit).value
                return size_, "m"

        mess = "unable to find {} pixel size for entry {}".format(
            axis, self.initialization_entry
        )
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set to 10-6m"
            return 10e-6, "m"

    def _get_field_of_fiew(self):
        if self._FOV_PATH in self._initialization_entry:
            return h5py_read_dataset(self.initialization_entry[self._FOV_PATH])
        else:
            mess = (
                "unable to find information regarding field of view for"
                " entry {}".format(self.initialization_entry)
            )
            if self.raise_error_if_issue:
                raise ValueError(mess)
            else:
                mess += "set it to default value (Full)"
                _logger.warning(mess)
                return "Full"

    def _get_estimated_cor_from_motor(self, pixel_size):
        """given pixel is expected to be given in meter"""
        if self._file_keys.y_rot_key in self._initialization_entry:
            y_rot = h5py_read_dataset(
                self.initialization_entry[self._file_keys.y_rot_key]
            )
        else:
            _logger.warning(
                "unable to find information on positioner {}".format(
                    self._file_keys.y_rot_key
                )
            )
            return None, None
        # y_rot is provided in mm when pixel size is in meter.
        y_rot = y_rot * metricsystem.millimeter.value

        if pixel_size is None:
            mess = (
                "pixel size is required to estimate the cor from the "
                "motor position on pixels"
            )
            if self.raise_error_if_issue:
                raise ValueError(mess)
            else:
                mess += " Set default value (0m)"
                _logger.warning(mess)
                return 0, "m"
        else:
            return y_rot / pixel_size, "pixels"

    def write_as_nxtomo(
        self,
        output_file: str,
        data_path: str,
        input_file_path: str,
        request_input: bool,
        plugins,
        input_callback=None,
    ) -> None:
        """
        write the current sequence in an NXtomo like

        :param str output_file: destination file
        :param str data_path: path to store the data in the destination file
        :param str input_file_path: hdf5 source file
        :param bool request_input: if some entries are missing should we ask
                                   the user for input
        :param list plugins: plugins to process
        :param input_callback: if provided then will call this callback
                               function with  (missing_entry, desc) instead of
                               input
        """
        _logger.info(
            "write data of %s to %s"
            % (self.initialization_entry.name, output_file + "::/" + data_path)
        )
        self.set_plugins(plugins)

        # work on absolute path. The conversion to relative path and
        # then to absolute path is a trick in case there is some 'mounted'
        # directory exposed differently. Like '/mnt/multipath-shares/tmp_14_days'
        input_file_path = os.path.abspath(os.path.relpath(input_file_path, os.getcwd()))
        output_file = os.path.abspath(os.path.relpath(output_file, os.getcwd()))
        input_file_path = os.path.realpath(input_file_path)
        output_file = os.path.realpath(output_file)

        # first retrieve the data and create some virtual dataset.
        self._preprocess_frames(input_file_path, output_file=output_file)
        with HDF5File(output_file, "a") as h5_file:
            entry = h5_file.require_group(data_path)
            entry.attrs["NX_class"] = u"NXentry"
            entry.attrs["definition"] = u"NXtomo"
            entry.attrs["version"] = CURRENT_OUTPUT_VERSION
            entry.attrs["default"] = "instrument/detector"

            self._write_beam(
                entry, request_input=request_input, input_callback=input_callback
            )
            self._write_instrument(entry)
            self._write_sample(entry)
            self._write_plugins_output(entry)


class _ZSeriesBaseAcquisition(_BaseAcquisition):
    """
    A 'z serie acquisition' is considered as a serie of _StandardAcquisition.
    Registered scan can be split according to z_translation value.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._acquisitions = {}
        """key is z value and value is _StandardAcquisition"""

    def getStandardSubAcquisitions(self) -> tuple:
        """
        Return the tuple of all _StandardAcquisition composing _Acquisition
        """
        return tuple(self._acquisitions.values())

    def get_z(self, entry):
        z_array = self._get_z_translation(entry, n_frame=None)[0]
        if z_array is None:
            raise ValueError("No z found for scan {}".format(entry.name))
        if isinstance(z_array, (numpy.ndarray, tuple, list)):
            z_array = set(z_array)
        else:
            z_array = set((z_array,))

        # might need an epsilon here ?
        if len(z_array) > 1:
            raise ValueError("More than one value of z found for {}".format(entry.name))
        else:
            return z_array.pop()

    def register_step(self, entry: h5py.Group) -> None:
        """

        :param entry:
        """
        z = self.get_z(entry)
        if z not in self._acquisitions:
            self._acquisitions[z] = _StandardBaseAcquisition(
                entry=self.initialization_entry,
                file_keys=self._file_keys,
                scan_titles=self._scan_titles,
                param_already_defined=self._param_already_defined,
                raise_error_if_issue=self._raise_error_if_issue,
                detector_sel_callback=self._detector_sel_callback,
            )

        self._acquisitions[z].register_step(entry=entry)
