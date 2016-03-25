__author__ = 'Experiment'

from PyQt4 import QtGui

from src.old_gui import gui_custom_widgets as gui_cw


def add_zi_layout(self, vbox, plotBox):
    self.ziPlot = gui_cw.MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)
    plotBox.addWidget(self.ziPlot)
    self.ZILayout = QtGui.QGridLayout()
    self.amp = QtGui.QLineEdit(self.main_widget)
    self.ampL = QtGui.QLabel(self.main_widget)
    self.ampL.setText("Amplitude")
    self.offset = QtGui.QLineEdit(self.main_widget)
    self.offsetL = QtGui.QLabel(self.main_widget)
    self.offsetL.setText("Offset")
    self.freqLow = QtGui.QLineEdit(self.main_widget)
    self.freqLowL = QtGui.QLabel(self.main_widget)
    self.freqLowL.setText("Low Frequency")
    self.freqHigh = QtGui.QLineEdit(self.main_widget)
    self.freqHighL = QtGui.QLabel(self.main_widget)
    self.freqHighL.setText("High Frequency")
    self.sampleNum = QtGui.QLineEdit(self.main_widget)
    self.sampleNumL = QtGui.QLabel(self.main_widget)
    self.sampleNumL.setText("Sample Number")
    self.samplePerPt = QtGui.QLineEdit(self.main_widget)
    self.samplePerPtL = QtGui.QLabel(self.main_widget)
    self.samplePerPtL.setText("Samples Per Point")
    self.saveLocZI = QtGui.QLineEdit(self.main_widget)
    self.saveLocZIL = QtGui.QLabel(self.main_widget)
    self.saveLocZIL.setText("Sweep Save Location")
    self.buttonZI = QtGui.QPushButton('ZI',self.main_widget)
    self.buttonZI.clicked.connect(self.ZIBtnClicked)
    self.buttonZILog = QtGui.QPushButton('Log', self.main_widget)
    self.buttonZILog.setCheckable(True)
    self.buttonZISave = QtGui.QPushButton('Save Sweep', self.main_widget)
    self.buttonZISave.clicked.connect(self.ZISaveClicked)
    self.ZILayout.addWidget(self.amp,2,1)
    self.ZILayout.addWidget(self.ampL,1,1)
    self.ZILayout.addWidget(self.offset,2,2)
    self.ZILayout.addWidget(self.offsetL,1,2)
    self.ZILayout.addWidget(self.freqLow,2,3)
    self.ZILayout.addWidget(self.freqLowL,1,3)
    self.ZILayout.addWidget(self.freqHigh,2,4)
    self.ZILayout.addWidget(self.freqHighL,1,4)
    self.ZILayout.addWidget(self.sampleNum,2,5)
    self.ZILayout.addWidget(self.sampleNumL,1,5)
    self.ZILayout.addWidget(self.samplePerPt,2,6)
    self.ZILayout.addWidget(self.samplePerPtL,1,6)
    self.ZILayout.addWidget(self.saveLocZI,2,7)
    self.ZILayout.addWidget(self.saveLocZIL,1,7)
    self.ZILayout.addWidget(self.buttonZI,1,8)
    self.ZILayout.addWidget(self.buttonZILog,2,8)
    self.ZILayout.addWidget(self.buttonZISave,1,9)
    self.vbox.addLayout(self.ZILayout)
    self.ZIData = None