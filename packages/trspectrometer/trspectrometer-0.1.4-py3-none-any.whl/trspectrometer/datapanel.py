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
import logging
import warnings
#from threading import Lock

from PySide2 import QtCore, QtGui, QtWidgets #pylint: disable=import-error
from PySide2.QtUiTools import loadUiType     #pylint: disable=no-name-in-module
#from PySide2.QtCore import Signal
from PySide2.QtCore import QRectF            #pylint: disable=no-name-in-module
import numpy as np

from . import pyqtgraph as pg
from . import configuration as config
from . import hardware as hw
from . import datastorage as ds
from . qtwidgets import FlowLayout

class DataPanel(QtWidgets.QWidget, loadUiType(__file__.split(".py")[0] + ".ui")[0]):
    """
    UI panel to facilitate the collection and viewing of data.

    :param parent: Parent of the QWidget.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Listen for when data set is changed
        ds.signals.data_changed.connect(self._data_changed)
        ds.signals.raw_selection_changed.connect(self._raw_selection_changed)

        # Setup pyqtgraph plot areas
        pg.setConfigOptions(imageAxisOrder='row-major', antialias=True)
        self.overview = self.glw.addPlot(row=0, col=0, enableMenu=False)
        self.overview.setLabels(bottom="Wavelength (nm)", left="Delay (ps)")
        [ self.overview.getAxis(ax).setZValue(10) for ax in self.overview.axes ] # Draw axes and ticks above image/data
        self.overview_composite_image = pg.ImageItem()
        self.overview_images = []
        self.overview.getAxis('left').setStyle(autoExpandTextSpace=False)
        self.crosshairx = pg.InfiniteLine(pos=0.0, angle=90, movable=True, pen=config.data["rawdata"]["crosshair"]["colour"], hoverPen=config.data["rawdata"]["crosshair"]["highlight"])
        self.crosshairy = pg.InfiniteLine(pos=0.0, angle=0, movable=True, pen=config.data["rawdata"]["crosshair"]["colour"], hoverPen=config.data["rawdata"]["crosshair"]["highlight"])
        self.crosshairx.setZValue(9)
        self.crosshairy.setZValue(9)
        self.overview.addItem(self.crosshairx, ignoreBounds=True)
        self.overview.addItem(self.crosshairy, ignoreBounds=True)
        self.crosshair = pg.ROI(pos=(0.0, 0.0), size=(0.0, 0.0), handlePen=config.data["rawdata"]["crosshair"]["colour"], handleHoverPen=config.data["rawdata"]["crosshair"]["highlight"])
        self.crosshair.addTranslateHandle((0.0, 0.0))
        self.overview.addItem(self.crosshair, ignoreBounds=True)
        self.crosshair.sigRegionChanged.connect(self._crosshair_changed)
        self.crosshairx.sigPositionChanged.connect(self._crosshairx_changed)
        self.crosshairy.sigPositionChanged.connect(self._crosshairy_changed)
        # Indicies of currently selected wavelength, time
        self.selected_w_i = 0
        self.selected_t_i = 0

        # Colourmap bar
        self.cbar = pg.HistogramLUTItem(self.overview_composite_image)
        self.cbar.gradient.restoreState({"mode": "rgb",
            "ticks": [(0.00, (0, 0, 0)),
                      (0.25, (0, 0, 128)),
                      (0.50, (144, 0 , 0)),
                      (0.85, (224, 224, 0)),
                      (1.00, (255, 255, 255))]})
        self.cbar.axis.setStyle(autoExpandTextSpace=False)
        self.cbar.sigLookupTableChanged.connect(self._cbar_changed)
        self.cbar.sigLevelsChanged.connect(self._cbar_changed)
        self.glw.addItem(self.cbar, row=0, col=2, rowspan=2)

        # Slice along the y direction, kinetics for a given wavelength
        self.xslice = self.glw.addPlot(row=0, col=1, enableMenu=False)
        self.xslice.showGrid(x=True, y=True)
        self.xslice.addLegend(offset=(-10, 5))
        self.xslice.setLabels(bottom="Delay (ps)", left="ΔA")
        self.xslice.getAxis('left').setStyle(autoExpandTextSpace=False)
        self.xslice_plot = self.xslice.plot(pen=(255, 255, 0), name="Temporal slice @ 000.0 nm")
        self.xslice_plot.setZValue(9)
        #self.latest_scan_plot = self.xslice.plot(pen=0.3, name="Latest scan")
        #self.latest_scan_plot.setZValue(8)
        self.xslice_scan_plots = []
        self.xslice_crosshair = pg.InfiniteLine(pos=0.0, angle=90, movable=True, pen=config.data["rawdata"]["crosshair"]["colour"], hoverPen=config.data["rawdata"]["crosshair"]["highlight"])
        self.xslice.addItem(self.xslice_crosshair, ignoreBounds=True)
        self.xslice_crosshair.sigPositionChanged.connect(self._xslice_crosshair_changed)

        # Slice along the x direction, spectrum for a given time
        self.yslice = self.glw.addPlot(row=1, col=0, enableMenu=False)
        self.yslice.showGrid(x=True, y=True)
        self.yslice.addLegend(offset=(-10, 5))
        self.yslice.setLabels(bottom="Wavelength (nm)", left="ΔA")
        self.yslice.getAxis('left').setStyle(autoExpandTextSpace=False)
        self.yslice_plot = self.yslice.plot(pen=(255, 255, 0), name="Spectral slice @ 0000.0 ps")
        self.yslice_plot.setZValue(9)
        #self.latest_acq_plot = self.yslice.plot(pen=0.33, name="Latest spectrum")
        #self.latest_acq_plot.setZValue(8)
        self.yslice_scan_plots = []
        self.yslice_crosshair = pg.InfiniteLine(pos=0.0, angle=90, movable=True, pen=config.data["rawdata"]["crosshair"]["colour"], hoverPen=config.data["rawdata"]["crosshair"]["highlight"])
        self.yslice.addItem(self.yslice_crosshair, ignoreBounds=True)
        self.yslice_crosshair.sigPositionChanged.connect(self._yslice_crosshair_changed)

        # Link axes
        self.overview.getViewBox().sigRangeChangedManually.connect(self._link_axes_overview)
        self.xslice.getViewBox().sigRangeChangedManually.connect(self._link_axes_xslice)
        self.yslice.setXLink(self.overview)

        # Bottom right panel containing list of scans
        self.scansWidget = DataPanelScansWidget()
        self.proxyWidget = QtWidgets.QGraphicsProxyWidget()
        self.proxyWidget.setWidget(self.scansWidget)
        self.glw.addItem(self.proxyWidget, row=1, col=1)

        # Set up the step size table
        self.stepmodel = QtGui.QStandardItemModel(0, 2)
        self.stepTableView.setModel(self.stepmodel)
        self.stepTableView.setItemDelegate(StepsSpinBoxDelegate())
        self._reset_step_table()
        self._add_step_table_row()

        # Connect signals
        self.stepComboBox.currentIndexChanged.connect(self._steptype_changed)
        self.addStepPushButton.clicked.connect(self._addstep_clicked)
        self.removeStepPushButton.clicked.connect(self._removestep_clicked)
        self.loadStepPushButton.clicked.connect(self._loadstep_clicked)

    def _link_axes_overview(self):
        self.xslice.setXRange(*self.overview.viewRange()[1])

    def _link_axes_xslice(self):
        self.overview.setYRange(*self.xslice.viewRange()[0])

    def _crosshair_changed(self):
        pos = self.crosshair.pos()
        if not self.crosshairx.value() == pos[0]:
            self.crosshairx.setPos(pos[0])
        if not self.crosshairy.value() == pos[1]:
            self.crosshairy.setPos(pos[1])

    def _crosshairx_changed(self):
        self.crosshair.setPos(self.crosshairx.value(), self.crosshairy.value())
        if not self.yslice_crosshair.value() == self.crosshairx.value():
            self.yslice_crosshair.setPos(self.crosshairx.value())
        new_i = np.argmin(np.abs(ds.d["raw/wavelength"][:] - self.crosshairx.value()))
        if new_i != self.selected_w_i:
            self.selected_w_i = new_i
            #self._acquisition_lock.acquire()
            # Update individual scan traces
            for scan_i, plotitem in enumerate(self.xslice_scan_plots):
                scan_data = ds.d["raw/data"][scan_i]
                nonzero_t_i = np.any(scan_data, axis=1)
                plotitem.setData(ds.d["raw/time"][:][nonzero_t_i], scan_data[nonzero_t_i,self.selected_w_i])
            # Update average trace
            nonzero_t_i = np.any(ds.t["raw/data_avg"], axis=1)
            self.xslice_plot.setData(ds.d["raw/time"][:][nonzero_t_i], ds.t["raw/data_avg"][:][nonzero_t_i,self.selected_w_i])
            #self._acquisition_lock.release()
            self._update_legend()

    def _crosshairy_changed(self):
        self.crosshair.setPos(self.crosshairx.value(), self.crosshairy.value())
        if not self.xslice_crosshair.value() == self.crosshairy.value():
            self.xslice_crosshair.setPos(self.crosshairy.value())
        new_i = np.argmin(np.abs(ds.d["raw/time"][:] - self.crosshairy.value()))
        if new_i != self.selected_t_i:
            self.selected_t_i = new_i
            #self._acquisition_lock.acquire()
            # Update individual scan traces
            for scan_i, plotitem in enumerate(self.yslice_scan_plots):
                plotitem.setData(ds.d["raw/wavelength"], ds.d["raw/data"][scan_i,self.selected_t_i,:])
            # Update average trace
            self.yslice_plot.setData(ds.d["raw/wavelength"], ds.t["raw/data_avg"][self.selected_t_i,:])
            #self._acquisition_lock.release()
            self._update_legend()

    def _xslice_crosshair_changed(self):
        if not self.xslice_crosshair.value() == self.crosshairy.value():
            self.crosshairy.setPos(self.xslice_crosshair.value())

    def _yslice_crosshair_changed(self):
        if not self.yslice_crosshair.value() == self.crosshairx.value():
            self.crosshairx.setPos(self.yslice_crosshair.value())

    def _crosshair_reset(self):
        # Restrict bounds of crosshairs
        self.crosshair.maxBounds = QRectF(ds.d["raw/wavelength"][0], ds.d["raw/time"][0], ds.d["raw/wavelength"][-1] - ds.d["raw/wavelength"][0], ds.d["raw/time"][-1] - ds.d["raw/time"][0])
        self.crosshairx.setBounds((ds.d["raw/wavelength"][0], ds.d["raw/wavelength"][-1]))
        self.crosshairy.setBounds((ds.d["raw/time"][0], ds.d["raw/time"][-1]))
        self.xslice_crosshair.setBounds((ds.d["raw/time"][0], ds.d["raw/time"][-1]))
        self.yslice_crosshair.setBounds((ds.d["raw/wavelength"][0], ds.d["raw/wavelength"][-1]))
        # Position the crosshairs
        self.selected_w_i = int(ds.d["raw/wavelength"].shape[0]/2)
        self.crosshairx.setPos(ds.d["raw/wavelength"][self.selected_w_i])
        self.selected_t_i = 0
        self.crosshairy.setPos(ds.d["raw/time"][self.selected_t_i])
        self.crosshair.setPos(ds.d["raw/wavelength"][self.selected_w_i], ds.d["raw/time"][self.selected_t_i])
        self.xslice_crosshair.setPos(ds.d["raw/time"][self.selected_t_i])
        self.yslice_crosshair.setPos(ds.d["raw/wavelength"][self.selected_w_i])

    def _axes_reset(self):
        wavelength_scale = (ds.d["raw/wavelength"][-1] - ds.d["raw/wavelength"][0])/(ds.d["raw/wavelength"].shape[0]-1) if ds.d["raw/wavelength"].shape[0] > 1 else 1.0
        delaytime_scale = (ds.d["raw/time"][-1] - ds.d["raw/time"][0])/(ds.d["raw/time"].shape[0]-1) if ds.d["raw/time"].shape[0] > 1 else 1.0
        self.overview.setLimits(xMin=ds.d["raw/wavelength"][0] - wavelength_scale/2, xMax=ds.d["raw/wavelength"][-1] + wavelength_scale/2,
                                yMin=ds.d["raw/time"][0] - delaytime_scale/2, yMax=ds.d["raw/time"][-1] + delaytime_scale/2)
        self.xslice.setLimits(xMin=ds.d["raw/time"][0] - delaytime_scale/2, xMax=ds.d["raw/time"][-1] + delaytime_scale/2,
                              yMin=-2**16, yMax=2**16)
        self.yslice.setLimits(xMin=ds.d["raw/wavelength"][0] - wavelength_scale/2, xMax=ds.d["raw/wavelength"][-1] + wavelength_scale/2,
                                yMin=-2**16, yMax=2**16)
        self.overview.autoRange(pg.ViewBox.XYAxes)
        self.xslice.autoRange(pg.ViewBox.XYAxes)
        self.yslice.autoRange(pg.ViewBox.XYAxes)
        self.overview.enableAutoRange(pg.ViewBox.XYAxes)
        self.xslice.enableAutoRange(pg.ViewBox.XYAxes)
        self.yslice.enableAutoRange(pg.ViewBox.XYAxes)
        self._update_legend()

    def _update_legend(self):
        try:
            self.xslice.legend.items[0][1].setText("Temporal slice λ = {} nm".format(np.round(ds.d["raw/wavelength"][self.selected_w_i].astype(np.float64), 1)))
            self.yslice.legend.items[0][1].setText("Spectral slice t = {} ps".format(np.round(ds.d["raw/time"][self.selected_t_i].astype(np.float64), 1)))
        except Exception:
            # Probably zarr bounds check error when selected index out of range when loading new data
            pass

    def _reset_step_table(self):
        self.stepmodel.clear()
        self.stepmodel.setHorizontalHeaderLabels(["#", "Size (ps)", "Step (ps)"])
        self.stepTableView.setColumnWidth(0, 35)
        self.stepTableView.setColumnWidth(1, 75)
        self.stepTableView.setColumnWidth(2, 65)

    def _steptype_changed(self, value):
        self.fixedStepDoubleSpinBox.setEnabled(not value)
        self.variableControls.setEnabled(bool(value))

    def _addstep_clicked(self):
        self._add_step_table_row()

    def _removestep_clicked(self):
        selected_row = self.stepTableView.selectionModel().currentIndex().row()
        if selected_row == -1: selected_row = self.stepmodel.rowCount() - 1
        self.stepmodel.takeRow(selected_row)
        self.stepTableView.selectionModel().clear()
        self.removeStepPushButton.setEnabled(self.stepmodel.rowCount() > 1)

    def _loadstep_clicked(self):
        # TODO
        pass

    def _add_step_table_row(self, window=100.0, step=1.0):
        windowitem = QtGui.QStandardItem(f"{window:f}".rstrip("0").rstrip(".") + " @")
        windowitem.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        stepitem = QtGui.QStandardItem(f"{step:f}".rstrip("0").rstrip("."))
        countitem = QtGui.QStandardItem(f"{int(window/step) if not step == 0.0 else '?'}")
        countitem.setEditable(False)
        self.stepmodel.appendRow([countitem, windowitem, stepitem])
        # Limit number of rows
        self.addStepPushButton.setEnabled(self.stepmodel.rowCount() < 20)
        self.removeStepPushButton.setEnabled(self.stepmodel.rowCount() > 1)

    def _data_changed(self):
        """Rebuild plots when new data is loaded etc."""

        # Generate average if needed
        if not "raw/data_avg" in ds.t:
            ds.t["raw/data_avg"] = ds.raw_data_average()

        # Remove old scan traces from xslice panel
        for plot in self.xslice_scan_plots:
            self.xslice.removeItem(plot)
        self.xslice_plot.setData()
        self.xslice_scan_plots = []
        # Remove old scan traces from yslice panel
        for plot in self.yslice_scan_plots:
            self.yslice.removeItem(plot)
        self.yslice_plot.setData()
        self.yslice_scan_plots = []
        # Remove overview images
        for img in self.overview_images:
            self.overview.removeItem(img)
        self.overview_images = []

        # Build new kinetic and spectral scan traces
        self.selected_w_i = int(ds.d["raw/wavelength"].shape[0]/2)
        self.selected_t_i = 0
        c_start = np.array(config.data["rawdata"]["scangradient"]["start"])
        c_stop = np.array(config.data["rawdata"]["scangradient"]["stop"])
        # Include all scans if excluded scans not specified yet
        if not "exclude_scans" in ds.t["raw"].attrs:
            ds.t["raw"].attrs["exclude_scans"] = []
        # Ensure any excluded scans are invisible
        scan_enabled_list = np.ones((ds.d["raw/data"].shape[0],), dtype=np.bool)
        scan_enabled_list[ds.t["raw"].attrs["exclude_scans"]] = False
        for i, scan_data in enumerate(ds.d["raw/data"]):
            # Compute colour in the gradient to use
            c = tuple((c_start + ((i/(ds.d["raw/data"].shape[0] - 1)) if ds.d["raw/data"].shape[0] > 1 else 0)*(c_stop - c_start)).astype(np.int))
            nonzero_t_i = np.any(scan_data, axis=1)
            self.xslice_scan_plots.append(self.xslice.plot(ds.d["raw/time"][:][nonzero_t_i], scan_data[nonzero_t_i,self.selected_w_i], pen=c if scan_enabled_list[i] else None)) 
            self.yslice_scan_plots.append(self.yslice.plot(ds.d["raw/wavelength"], scan_data[self.selected_t_i,:], pen=c if scan_enabled_list[i] else None))
            # Store the assigned colour in the PlotItem so we can retrieve it later
            # This way we can toggle pen=None/pen=baseColor to hide an individual trace
            self.xslice_scan_plots[-1].baseColor = c
            self.yslice_scan_plots[-1].baseColor = c
            # Connect to click events
            self.xslice_scan_plots[-1].sigClicked.connect(self.scansWidget.highlight_scan)
            self.xslice_scan_plots[-1].curve.setClickable(True)
            self.yslice_scan_plots[-1].sigClicked.connect(self.scansWidget.highlight_scan)
            self.yslice_scan_plots[-1].curve.setClickable(True)
        # Update the scan selection checkboxes

        
        self.scansWidget.set_scans(list(zip(self.xslice_scan_plots, self.yslice_scan_plots)), checked=scan_enabled_list)
        
        # Update the average traces
        nonzero_t_i = np.any(ds.t["raw/data_avg"], axis=1)
        self.xslice_plot.setData(ds.d["raw/time"][:][nonzero_t_i], ds.t["raw/data_avg"][:][nonzero_t_i,self.selected_w_i])
        self.yslice_plot.setData(ds.d["raw/wavelength"], ds.t["raw/data_avg"][self.selected_t_i,:])
        
        # Generate an image segment for each detected step size range
        steplist = ds.find_stepsizes(ds.d["raw/time"])
        # Wavelength axis should be fairly uniform and common to all segments
        wavelength_scale = (ds.d["raw/wavelength"][-1] - ds.d["raw/wavelength"][0])/(ds.d["raw/wavelength"].shape[0]-1) if ds.d["raw/wavelength"].shape[0] > 1 else 1.0
        tslice_start = 0
        for i, (step_count, _) in enumerate(steplist):
            # Build slice indices for this segment
            tslice_end = tslice_start + step_count + (1 if i == 0 else 0)
            image = pg.ImageItem(ds.t["raw/data_avg"][tslice_start:tslice_end if tslice_end < ds.d["raw/time"].shape[0] else None])
            # TODO: Images don't look absolutely perfectly aligned, may be off-by one errors in indexing here...
            delaytime_scale = (ds.d["raw/time"][tslice_end if tslice_end < ds.d["raw/time"].shape[0] else -1] - ds.d["raw/time"][tslice_start])/(tslice_end - tslice_start) if (tslice_end - tslice_start) > 0 else 1.0
            image.resetTransform()
            image.translate(ds.d["raw/wavelength"][0] - wavelength_scale/2, ds.d["raw/time"][tslice_start] - delaytime_scale/2)
            image.scale(wavelength_scale, delaytime_scale)
            image.setLookupTable(self.cbar.getLookupTable)
            self.overview.addItem(image)
            self.overview_images.append(image)
            tslice_start = tslice_end
        
        # Update colour bar (which links to the invisible composite image)
        # TODO: Can probably downsample this image data to get better performance
        self.overview_composite_image.setImage(ds.t["raw/data_avg"][:])
        
        # Reset view
        self._axes_reset()
        self._crosshair_reset()
        
        # Update the step list
        self._reset_step_table()
        for step in steplist:
            self._add_step_table_row(step[0]*step[1], step[1])
        
        # Update other controls
        self.countSpinBox.setValue(ds.d["raw/data"].shape[0])
        self.windowDoubleSpinBox.setValue(ds.d["raw/time"][-1] - ds.d["raw/time"][0])
        if len(steplist) == 0:
            # Empty data set
            self.startDoubleSpinBox.setEnabled(True)
            self.windowDoubleSpinBox.setEnabled(True)
            self.stepComboBox.setCurrentIndex(0)
            self.stepComboBox.setEnabled(True)
            self.fixedStepDoubleSpinBox.setValue(1)
            self.fixedStepDoubleSpinBox.setEnabled(True)
            self._add_step_table_row()
            self.variableControls.setEnabled(False)
            self.addStepPushButton.setEnabled(True)
            self.removeStepPushButton.setEnabled(False)
            self.countSpinBox.setEnabled(True)
            self.metadataGroupBox.setEnabled(True)
            self.startPushButton.setEnabled(True)
        elif len(steplist) == 1:
            # Only one step size, fixed steps
            self.startDoubleSpinBox.setEnabled(False)
            self.windowDoubleSpinBox.setEnabled(False)
            self.stepComboBox.setCurrentIndex(0)
            self.stepComboBox.setEnabled(False)
            self.fixedStepDoubleSpinBox.setValue(steplist[0][1])
            self.fixedStepDoubleSpinBox.setEnabled(False)
            self.variableControls.setEnabled(False)
            self.addStepPushButton.setEnabled(True)
            self.removeStepPushButton.setEnabled(False)
            self.countSpinBox.setEnabled(False)
            self.metadataGroupBox.setEnabled(False)
            self.startPushButton.setEnabled(False)
        else:
            # Variable step size
            self.startDoubleSpinBox.setEnabled(False)
            self.windowDoubleSpinBox.setEnabled(False)
            self.stepComboBox.setCurrentIndex(1)
            self.stepComboBox.setEnabled(False)
            self.fixedStepDoubleSpinBox.setValue(steplist[0][1])
            self.fixedStepDoubleSpinBox.setEnabled(False)
            self.variableControls.setEnabled(False)
            self.addStepPushButton.setEnabled(True)
            self.removeStepPushButton.setEnabled(True)
            self.countSpinBox.setEnabled(False)
            self.metadataGroupBox.setEnabled(False)
            self.startPushButton.setEnabled(False)

    def _raw_selection_changed(self):
        """Generate new average of selected traces."""
        # Compute new average traces and update
        ds.t["raw/data_avg"] = ds.raw_data_average()
        nonzero_t_i = np.any(ds.t["raw/data_avg"], axis=1)
        self.xslice_plot.setData(ds.d["raw/time"][:][nonzero_t_i], ds.t["raw/data_avg"][:][nonzero_t_i,self.selected_w_i])
        self.yslice_plot.setData(ds.d["raw/wavelength"], ds.t["raw/data_avg"][self.selected_t_i,:])
        # Recompute overview image sections
        steplist = ds.find_stepsizes(ds.d["raw/time"])
        tslice_start = 0
        for i, (step_count, _) in enumerate(steplist):
            tslice_end = tslice_start + step_count + (1 if i == 0 else 0)
            self.overview_images[i].setImage(ds.t["raw/data_avg"][tslice_start:tslice_end if tslice_end < ds.d["raw/time"].shape[0] else None])
            tslice_start = tslice_end
        self._cbar_changed()

    def _cbar_changed(self):
        for image in self.overview_images:
            image.setLookupTable(self.cbar.getLookupTable(n=512))
            image.setLevels(self.cbar.getLevels())
            


class StepsSpinBoxDelegate(QtWidgets.QItemDelegate):
    """
    Delegate used to spawn spinbox controls for editing cells in the QTableView.
    """

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setDecimals(2)
        editor.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)

        if index.column() == 1:
            # Step window
            editor.setRange(0.05, 1000)
        elif index.column == 2:
            # Step size
            editor.setRange(0.05, 100)
            #editor.setSuffix(" @")
        return editor

    def setEditorData(self, spinBox, index):
        value = float(index.model().data(index, QtCore.Qt.EditRole).split()[0])
        spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, f"{value:f}".rstrip("0").rstrip(".") + (" @" if index.column() == 1 else ""), QtCore.Qt.EditRole)
        # Update the step count as well
        window = float(index.model().data(model.index(index.row(), 1), QtCore.Qt.EditRole).split()[0])
        step = float(index.model().data(model.index(index.row(), 2), QtCore.Qt.EditRole).split()[0])
        model.setData(model.index(index.row(), 0), f"{int(window/step)}")

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class DataPanelScansWidget(QtWidgets.QFrame, loadUiType(os.path.join(os.path.dirname(__file__), "datapanelscans.ui"))[0]):
    """
    The QWidget which will be inserted into the GraphicsLayout to display a
    list of checkboxes to disable or enable individiual scans. 
    """

    def __init__(self, parent=None, plotitems=[], label="Scan #{}"):
        super().__init__(parent)
        self.setupUi(self)
        self.scrollWidget.setLayout(FlowLayout())
        self.items = {}
        self.highlighted_item = None
        self.set_scans(plotitems, label=label)
    
    def set_scans(self, plotitems, checked=None, label="Scan #{}"):
        # Remove any existing checkboxes
        for checkbox in self.items.keys():
            self.scrollWidget.layout().removeWidget(checkbox)
            checkbox.setParent(None)
        self.items = {}
        # All checkboxes are checked if not specified
        if checked is None:
            checked = [True]*len(plotitems)
        # Create new checkboxes for given PlotItems
        for i, plotitem in enumerate(plotitems):
            # Ensure plotitem is a tuple
            try:
                plotitem = tuple(plotitem)
            except TypeError:
                plotitem = (plotitem,)
            checkbox = QtWidgets.QCheckBox(label.format(i + 1))
            checkbox.setChecked(bool(checked[i]))
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self._checkbox_clicked(state, checkbox))
            checkbox.installEventFilter(self)
            pen = plotitem[0].baseColor
            # Choose text colour depending on brightness of background
            c_text = "black" if (pen[0] + pen[1] + pen[2])*pen[3] > 97920 else "#d0d0d0"
            checkbox.setStyleSheet(f"QCheckBox {{ background: rgba({pen[0]},{pen[1]},{pen[2]},{pen[3]/255}); color: {c_text} }}")
            self.scrollWidget.layout().addWidget(checkbox)
            self.items[checkbox] = plotitem

    def _checkbox_clicked(self, state, checkbox):
        for plotitem in self.items[checkbox]:
            plotitem.setPen(plotitem.baseColor if state else None)
        # Update the list of excluded scans
        excluded_scans = []
        for i, checkbox in enumerate(self.items.keys()):
            if not checkbox.isChecked():
                excluded_scans.append(i)
        ds.t["raw"].attrs["exclude_scans"] = excluded_scans
        # Notify any listeners of the change to selection
        ds.signals.raw_selection_changed.emit()

    def eventFilter(self, target, event):
        """Event filter to handle mouse movements over scan selection checkboxes and highlight matching scan trace."""
        if not type(target) == QtWidgets.QCheckBox: return False
        if target.isChecked() and (event.type() == QtCore.QEvent.HoverEnter or event.type() == QtCore.QEvent.HoverMove):
            self.highlight_scan(self.items[target][0])
        elif event.type() == QtCore.QEvent.HoverLeave:
            self.highlight_scan(None)
        return False

    def highlight_scan(self, plotitem):
        # Check if item already highlighted
        if self.highlighted_item is not None and self.highlighted_item == plotitem: return
        # Don't respond if plotitem is hidden
        if plotitem is not None and type(plotitem.opts["pen"]) == QtGui.QPen and plotitem.opts["pen"].style() == QtCore.Qt.NoPen: return
        # Remove any existing highlight
        if self.highlighted_item in self.items:
            c = self.items[self.highlighted_item][0].baseColor
            c_text = "black" if (c[0] + c[1] + c[2])*c[3] > 97920 else "#d0d0d0"
            self.highlighted_item.setStyleSheet(f"QCheckBox {{ background: rgba({c[0]},{c[1]},{c[2]},{c[3]/255}); color: {c_text} }}")
            for p in self.items[self.highlighted_item]:
                p.setPen(p.baseColor if self.highlighted_item.isChecked() else None)
            self.highlighted_item = None
        # Allow None to remove highlight
        if plotitem is None: return
        # Loop through items looking for plotitem
        for checkbox, plotitems in self.items.items():
            if plotitem in plotitems:
                # Highlight the checkbox and both plotitems
                c = config.data["rawdata"]["scangradient"]["highlight"]
                checkbox.setStyleSheet(f"QCheckBox {{ background: rgba({c[0]},{c[1]},{c[2]},{c[3]/255}); }}")
                for p in plotitems:
                    p.setPen(c)
                self.highlighted_item = checkbox
                

def main():
    """
    Run the DataPanel as a standalone application.
    """
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = DataPanel()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
