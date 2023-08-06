#!/usr/bin/env python3

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

import logging

from PySide2 import QtCore, QtGui, QtWidgets  #pylint: disable=import-error
from PySide2.QtUiTools import loadUiType      #pylint: disable=no-name-in-module

class LogPanel(QtWidgets.QFrame, loadUiType(__file__.split(".py")[0] + ".ui")[0]):

    """
    A UI panel which attaches to the root logger to display logged messages.

    Note that this panel is unable to display log messages which occur prior to
    its initialisation.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Configure the log handler with default format etc.
        self.handler = logging.StreamHandler(self)
        self.handler.terminator = ""
        self.handler.setFormatter(logging.Formatter(fmt=logging.BASIC_FORMAT))
        # Attach to the root logger
        logging.getLogger().addHandler(self.handler)

        # Finish setting up UI and connect signals
        self.log.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.wordwrapCheckBox.clicked.connect(self._wordwrap_clicked)

    def write(self, data):
        """
        Write data to the log window.

        Primarily used to handle input provided from the ``StreamHandler``.
        """
        self.log.append(data)

    def flush(self):
        """
        Does nothing, but required to support stream-like behaviour.
        """
        pass

    def _wordwrap_clicked(self):
        if self.wordwrapCheckBox.isChecked():
            self.log.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        else:
            self.log.setWordWrapMode(QtGui.QTextOption.NoWrap)
