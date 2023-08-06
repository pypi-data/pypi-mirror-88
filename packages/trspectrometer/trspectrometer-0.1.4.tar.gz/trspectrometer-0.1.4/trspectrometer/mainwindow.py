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

import os
import sys
import argparse
import traceback
import logging
logging.basicConfig(level=logging.INFO)

from PySide2 import QtCore, QtWidgets       #pylint: disable=import-error
from PySide2.QtUiTools import loadUiType    #pylint: disable=no-name-in-module
from PySide2.QtWidgets import QMessageBox   #pylint: disable=no-name-in-module
import zarr                                 #pylint: disable=import-error

# Some imports just so they're avialable in the console
import numpy as np
from . import pyqtgraph as pg
#import scipy
#import matplotlib as mpl
#mpl.use('QT5Agg')
#import matplotlib.pyplot as plt

# This is a workaround for loadUiType not finding the resource _rc.py inside the package
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def exception_handler(extype, value, tb):
    """
    Global handler for exceptions.
    Not particuarly smart, but stops crashes from minor recoverable errors.
    The exception details are sent to the log.
    """
    logging.error("Caught an unhandled exception:\n  " + "  ".join(traceback.format_exception(extype, value, tb)).rstrip("\n"))
sys.excepthook = exception_handler

class MainWindow(QtWidgets.QMainWindow, loadUiType(__file__.split(".py")[0] + ".ui")[0]):
    """
    Main window for the various components of the spectrometer software.
    """
    def __init__(self, init_hardware=None):
        super().__init__()
        self.setupUi(self)

        # Note we are doing imports as late as possible so that the logPanel
        # is able to catch and display as much as possible from the logger.

        # Intialise logging system
        from . logpanel import LogPanel
        self.log = logging.getLogger(__name__)
        self.logPanel = LogPanel()
        self.actionLog.triggered.connect(lambda: _show_and_activate(self.logPanel))

        # Initialise configuration
        from . import configuration as config

        # Adjust config based on provided arguments
        if not init_hardware is None:
            config.data["hardware"]["init_hardware"] = init_hardware

        # Initialise python console
        # TODO: Does importing in init mean we can't access hardware etc in console now?
        from . console import Console
        self.console = Console(
            namespace_func=lambda: {**self.__dict__, **globals()},
            history_filename=os.path.join(os.path.dirname(config.configfile), "console.history")
        )
        self.actionPythonConsole.triggered.connect(lambda: _show_and_activate(self.console))

        # Initialise hardware status panel
        from . import hardware as hw
        self.hardwarestatusPanel = hw.HardwareStatusPanel()
        self.actionHardwareStatus.triggered.connect(lambda: _show_and_activate(self.hardwarestatusPanel))

        # Initialise alignment panel
        from . alignmentpanel import AlignmentPanel
        self.alignmentPanel = AlignmentPanel(self)
        self.tabWidget.insertTab(0, self.alignmentPanel, "Align")

        # Initialise data panel
        from . import datastorage as ds
        self.ds = ds
        from . datapanel import DataPanel
        self.dataPanel = DataPanel(self)
        self.tabWidget.insertTab(1, self.dataPanel, "Data")

        # Initialise about panel
        from . aboutpanel import AboutPanel
        self.aboutPanel = AboutPanel(self)

        # Start with data panel selected
        self.tabWidget.setCurrentIndex(1)

        # Connect UI signals
        self.actionNew.triggered.connect(self._new_clicked)
        self.actionOpen.triggered.connect(self._open_clicked)
        self.actionSaveAs.triggered.connect(self._save_clicked)
        self.actionImportRawData.triggered.connect(self._import_raw_data_clicked)
        self.actionExportRawDataAverage.triggered.connect(self._export_raw_data_average_clicked)
        self.actionAbout.triggered.connect(self._about_clicked)

        # Start new data set
        self._new_clicked()

    def closeEvent(self, event):
        """Handler for window close event."""
        #self.statusbar.showMessage('Closing hardware devices...')
        from . import hardware
        hardware.close()
        self.logPanel.close()
        self.console.close()
        self.hardwarestatusPanel.close()

    def _new_clicked(self):
        """Handler for the File->New menu item."""
        # TODO: Prompt unsaved
        self.ds.d = self.ds.null_raw_data()
        self.ds.t = zarr.group()
        self.ds.signals.data_changed.emit()
        self.actionSaveAs.setEnabled(False)
        self.menuExport.setEnabled(False)
        self.actionProperties.setEnabled(False)
        msg = f"New data set created"
        self.log.info(msg)
        self.statusbar.showMessage(msg)

    def _open_clicked(self):
        """Handler for the File->Open menu item."""
        # TODO: Prompt unsaved
        try:
            dirname = self.ds.open_zarr(parent=self)
        except Exception as ex:
            self.log.error(f"{ex}")
            QMessageBox.critical(self, "Error opening data directory", f"{ex}")
            return
        if not dirname: return
        self.ds.signals.data_changed.emit()
        self.actionSaveAs.setEnabled(True)
        self.menuExport.setEnabled(True)
        self.actionProperties.setEnabled(True)
        msg = f"Data opened from {dirname}"
        self.log.info(msg)
        self.statusbar.showMessage(msg)

    def _save_clicked(self):
        """Handler for the File->Save menu item."""
        try:
            dirname = self.ds.save_zarr(parent=self)
        except Exception as ex:
            self.log.error(f"{ex}")
            QMessageBox.critical(self, "Error saving data directory", f"{ex}")
            return
        if dirname == None: return
        msg = f"Data saved to {dirname}"
        self.log.info(msg)
        self.statusbar.showMessage(msg)

    def _import_raw_data_clicked(self):
        """Handler for the File->Import->Raw Data menu item."""
        # TODO: Prompt unsaved
        try:
            filename, data = self.ds.import_raw(parent=self)
        except Exception as ex:
            self.log.error(f"{ex}")
            QMessageBox.critical(self, "Error importing raw data", f"{ex}")
            return
        if not filename: return
        self.ds.d = data
        self.ds.t = zarr.group()
        self.ds.signals.data_changed.emit()
        self.actionSaveAs.setEnabled(True)
        self.menuExport.setEnabled(True)
        self.actionProperties.setEnabled(True)
        msg = f"Data imported from {filename}"
        self.log.info(msg)
        self.statusbar.showMessage(msg)

    def _export_raw_data_average_clicked(self):
        """Handler for the File->Export->Raw Data Average menu item."""
        try:
            filename = self.ds.export_raw_average(parent=self)
        except Exception as ex:
            self.log.exception(f"{ex}")
            QMessageBox.critical(self, "Error exporting raw data average", f"{ex}")
            return
        if filename is None: return
        msg = f"Data exported to {filename}"
        self.log.info(msg)
        self.statusbar.showMessage(msg)

    def _about_clicked(self):
        self.aboutPanel.exec_()
        

def _show_and_activate(widget):
    """Show and activate a given QWidget."""
    widget.show()
    widget.activateWindow()

def main():
    """Run the launcher application."""

    # Respond to command line arguments
    argparser = argparse.ArgumentParser(description="Run the TRSpectrometer application.")
    argparser.add_argument("--hardware", help="Perform hardware detection and initialisation.", nargs=1, choices=["true", "false"])
    args = argparser.parse_args()
    if args.hardware is not None:
        args.hardware = (args.hardware[0] == "true")

    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow(init_hardware=args.hardware)
    mainwindow.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
