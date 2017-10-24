# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logdlg.ui'
#
# Created: Tue Feb  3 11:17:52 2015
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

class Ui_LogDlg(object):
    def setupUi(self, LogDlg):
        LogDlg.setObjectName(_fromUtf8("LogDlg"))
        LogDlg.setWindowModality(QtCore.Qt.WindowModal)
        LogDlg.resize(368, 167)
        self.buttonBox = QtGui.QDialogButtonBox(LogDlg)
        self.buttonBox.setGeometry(QtCore.QRect(100, 120, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(LogDlg)
        self.label.setGeometry(QtCore.QRect(30, 25, 101, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.spinBoxUpdate = QtGui.QSpinBox(LogDlg)
        self.spinBoxUpdate.setGeometry(QtCore.QRect(170, 20, 59, 27))
        self.spinBoxUpdate.setMinimum(1)
        self.spinBoxUpdate.setMaximum(1800)
        self.spinBoxUpdate.setProperty("value", 1)
        self.spinBoxUpdate.setObjectName(_fromUtf8("spinBoxUpdate"))
        self.label_3 = QtGui.QLabel(LogDlg)
        self.label_3.setGeometry(QtCore.QRect(30, 74, 121, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.spinBoxSave = QtGui.QSpinBox(LogDlg)
        self.spinBoxSave.setEnabled(True)
        self.spinBoxSave.setGeometry(QtCore.QRect(170, 70, 59, 27))
        self.spinBoxSave.setMinimum(1)
        self.spinBoxSave.setMaximum(100)
        self.spinBoxSave.setObjectName(_fromUtf8("spinBoxSave"))

        self.retranslateUi(LogDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LogDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LogDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(LogDlg)

    def retranslateUi(self, LogDlg):
        LogDlg.setWindowTitle(_translate("LogDlg", "Dialog", None))
        self.label.setText(_translate("LogDlg", "Update every", None))
        self.label_3.setText(_translate("LogDlg", "Save to file every", None))

