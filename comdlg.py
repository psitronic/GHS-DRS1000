# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'comdlg.ui'
#
# Created: Fri Jan 30 10:04:55 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ComDlg(object):
    def setupUi(self, ComDlg):
        ComDlg.setObjectName(_fromUtf8("ComDlg"))
        ComDlg.setWindowModality(QtCore.Qt.WindowModal)
        ComDlg.resize(368, 167)
        self.buttonBox = QtGui.QDialogButtonBox(ComDlg)
        self.buttonBox.setGeometry(QtCore.QRect(100, 120, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.groupBox = QtGui.QGroupBox(ComDlg)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 171, 101))
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.comboBoxPortMaxiGauge = QtGui.QComboBox(self.groupBox)
        self.comboBoxPortMaxiGauge.setGeometry(QtCore.QRect(50, 40, 85, 27))
        self.comboBoxPortMaxiGauge.setObjectName(_fromUtf8("comboBoxPortMaxiGauge"))
        self.comboBoxPortMaxiGauge.addItem(_fromUtf8(""))
        self.comboBoxPortMaxiGauge.addItem(_fromUtf8(""))
        self.comboBoxPortMaxiGauge.addItem(_fromUtf8(""))
        self.comboBoxPortMaxiGauge.addItem(_fromUtf8(""))
        self.comboBoxPortMaxiGauge.addItem(_fromUtf8(""))
        self.comboBoxPortMaxiGauge.addItem(_fromUtf8(""))
        self.comboBoxPortMaxiGauge.addItem(_fromUtf8(""))
        self.comboBoxPortMaxiGauge.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 45, 31, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox_2 = QtGui.QGroupBox(ComDlg)
        self.groupBox_2.setGeometry(QtCore.QRect(190, 10, 171, 101))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 46, 31, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.comboBoxPortGHS = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxPortGHS.setGeometry(QtCore.QRect(50, 40, 85, 27))
        self.comboBoxPortGHS.setObjectName(_fromUtf8("comboBoxPortGHS"))
        self.comboBoxPortGHS.addItem(_fromUtf8(""))
        self.comboBoxPortGHS.addItem(_fromUtf8(""))
        self.comboBoxPortGHS.addItem(_fromUtf8(""))
        self.comboBoxPortGHS.addItem(_fromUtf8(""))
        self.comboBoxPortGHS.addItem(_fromUtf8(""))
        self.comboBoxPortGHS.addItem(_fromUtf8(""))
        self.comboBoxPortGHS.addItem(_fromUtf8(""))
        self.comboBoxPortGHS.addItem(_fromUtf8(""))

        self.retranslateUi(ComDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ComDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ComDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(ComDlg)

    def retranslateUi(self, ComDlg):
        ComDlg.setWindowTitle(_translate("ComDlg", "Communication parameters", None))
        self.groupBox.setTitle(_translate("ComDlg", "MaxiGauge", None))
        self.comboBoxPortMaxiGauge.setItemText(0, _translate("ComDlg", "COM1", None))
        self.comboBoxPortMaxiGauge.setItemText(1, _translate("ComDlg", "COM2", None))
        self.comboBoxPortMaxiGauge.setItemText(2, _translate("ComDlg", "COM3", None))
        self.comboBoxPortMaxiGauge.setItemText(3, _translate("ComDlg", "COM4", None))
        self.comboBoxPortMaxiGauge.setItemText(4, _translate("ComDlg", "COM5", None))
        self.comboBoxPortMaxiGauge.setItemText(5, _translate("ComDlg", "COM6", None))
        self.comboBoxPortMaxiGauge.setItemText(6, _translate("ComDlg", "COM7", None))
        self.comboBoxPortMaxiGauge.setItemText(7, _translate("ComDlg", "COM8", None))
        self.label.setText(_translate("ComDlg", "Port", None))
        self.groupBox_2.setTitle(_translate("ComDlg", "MicroTask", None))
        self.label_2.setText(_translate("ComDlg", "Port", None))
        self.comboBoxPortGHS.setItemText(0, _translate("ComDlg", "COM1", None))
        self.comboBoxPortGHS.setItemText(1, _translate("ComDlg", "COM2", None))
        self.comboBoxPortGHS.setItemText(2, _translate("ComDlg", "COM3", None))
        self.comboBoxPortGHS.setItemText(3, _translate("ComDlg", "COM4", None))
        self.comboBoxPortGHS.setItemText(4, _translate("ComDlg", "COM5", None))
        self.comboBoxPortGHS.setItemText(5, _translate("ComDlg", "COM6", None))
        self.comboBoxPortGHS.setItemText(6, _translate("ComDlg", "COM7", None))
        self.comboBoxPortGHS.setItemText(7, _translate("ComDlg", "COM8", None))

