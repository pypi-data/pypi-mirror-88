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
Module for management of various spectrometer hardware devices.
"""

import os
import atexit
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import loadUiType     #pylint: disable=no-name-in-module

from . import aligncam

def close():
    aligncam.close()
atexit.register(close)


class HardwareStatusPanel(QtWidgets.QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Build the UI
        self.setWindowTitle("Hardware Status")
        self.setWindowIcon(QtGui.QIcon("trspectrometer.png"))
        self.setWidgetResizable(True)
        self.panel = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self)
        # Add the various hardware status panels
        self.layout.addWidget(aligncam.AlignmentCameraStatusPanel(self))
        #...

        self.layout.addStretch(1)
        self.panel.setLayout(self.layout)
        self.setWidget(self.panel)
