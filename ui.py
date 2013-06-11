# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '2chan_scope_ui.ui'
#
# Created: Tue Jun 11 18:18:41 2013
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout.addWidget(self.graphicsView)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.stacked_plot = QtGui.QRadioButton(self.groupBox_2)
        self.stacked_plot.setObjectName(_fromUtf8("stacked_plot"))
        self.buttonGroup = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.stacked_plot)
        self.verticalLayout_2.addWidget(self.stacked_plot)
        self.xy_plot = QtGui.QRadioButton(self.groupBox_2)
        self.xy_plot.setObjectName(_fromUtf8("xy_plot"))
        self.buttonGroup.addButton(self.xy_plot)
        self.verticalLayout_2.addWidget(self.xy_plot)
        self.gridLayout.addWidget(self.groupBox_2, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 6, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_3.setMinimumSize(QtCore.QSize(100, 100))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.i_offset = QtGui.QDial(self.groupBox_3)
        self.i_offset.setMaximumSize(QtCore.QSize(75, 75))
        self.i_offset.setMaximum(99)
        self.i_offset.setWrapping(False)
        self.i_offset.setNotchesVisible(True)
        self.i_offset.setObjectName(_fromUtf8("i_offset"))
        self.gridLayout_2.addWidget(self.i_offset, 0, 4, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 1, 4, 1, 1)
        self.q_offset = QtGui.QDial(self.groupBox_3)
        self.q_offset.setMaximumSize(QtCore.QSize(75, 75))
        self.q_offset.setOrientation(QtCore.Qt.Horizontal)
        self.q_offset.setInvertedAppearance(False)
        self.q_offset.setNotchesVisible(True)
        self.q_offset.setObjectName(_fromUtf8("q_offset"))
        self.gridLayout_2.addWidget(self.q_offset, 0, 5, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 5, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 0, 3, 1, 3)
        self.verticalLayout.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "2 Chan Scope", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Plot Type", None, QtGui.QApplication.UnicodeUTF8))
        self.stacked_plot.setText(QtGui.QApplication.translate("MainWindow", "Stacked Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.xy_plot.setText(QtGui.QApplication.translate("MainWindow", "XY Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Vertical Offsets", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "I Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Q Offset", None, QtGui.QApplication.UnicodeUTF8))

from pyqtgraph import PlotWidget
