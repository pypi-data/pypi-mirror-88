# Copyright 2020 Patrick C. Tapping
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Utilities for handling the creation, manipulation, and storage of transient
absorption data.

The native storage format uses `zarr <https://zarr.readthedocs.io/>`_, which has
many friendly methods for handling data.
These utilities therefore are mainly for the import and export of different file
formats.
"""

import os
import warnings
import logging

import numpy as np
import zarr                                                 #pylint: disable=import-error
from scipy.stats import norm
from scipy.ndimage import median_filter
from PySide2.QtWidgets import QFileDialog, QMessageBox      #pylint: disable=no-name-in-module
from PySide2 import QtCore                                  #pylint: disable=import-error
from PySide2.QtCore import Signal                           #pylint: disable=no-name-in-module

from . import configuration as config
from . ufsfile import UFSData

log = logging.getLogger(__name__)
"Logger for this module."

d = {}
"Reference to the currently loaded data as a zarr array."

d_path = ""
"Path to the currently loaded zarr data array in :attr:`d`."

t = zarr.group()
"Reference to temporary data which doesn't need to be saved to disk or can be rebuilt from :attr:`d`."

root_attrs = {
    "Description"      : "Time-resolved spectroscopy data",
    "Format"           : "trdata",
    "Version"          : "1.0.0",
    "CreationSoftware" : "trspectrometer",
}
"Attributes to include in the root of the zarr array."

class SignalStorage(QtCore.QObject):
    """
    A class which is able to store and send Qt Signals.

    Since Signals can only be sent by QObjects, an instance of this class
    is used to store and emit the various Signals.
    """

    "Signal that new data has been loaded."
    data_changed = Signal()

    "Signal that the selection of raw data traces has changed."
    raw_selection_changed = Signal()
signals = SignalStorage()


def null_raw_data():
    """
    Generate blank raw data.
    """
    data = zarr.group()
    data.attrs.update(root_attrs)
    data.create_group("raw")
    data["raw"].array("wavelength", data=np.array([500.0], dtype=np.float32))
    data["raw"].array("time", data=np.array([0.0], dtype=np.float32))
    data["raw"].zeros("data", shape=(1, 1, 1), dtype=np.float32)
    data["raw/wavelength"].attrs["units"] = "nm"
    data["raw/time"].attrs["units"] = "ps"
    data["raw/data"].attrs["units"] = "DeltaA"
    return data

def dummy_raw_data(scans=5, wl_size=2048, t_size=1500):
    """
    Generate some dummy raw data for testing purposes.

    :param scans: Number of scans in the data set.
    :param wl_size: Number if elements on the wavelength axis.
    :param t_size: Number of elements on the time axis.
    :returns: zarr group containing the dummy data.
    """
    data = zarr.group()
    data.attrs.update(root_attrs)
    data.create_group("raw")
    data["raw"].array("wavelength", data=np.linspace(500.0, 1000.0, num=wl_size, dtype=np.float32))
    data["raw"].array("time", data=np.linspace(0.0, 4000.0, num=t_size, dtype=np.float32))
    data["raw"].zeros("data", shape=(0, t_size, wl_size), dtype=np.float32)
    data["raw/wavelength"].attrs["units"] = "nm"
    data["raw/time"].attrs["units"] = "ps"
    data["raw/data"].attrs["units"] = "DeltaA"

    # Add scans incrementally
    for _ in range(scans):
        scan = np.zeros((t_size, wl_size), dtype=np.float32)
        # A spectral feature
        scan[:,:] = norm.pdf(np.linspace(-5, 5, num=wl_size), loc=0, scale=1)[np.newaxis]
        # With exponential decay kinetics
        scan[:,:] *= np.exp(-(data["raw/time"][:]/1000))[:,np.newaxis]
        scan[0:50] = 0.0
        # Add some noise
        scan += 0.1*(1 - 2*np.random.random_sample(size=(t_size, wl_size)))
        # Add scan to data set
        data["raw/data"].append(scan[np.newaxis], axis=0)

    return data

def raw_data_average():
    """
    Compute and return the average of the raw data set.

    This routine will use the "exclude_scans" attribute of raw to exclude scans from the average.
    The attribute should contain a list of scan indices to exclude.

    :returns: Array containing the averaged data.
    """
    if (not "raw" in d) or (not "raw/data" in d): return None
    if not "raw" in t:
        t.create_group("raw")
    if not "exclude_scans" in t["raw"].attrs:
        # Include all scans if not specified yet
        t["raw"].attrs["exclude_scans"] = []
    if d["raw/data"].shape[0] - len(t["raw"].attrs["exclude_scans"]) >= 1:
        # Multiple scans included, average them
        selection_mask = np.ones((d["raw/data"].shape[0]), dtype=np.bool)
        selection_mask[t["raw"].attrs["exclude_scans"]] = False
        # Ignore warining if all NaNs in slice
        warnings.simplefilter("ignore")
        result = np.nanmean(d["raw/data"].get_orthogonal_selection((selection_mask, slice(None), slice(None))), axis=0)
        warnings.simplefilter("default")
    else:
        # Zero traces specified!?!? Just average everything again.
        # TODO: Handle this better?
        # Eventually we want to be able to handle completely missing raw data.
        # Ignore warining if all NaNs in slice
        warnings.simplefilter("ignore")
        result = np.nanmean(d["raw/data"], axis=0)
        warnings.simplefilter("default")
    return result

def open_zarr(parent=None, initial_dir=None):
    """
    Show a dialog for selecting a time-resolved data directory, and load the data.

    The native format for data is a Zarr data directory.
    If the selected directory does not appear to contain time-resolved data,
    a RuntimeError will be raised.

    :param parent: The parent QWidget for the dialog box.
    :param initial_dir: Initial directory for the dialog box.
        If `None`, then the data directory specified in the configuration will be used.
    :returns: Name of selected data directory, or ``None`` if no directory selected.
    """
    global d, t, d_path
    if initial_dir is None:
        initial_dir = config.data["directories"]["data"]
    # Was hoping that using a filter and directory options would limit to 
    # selection of dirname.zarr, but it doesn't quite work that way...
    qfd = QFileDialog(parent, "Open Time-resolved Data", initial_dir, "Zarr data directory (*)")
    qfd.setAcceptMode(QFileDialog.AcceptOpen)
    qfd.setFileMode(QFileDialog.Directory)
    qfd.setOption(QFileDialog.ShowDirsOnly)
    if qfd.exec_():
        dirname = qfd.selectedFiles()[0]
        try:
            # Open read-only to prevent inadvertant modifications to data
            data = zarr.open(dirname, mode="r")
        except:
            raise RuntimeError(f"Unable to read {dirname}:\nNot a Zarr data directory.")
        if not "Format" in data.attrs or not data.attrs["Format"] == "trdata":
            raise RuntimeError(f"Unable to read {dirname}:\nNot time-resolved data.")
        # Looks OK, switch in the loaded data
        d = data
        t = zarr.group()
        # Copy data and metadata which may be modified to temporary storage
        if ("raw" in d) and ("exclude_scans" in d["raw"].attrs):
            t.create_group("raw")
            t["raw"].attrs["exclude_scans"] = d["raw"].attrs["exclude_scans"]
        d_path = dirname
        return dirname
    return None

def save_zarr(parent=None, initial_dir=None, data=None):
    """
    Show a dialog for selecting the save directory location for time-resolved data.

    The native format for data is a Zarr data directory.
    If the Zarr `data` is not provided, the currently loaded data will be saved.

    :param parent: The parent QWidget for the dialog box.
    :param initial_dir: Initial directory for the dialog box.
        If `None`, then the data directory specified in the configuration will be used.
    :param data: Zarr data to save.
    :returns: Directory where data was saved, or ``None`` if no directory selected.
    """
    # If data not given, default to currently loaded data
    global d, t, d_path
    if data is None:
        if d is None: return None
        data = d
    if initial_dir is None:
        initial_dir = config.data["directories"]["data"]
    qfd = QFileDialog(parent, "Save Time-resolved Data", initial_dir, "Zarr data directory (*)")
    qfd.setAcceptMode(QFileDialog.AcceptSave)
    qfd.setFileMode(QFileDialog.Directory)
    qfd.setOption(QFileDialog.ShowDirsOnly)
    dirname = None
    while qfd.exec_():
        dirname = qfd.selectedFiles()[0]
        if dirname == d_path:
            # Selected data dir is the one currently open
            reply = QMessageBox.question(parent, "Data Directory Exists", "Selected data directory is the one currently open. Do you want to overwrite its contents?")
            if reply == QMessageBox.No:
                # Show selection dialog again
                dirname = None
                continue
            else:
                # Just need to update currently open data directory, enable write
                dest = zarr.open(dirname, mode="r+")
        else:
            # Selected data dir is not the one currently open
            # QFileDialog creates the directory before the suffix is appended, delete it if empty
            try:
                os.rmdir(dirname)
            except Exception as ex:
                pass
            # Ensure name has a .tr.zarr suffix
            dirname = dirname.partition(".tr.zarr")[0] + ".tr.zarr"
            try:
                dest = zarr.open(dirname, mode="w-")
            except Exception as ex:
                # Failed with "w-" mode as directory already exists
                reply = QMessageBox.question(parent, "Data Directory Exists", "Selected data directory already exists. Do you want to overwrite its contents?")
                if reply == QMessageBox.No:
                    # Show selection dialog again
                    initial_dir = dirname
                    dirname = None
                    continue
                else:
                    # Force overwrite of directory
                    dest = zarr.open(dirname, mode="w")
            # Copy the data over to new destination
            try:
                zarr.copy_all(data, dest)
                # Root attributes don't get copied. Bug in zarr 2.5.0
                dest.attrs.update(data.attrs)
            except Exception as ex:
                raise RuntimeError(f"Unable to write {dirname}:\n{ex}")
        # Save out data modifications from temporary storage
        if ("raw" in t) and ("exclude_scans" in t["raw"].attrs):
            if "raw" not in dest:
                dest.create_group("raw")
            dest["raw"].attrs["exclude_scans"] = t["raw"].attrs["exclude_scans"]
        # Done. Start using new data directory in read-only mode
        d_path = dirname
        d = zarr.open(dirname, "r")
        break
    return dirname
        

def import_raw(parent=None, initial_dir=None):
    """
    Show a dialog for selecting non-native time-resolved data file(s), and return the data.

    :param parent: The parent QWidget for the dialog box.
    :param initial_dir: Initial directory for the dialog box.
        If `None`, then the data directory specified in the configuration will be used.
    :returns: Tuple of selected file name(s) and zarr data.
    """
    if initial_dir is None:
        initial_dir = config.data["directories"]["data"]
    # File type definitions
    type_csv = "CSV Files (*.csv *.csv? *.csv??)"
    type_ufs = "UFS Files (*.ufs)"
    filenames, filetype = QFileDialog.getOpenFileNames(parent, "Import Time-resolved Data", initial_dir, f"{type_csv};;{type_ufs}")
    if not filenames: return None, None
    if filetype == type_csv:
        data_matrix, warning_msgs = load_csv_matrix(filenames)
        if data_matrix.shape < (1, 2, 2):
            raise RuntimeError(f"Unable to interpret valid data from selected files.")
        # Transpose from (scan, wavelength, time) to (scan, time, wavelength)
        data_matrix = np.swapaxes(data_matrix, 1, 2)
        # Build the zarr data array
        data = zarr.group()
        data.attrs.update(root_attrs)
        data.create_group("raw")
        data["raw"].array("wavelength", data=np.mean(data_matrix[:,0,1:], axis=0))
        data["raw"].array("time", data=np.mean(data_matrix[:,1:,0], axis=0))
        data["raw"].array("data", data=data_matrix[:,1:,1:])
        data["raw/wavelength"].attrs["units"] = "nm"
        data["raw/time"].attrs["units"] = "ps"
        data["raw/data"].attrs["units"] = "DeltaA"        
    elif filetype == type_ufs:
        ufs = [ UFSData(ufsfile=f) for f in filenames ]
        # UFS files can potentially contain multiple scans.
        # Use the wavelength and time axes from the first file and if the
        # shape of subsequent file data matches, include it as additional scans.
        warning_msgs = ""
        data_matrices = []
        for i, u in enumerate(ufs):
            if not u.data_matrix.shape == ufs[0].data_matrix.shape:
                warning_msgs += f"Matrix shape of {os.path.basename(filenames[i])} does not match other files, skipping.\n"
                ufs.remove(u)
            else:
                data_matrices.append(np.swapaxes(u.data_matrix, 1, 2))
        data_matrices = np.concatenate(data_matrices, axis=0)
        # Build the zarr data array
        data = zarr.group()
        data.attrs.update(root_attrs)
        data.create_group("raw")
        data["raw"].array("wavelength", data=ufs[0].axis1_data)
        data["raw"].array("time", data=ufs[0].axis2_data)
        data["raw"].array("data", data=data_matrices)
        data["raw/wavelength"].attrs["units"] = ufs[0].axis1_units
        data["raw/time"].attrs["units"] = ufs[0].axis2_units
        data["raw/data"].attrs["units"] = "DeltaA" if ufs[0].data_units == "DA" else ufs[0].data_units
        data["raw"].attrs["ufs_metadata"] = ufs[0].metadata
    # Alert if any warnings for invalid files etc
    if warning_msgs:
        QMessageBox.warning(parent, "Warnings during import", warning_msgs)
    # Abbreviate filename list if needed
    if len(filenames) > 1:
        filename = f"{os.path.basename(filenames[0])} and {len(filenames) - 1} other{'s' if len(filenames) > 2 else ''}"
    else:
        filename = os.path.basename(filenames[0])
    return filename, data


def load_csv_matrix(filenames, cleanrows=95, cleancols=95):
    """
    Load a list of CSV files containing data matrices.

    The CSV data in each file must have identical shapes (number of rows and columns).
    Any file where the shape does not match the first loaded file will be ignored.

    :param filenames: List of CSV file names to load data from.
    :returns: Numpy array containing file data.
    """
    warning_messages = ""
    data_matrices = []
    for filename in filenames:
        try:
            warnings.simplefilter('ignore') # ignore any mismatched line lengths (text/metadata at end of file)
            data_matrices.append(np.genfromtxt(filename, delimiter=',', dtype=np.float32, invalid_raise=False))
            warnings.simplefilter('default')
        except OSError:
            warning_messages += f"Error opening {os.path.basename(filename)}, skipping.\n"
            continue
        # Ensure shape of each matrix matches the first file
        if not data_matrices[len(data_matrices)-1].shape == data_matrices[0].shape:
            warning_messages += f"Matrix shape of {os.path.basename(filename)} does not match other files, skipping.\n"
    # Ignore files if matrix shapes don't match
    data_matrices = np.stack([ x for x in data_matrices if x.shape == data_matrices[0].shape ], 0)
    
    # Convert any infs to nans
    data_matrices[np.logical_not(np.isfinite(data_matrices))] = np.nan

    # Remove wavelengths/rows with too many nan values
    if cleanrows < 100:
        cleanrows = max(0, cleanrows)
        mask = np.sum(np.isfinite(data_matrices[:,:,1:]), axis=2) >= (1.0 - cleanrows/100.0)*(data_matrices.shape[2] - 1)
        # Remove rows from all scans so dimensions still match
        mask = np.all(mask, axis=0) 
        data_matrices = data_matrices[:,mask]
        #print('Removed rows with more than {}% invalid data. New matrix shape: {}'.format(cleanrows, data_matrices[0].shape))
    
    # Remove times/columns with too many nan values
    if cleancols < 100:
        cleancols = max(0, cleancols)
        mask = np.sum(np.isfinite(data_matrices[:,1:,:]), axis=1) >= (1.0 - cleancols/100.0)*(data_matrices.shape[1] - 1)
        # Remove columns from all scans so dimensions still match
        mask = np.all(mask, axis=0)
        data_matrices = data_matrices[:,:,mask]
        #print('Removed columns with more than {}% invalid data. New matrix shape: {}'.format(cleancols, data_matrices[0].shape))

    return data_matrices, warning_messages


def export_raw_average(parent=None, initial_dir=None):
    """
    Show a dialog for saving out the average of the selected raw data traces to a non-native data file.

    :param parent: The parent QWidget for the dialog box.
    :param initial_dir: Initial directory for the dialog box.
        If `None`, then the data directory specified in the configuration will be used.
    """
    if initial_dir is None:
        initial_dir = config.data["directories"]["data"]
    # File type definitions
    type_csv = "CSV Files (*.csv)"
    type_ufs = "UFS Files (*.ufs)"
    filename, filetype = QFileDialog.getSaveFileName(parent, "Export Raw Data Average", initial_dir, f"{type_csv};;{type_ufs}")
    if not filename: return None
    if filetype == type_csv:
        # Ensure name has a .csv suffix
        filename = filename.partition(".csv")[0] + ".csv"
        # Attach wavelength and time axis to data matrix
        data_average = raw_data_average()
        data = np.zeros((data_average.shape[1] + 1, data_average.shape[0] + 1))
        data[1:,1:] = data_average.T
        data[1:,0] = d["raw/wavelength"]
        data[0,1:] = d["raw/time"]
        np.savetxt(filename, data, fmt="%g", delimiter=",")
    elif filetype == type_ufs:
        # Ensure name has a .ufs suffix
        filename = filename.partition(".ufs")[0] + ".ufs"
        # Build a UFSData object
        ufs = UFSData()
        ufs.version = "Version2".encode("utf-8")
        ufs.axis1_label = "Wavelength".encode("utf-8")
        ufs.axis1_units = d["raw/wavelength"].attrs["units"].encode("utf-8")
        ufs.axis1_data = d["raw/wavelength"]
        ufs.axis2_label = "Time".encode("utf-8")
        ufs.axis2_units = d["raw/time"].attrs["units"].encode("utf-8")
        ufs.axis2_data = d["raw/time"]
        ufs.data_units = ("DA" if d["raw/data"].attrs["units"] == "DeltaA" else d["raw/data"].attrs["units"]).encode("utf-8")
        ufs.data_matrix = np.swapaxes(raw_data_average(), 0, 1)[np.newaxis,:,:]
        # TODO: Could actually put something useful in here...
        ufs.metadata = "".encode("utf-8")
        ufs.write_file(filename)
    return filename


def find_stepsizes(time_axis, filter_window=35, snap=0.05):
    """
    Generate a list of time step sizes from a given time axis label array.

    :param time_axis: Array of time axis values.
    :param filter_window: Width of filtering window to apply, in array indices.
    :param snap: Minimum step size permitted. Step sizes will be snapped to multiples of this value.
    :returns: List of [count, step_size] pairs.
    """
    if time_axis.shape[0] < 2: return []
    steps = np.round(snap*np.round(median_filter(np.diff(time_axis.astype(np.float64)), size=filter_window)/snap), 6)
    steplist = [ [0, steps[0]] ]
    for x in steps:
        if x == steplist[-1][1]:
            # Repeated step size
            steplist[-1][0] += 1
        else:
            # New step size
            steplist.append([1, x])
    return steplist