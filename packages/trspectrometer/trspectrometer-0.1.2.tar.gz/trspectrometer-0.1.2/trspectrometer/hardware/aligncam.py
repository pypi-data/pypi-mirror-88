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
Module for management of webcams or similar devices acessed via OpenCV and used
for beam alignment.
"""

import os
import logging
import re
import atexit
from threading import Thread, Event

from PySide2 import QtCore, QtWidgets
from PySide2.QtUiTools import loadUiType      #pylint: disable=no-name-in-module
try:
    from PySide2.QtMultimedia import QCameraInfo  #pylint: disable=no-name-in-module
except:
    # Work around for ReadTheDocs not having required pulseaudio library.
    pass
import cv2

from .. import configuration as config

log = logging.getLogger(__name__)

class AlignmentCamera():

    def __init__(self, cv_index=0, name="Alignment Camera", description="Camera", devicename=None, focus=50):
        """
        An alignment camera device.

        Note that running multiple cameras from the same USB bus may not work
        due to bandwidth constraints. If a camera fails to serve frames, try
        plugging it into a different set of USB ports.

        :param cv_index: Index of the OpenCV device to use.
        :param name: Friendly name of device to use in the application.
        :param description: Description or model number of the camera hardware.
        :param devicename: System path for the camera device.
        """

        if cv_index is not None:
            self.vidcap = cv2.VideoCapture(cv_index)
            # Attempt to set 720p resolution
            self.vidcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.vidcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            # Set a fixed focus, inf--macro as 0--255 in increments of 5
            self.vidcap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            # Work around bug where sometimes focus doesn't change if previously at that value
            self.vidcap.set(cv2.CAP_PROP_FOCUS, ((focus + 1)%51 if focus is not None else 51)*5)
            self.vidcap.set(cv2.CAP_PROP_FOCUS, (focus if focus is not None else 50)*5)
        else:
            self.vidcap = None

        self.name = name
        self.description = description
        if devicename is None:
            if self.vidcap is not None:
                # Probably correct on Linux, just a descriptor anyway
                self.devicename = f"/dev/video{cv_index}"
            else:
                self.devicename = "missing"
        else:
            self.devicename = devicename

        # Callback functions to call when new frame data is available.
        self._frame_callbacks = set()

        # Thread for frame acquisition
        self._acq_thread = None
        #self._acq_lock = Lock()
        self._acq_stop_event = Event()

    def add_frame_callback(self, callback_function):
        """
        Register a function to be called when new frame data is available.

        The ``callback_function`` must accept a 2-dimensional numpy array of
        greyscale image data.

        Note that this implementation is pure python and does not use the Qt
        QSignal and QSlot mechanisms. Do not directly add a signal's ``emit``
        function here, but instead wrap the call to ``emit()`` in a separate
        method.

        :param callback_function: Function to call when new frame data is available.
        """
        if self.vidcap is None: return
        if callable(callback_function):
            self._frame_callbacks.add(callback_function)
            # Start the acquisition thread if needed
            if self._acq_thread is None or not self._acq_thread.is_alive():
                self._acq_thread = Thread(target=self._start_acquisition, name=f"{self.name}_Acquisition")
                self._acq_stop_event.clear()
                self._acq_thread.start()

    def remove_frame_callback(self, callback_function):
        """
        Unregister a callback function added using ``add_frame_callback()``.

        :param callback_function: Function to unregister.
        """
        if self.vidcap is None: return
        if callback_function in self._frame_callbacks:
            self._frame_callbacks.remove(callback_function)
            if len(self._frame_callbacks) == 0:
                # No more listeners, can stop acquisition thread now
                self._acq_stop_event.set()
                # Wait for thread to finish
                if self._acq_thread is not None:
                    self._acq_thread.join()
        else:
            #log.warning(f"Alignment camera {self.name} had attempt to remove unrecognised callback function: {callback_function}")
            # Probably don't need to warn about this
            pass


    def _start_acquisition(self):
        if self.vidcap is None: return
        log.debug(f"{self.name} acquisition starting.")
        status, frame = self.vidcap.read()
        while status:
            # Convert to greyscale
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Notify callback functions
            for cb in self._frame_callbacks:
                cb(frame)
            # Stop acquisition is requested
            if self._acq_stop_event.is_set():
                log.debug(f"{self.name} acquisition stopped.")
                return
            status, frame = self.vidcap.read()
        log.error(f"{self.name} failed to acquire image data!")

    def close(self):
        """
        Stop frame acquisition and close the camera device.
        """
        if self.vidcap is None: return
        self._acq_stop_event.set()
        if self._acq_thread is not None:
            self._acq_thread.join()
        self.vidcap.release()
        self.vidcap = None

    @property
    def width(self):
        if self.vidcap is not None:
            return int(self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        else:
            return 1280

    @width.setter
    def width(self, x):
        if self.vidcap is not None:
            self.vidcap.set(cv2.CAP_PROP_FRAME_WIDTH, x)

    @property
    def height(self):
        if self.vidcap is not None:
            return int(self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            return 720

    @height.setter
    def height(self, y):
        if self.vidcap is not None:
            self.vidcap.set(cv2.CAP_PROP_FRAME_HEIGHT, y)


"""List of available ``AlignmentCamera`` devices."""
cams = []

"""List of functions to call when device list is refreshed."""
_change_callbacks = set()

def init():
    # OpenCV doesn't have any means to enumerate or get info about devices
    # We'll use Qt QCameraInfo to do this, but the number of devices
    # don't necessarily match 1:1 between Qt and OpenCV...

    global cams

    # If reinitialising, first close any existing cameras
    for cam in cams:
        cam.close()
    cams = []

    # Try opening OpenCV devices to see which ones work
    cvcams = []
    print("Note: probing for OpenCV camera devices. You can ignore any warnings here.")
    for i in range(10):
        log.debug(f"Testing OpenCV device #{i}...")
        vidcap = cv2.VideoCapture(i)
        if vidcap.isOpened():
            log.debug(f"OpenCV device #{i} opened OK.")
            cvcams.append(i)
            vidcap.release()
        else:
            log.debug(f"OpenCV device #{i} failed to open.")
    # Hopefully now cvcams indices matches the QCameraInfo listings...
    qtcams = QCameraInfo.availableCameras()

    # If a camera is in use, the numbers won't match between Qt and OpenCV
    # We can't try opening cameras with Qt since we're not in a QApplication.
    # TODO: What to do? Just abort?
    if len(cvcams) != len(qtcams):
        log.warning("One or more camera devices appear to be in use. As this may cause problems with device matching, detection will be aborted.")
        # Abort, but first create placeholder AlignmentCameras
        for cam in config.data["hardware"]["aligncams"]:
            cams.append(AlignmentCamera(
                cv_index=None,
                name=cam["name"],
                description="Not Found",
                devicename="missing",
                focus=cam["focus"]))
        # Notify callbacks of device refresh
        for cb in _change_callbacks: cb()
        return

    # Log the detected camera devices
    if qtcams:
        log.info("Detected available alignment camera devices:")
        for i, qtcam in enumerate(qtcams):
            log.info(f"  Device #{cvcams[i]}: {qtcam.description()} ({qtcam.deviceName()})")
    else:
        log.info("No alignment camera devices found.")

    # Loop through aligncam list in config and look for matching devices
    for cam in config.data["hardware"]["aligncams"]:
        match_i = 0
        for i, qtcam in enumerate(qtcams):
            # Look for device that matches the filter regular expression
            if re.match(cam["filter"], qtcam.description()):
                # In case of multiple devices which match, select by index as well
                if match_i == cam["index"]:
                    log.info(f"{cam['name']} matched to {qtcam.description()} ({qtcam.deviceName()})")
                    cams.append(AlignmentCamera(
                        cv_index=cvcams[i],
                        name=cam["name"],
                        description=qtcam.description(),
                        devicename=qtcam.deviceName(),
                        focus=cam["focus"]))
                    match_i += 1
                    break
                match_i += 1
        if match_i == 0:
            log.warning(f"{cam['name']} was not matched to any available devices!")
            # Add a non-functional AlignmentCamera as a placeholder.
            cams.append(AlignmentCamera(
                cv_index=None,
                name=cam["name"],
                description="Not Found",
                devicename="missing",
                focus=cam["focus"]))

    # Notify callbacks of device refresh
    for cb in _change_callbacks: cb()

# Begin device initialisation if hardware is enabled
if config.data["hardware"]["init_hardware"]:
    init()

def add_change_callback(callback_function):
    """
    Register a function to be called when the list of ``AlignmentCamera``\ s is refreshed.

    :param callback_function: Function to call when devices are refreshed.
    """
    if callable(callback_function):
        _change_callbacks.add(callback_function)


def remove_change_callback(callback_function):
    """
    Unregister a callback function added using ``add_change_callback()``.

    :param callback_function: Function to unregister.
    """
    if callback_function in _change_callbacks:
        _change_callbacks.remove(callback_function)


def close():
    """Close any used alignment camera devices."""
    for cam in cams:
        cam.close()
# Automatically close camera devices on exit
atexit.register(close)



class AlignmentCameraStatusPanel(QtWidgets.QFrame, loadUiType(os.path.join(os.path.dirname(__file__), "aligncamstatus.ui"))[0]):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Refresh UI when devices change
        add_change_callback(self.refresh)
        # Reset button triggers hardware re-init
        self.resetPushButton.clicked.connect(init)
        self.refresh()

    def refresh(self):
        # Remove all widgets from grid and destroy them
        while True:
            w = self.grid.takeAt(0)
            if w is None: break
            w.widget().deleteLater()
        # Build the list of devices
        for row, cam in enumerate(cams):
            self.grid.addWidget(QtWidgets.QLabel(cam.name), row, 0)
            self.grid.addWidget(QtWidgets.QLabel(cam.description), row, 1)
            if cam.vidcap is None:
                w = QtWidgets.QLabel("ERROR")
                w.setStyleSheet("QLabel { color : red; }")
            else:
                w = QtWidgets.QLabel("OK")
                w.setStyleSheet("QLabel { color : green; }")
            self.grid.addWidget(w, row, 2, QtCore.Qt.AlignRight)
