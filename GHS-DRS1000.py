# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 09:14:24 2015

@author: Andrey A. Sidorenko

Software for monitoring the gas handling system of
the Dilution Refrigerator DRS1000

It is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

It is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PfeifferVacuum.py. If not, see <http://www.gnu.org/licenses/>.

- This module depends on PySerial, a cross platform Python module
- to leverage the communication with the serial port.
- http://pyserial.sourceforge.net/pyserial.html#installation
- If you have `pip` installed on your computer, getting PySerial is as easy as
- pip install pyserial

- This module depends on PfeifferVacuum, a Python Code to communicate with
- the 6 channel Pfeiffer Vacuum TPG256A MaxiGauge pressure gauge controller
- via a serial connection.
- https://gist.github.com/pklaus/1378695
"""

import sys
import platform
from PfeifferVacuum import MaxiGauge, MaxiGaugeError
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime
import GHSPanelUI
import comdlg
import logdlg
from MicroTask import *

__version__="1.0.0"

class NumberThread(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self,parent)
        self.problem = False    
        self.update_time = 1
        self.running = True
        
    def run(self):
        self.problem = False    
        self.initialization()
        self.emit(SIGNAL('panelMessage(QString)'),'Initialization looks ok')
        time.sleep(0.2)
        while True:
            startTime = time.time()
            self.getADCValues()
            time.sleep(0.2)
            self.getKeysValues()
            time.sleep(0.2)
            self.getPressuresValues()
            while (self.update_time - (time.time()-startTime) > .2):
                time.sleep(.2)
            time.sleep(max([0., self.update_time - (time.time()-startTime)]))            
            
    def getADCValues(self):
        try:
            err, values = self.panel.getADC()
            if err == 0:
                self.emit(SIGNAL('updateADC'), values )
            else:
                self.emit(SIGNAL('panelMessage(QString)'),'[ADC] Error code returned: ' + err)
                time.sleep(0.2)
                self.emit(SIGNAL('initProblem(bool)'),self.problem)                        
        except:
            self.emit(SIGNAL('panelMessage(QString)'),'Couldn\'t get ADC values.')        
            time.sleep(0.2)
            self.emit(SIGNAL('initProblem(bool)'),self.problem)     

    def getKeysValues(self):
        try:
            err, values = self.panel.getKeys()
            if err == 0:
                self.emit(SIGNAL('updateKeys'), values )
            else:
                self.emit(SIGNAL('panelMessage(QString)'),'[KEYS] Error code returned: ' + err)  
                time.sleep(0.2)
                self.emit(SIGNAL('initProblem(bool)'),self.problem)                        
        except:
            self.emit(SIGNAL('panelMessage(QString)'),'Couldn\'t get KEYS values.')          
            time.sleep(0.2)
            self.emit(SIGNAL('initProblem(bool)'),self.problem)                        

    def getPressuresValues(self):
        values = []
        try:
            ps = self.mg.pressures()
            for sensor in ps:
                values.append(sensor.pressure)
            time.sleep(0.2)
            self.emit(SIGNAL('updatePressures'), values )
        except:
            self.emit(SIGNAL('panelMessage(QString)'), 'Couldn\'t get pressure values.')         
            time.sleep(0.2)
            self.emit(SIGNAL('initProblem(bool)'),self.problem)                        
    
    def initialization(self):
        self.problem = False
        try:
            self.panel = GHSPanel(str(self.portGHS))
        except:
            self.emit(SIGNAL('panelMessage(QString)'),'Can\'t connect socket to MicroTask')                        
            time.sleep(0.2)
            self.problem = True
            self.emit(SIGNAL('initProblem(bool)'),self.problem)     
            time.sleep(0.2)

        try:
            self.mg = MaxiGauge(str(self.portMG))
        except:
            self.emit(SIGNAL('panelMessage(QString)'),'Can\'t connect socket to MaxiGauge')
            time.sleep(0.2)
            self.problem = True
            self.emit(SIGNAL('initProblem(bool)'),self.problem)     
            time.sleep(0.2)
           
    def stop(self):
        self.terminate()
        time.sleep(0.2)
        
        if not self.problem:
            if self.panel.connection:
                self.panel.connection.close()
                time.sleep(0.5)
                del self.panel
            if self.mg.connection:
                self.mg.connection.close()
                time.sleep(0.5)
                del self.mg
        
    def setAcquisitionPorts(self, portGHS, portMG):
        self.portGHS = portGHS
        self.portMG = portMG

    def setUpdateTime(self, updtime):
        self.update_time = updtime

    def __del__(self):
        self.wait()

class ComDlg(QDialog, comdlg.Ui_ComDlg):
    
    def __init__(self,parent = None):
        super(ComDlg, self).__init__(parent)
        self.setupUi(self)
        #self.updateUi()

class LogDlg(QDialog, logdlg.Ui_LogDlg):
    
    def __init__(self,parent = None):
        super(LogDlg, self).__init__(parent)
        self.setupUi(self)


class MainWindow(QMainWindow,GHSPanelUI.Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)        
        self.setupUi(self)   
        
        self.statustimer = QTimer()
        self.acquirethread = NumberThread()     
        
        self.connect( self.startButton,    SIGNAL("clicked()"), self.start)
        self.connect( self.stopButton,     SIGNAL("clicked()"), self.stop) 
        self.connect( self.acquirethread,  SIGNAL("updateADC"), self.updateADC_ui)
        self.connect( self.acquirethread,  SIGNAL("updateKeys"), self.updateKeys_ui)
        self.connect( self.acquirethread,  SIGNAL("updatePressures"), self.updatePressures_ui)
        self.connect( self.acquirethread,  SIGNAL("panelMessage(QString)"), self.updatelogFrame)        
        self.connect( self.acquirethread,  SIGNAL("initProblem(bool)"), self.stop)
        self.connect( self.actionNewPorts, SIGNAL("triggered()"), self.portNew)
        self.connect( self.actionLogs,     SIGNAL("triggered()"), self.logNew)
        self.connect( self.actionAbout,    SIGNAL("triggered()"), self.helpAbout)   
        
        self.statusbar.showMessage("Ready",5000)
        
        self.portGHS = 'COM3'
        self.portMG = 'COM4'
        
    def helpAbout(self):
        QMessageBox.about(self, "About GHS-DRS1000 Monitor",
        """<b>GHS-DRS1000 Monitor</b> %s
        <p>Copyright &copy; 2014-2015 Andrey A. Sidorenko
        <br>Licensed under the GNU General Public License v.3
        <p>Created by Andrey A. Sidorenko
        <p>Python %s - Qt %s - PyQt %s on %s""" % (
        __version__, platform.python_version(),
        QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def portNew(self):
        
        dialog = ComDlg(self)        
        dialog.comboBoxPortGHS.setCurrentIndex(dialog.comboBoxPortGHS.findText(self.portGHS))
        dialog.comboBoxPortMaxiGauge.setCurrentIndex(dialog.comboBoxPortMaxiGauge.findText(self.portMG))
        
        if dialog.exec_():            
            self.portGHS = dialog.comboBoxPortGHS.currentText()
            self.portMG = dialog.comboBoxPortMaxiGauge.currentText()  
            self.updatelogFrame('New port set')         

    def logNew(self):
        
        dialog = LogDlg(self)        
        if dialog.exec_():            
            self.updatelogFrame('New ')         
        
    def start(self):
        self.running = True
        self.statusbar.showMessage("Running")
        self.updatelogFrame("Started")
        self.stopButton.setEnabled(True)
        self.startButton.setEnabled(False)
        self.menuSettings.setEnabled(False)
        self.acquirethread.setAcquisitionPorts(self.portGHS,self.portMG)
        self.acquirethread.start()


    def stop(self):
        self.running = False
        if self.acquirethread is not None:
            self.acquirethread.stop()
        self.statusbar.showMessage("Idle")
        self.updatelogFrame("Stopped")
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.menuSettings.setEnabled(True)
        
    def updateADC_ui(self, values):        
        self.lcdNumber_P1.display(int(values[0]))
        self.lcdNumber_P2.display(int(values[1]))
        self.lcdNumber_P3.display(int(values[2]))
        self.lcdNumber_P4.display(int(values[3]))
        self.lcdNumber_P5.display(int(values[4]))
        self.lcdNumber_P6.display(int(values[5]))
        self.lcdNumber_P7.display(int(values[6]))
        self.lcdNumber_P8.display(int(values[7]))

    def updateKeys_ui(self, status):

        offstr, onstr = 'closed', 'open'
        stopstr, startstr = 'stopped', 'started'
        
        #------        
        
        if status[21] == 1 and self.radioButton_A0.isChecked():
            self.radioButton_A0.setChecked(False)
            self.updatelogFrame('\'A0\' ' + offstr)
            
        if status[21] == 2 and not self.radioButton_A0.isChecked():
            self.radioButton_A0.setChecked(True)            
            self.updatelogFrame( '\'A0\' ' + onstr)

        if status[51] == 1 and self.radioButton_A1.isChecked():
            self.radioButton_A1.setChecked(False)
            self.updatelogFrame( '\'A1\' ' + offstr)
            
        if status[51] == 2 and not self.radioButton_A1.isChecked():
            self.radioButton_A1.setChecked(True)
            self.updatelogFrame( '\'A1\' ' + onstr)

        if status[42] == 1 and self.radioButton_A2.isChecked():
            self.radioButton_A2.setChecked(False)
            self.updatelogFrame( '\'A2\' ' + offstr)

        if status[42] == 2 and not self.radioButton_A2.isChecked():        
            self.radioButton_A2.setChecked(True)
            self.updatelogFrame( '\'A2\' ' + onstr)
            
        if status[59] == 1 and self.radioButton_A3.isChecked():
            self.radioButton_A3.setChecked(False)
            self.updatelogFrame( '\'A3\' ' + offstr)
            
        if status[59] == 2 and not self.radioButton_A3.isChecked():            
            self.radioButton_A3.setChecked(True)
            self.updatelogFrame( '\'A3\' ' + onstr)

        if status[54] == 1 and self.radioButton_A4.isChecked():
            self.radioButton_A4.setChecked(False)
            self.updatelogFrame( '\'A4\' ' + offstr)
            
        if status[54] == 2 and not self.radioButton_A4.isChecked():
            self.radioButton_A4.setChecked(True)
            self.updatelogFrame( '\'A4\' ' + onstr)
            
        if status[48] == 1 and self.radioButton_A5.isChecked():
            self.radioButton_A5.setChecked(False)
            self.updatelogFrame( '\'A5\' ' + offstr)

        if status[48] == 2 and not self.radioButton_A5.isChecked():
            self.radioButton_A5.setChecked(True)
            self.updatelogFrame( '\'A5\' ' + onstr)

        if status[56] == 1 and self.radioButton_A6.isChecked():
            self.radioButton_A6.setChecked(False)
            self.updatelogFrame( '\'A6\' ' + offstr)

        if status[56] == 2 and not self.radioButton_A6.isChecked():
            self.radioButton_A6.setChecked(True)
            self.updatelogFrame( '\'A6\' ' + onstr)

        if status[50] == 1 and self.radioButton_A7.isChecked():
            self.radioButton_A7.setChecked(False)
            self.updatelogFrame( '\'A7\' ' + offstr)

        if status[50] == 2 and not self.radioButton_A7.isChecked():
            self.radioButton_A7.setChecked(True)
            self.updatelogFrame( '\'A7\' ' + onstr)

        if status[41] == 1 and self.radioButton_A8.isChecked():
            self.radioButton_A8.setChecked(False)
            self.updatelogFrame( '\'A8\' ' + offstr)

        if status[41] == 2 and not self.radioButton_A8.isChecked():
            self.radioButton_A8.setChecked(True)
            self.updatelogFrame( '\'A8\' ' + onstr)

        if status[39] == 1 and self.radioButton_A9.isChecked():
            self.radioButton_A9.setChecked(False)
            self.updatelogFrame( '\'A9\' ' + offstr)

        if status[39] == 2 and not self.radioButton_A9.isChecked():
            self.radioButton_A9.setChecked(True)
            self.updatelogFrame( '\'A9\' ' + onstr)

        if status[45] == 1 and self.radioButton_A10.isChecked():
            self.radioButton_A10.setChecked(False)
            self.updatelogFrame( '\'A10\' ' + offstr)

        if status[45] == 2 and not self.radioButton_A10.isChecked():
            self.radioButton_A10.setChecked(True)
            self.updatelogFrame( '\'A10\' ' + onstr)

        #------
            
        if status[47] == 1 and self.radioButton_Start.isChecked():
            self.radioButton_Start.setChecked(False)
            self.updatelogFrame( '\'START\' ' + offstr)

        if status[47] == 2 and not self.radioButton_Start.isChecked():
            self.radioButton_Start.setChecked(True)
            self.updatelogFrame( '\'START\' ' + onstr)
            
        if status[60] == 1 and self.radioButton_He3.isChecked():
            self.radioButton_He3.setChecked(False)
            self.updatelogFrame( '\'Condensing He3\' ' + stopstr)

        if status[60] == 2 and not self.radioButton_He3.isChecked():
            self.radioButton_He3.setChecked(True)
            self.updatelogFrame( '\'Condensing He3\' ' + startstr)
            
        if status[61] == 1 and self.radioButton_He4.isChecked():
            self.radioButton_He4.setChecked(False)
            self.updatelogFrame( '\'Condensing He4\' ' + stopstr)

        if status[61] == 2 and not self.radioButton_He4.isChecked():
            self.radioButton_He4.setChecked(True)
            self.updatelogFrame( '\'Condensing He4\' ' + startstr)

        if status[62] == 1 and self.radioButton_Norm.isChecked():
            self.radioButton_Norm.setChecked(False)
            self.updatelogFrame( '\'Normal Circulation\' ' + stopstr)

        if status[62] == 2 and not self.radioButton_Norm.isChecked():
            self.radioButton_Norm.setChecked(True)
            self.updatelogFrame( '\'Normal Circulation\' ' + startstr)

        if status[63] == 1 and self.radioButton_Rec.isChecked():
            self.radioButton_Rec.setChecked(False)
            self.updatelogFrame( '\'Recovery\' ' + stopstr)

        if status[63] == 2 and not self.radioButton_Rec.isChecked():
            self.radioButton_Rec.setChecked(True)
            self.updatelogFrame( '\'Recovery\' ' + startstr)

        if status[5] == 1 and self.radioButton_Aux1.isChecked():
            self.radioButton_Aux1.setChecked(False)
            self.updatelogFrame( '\'AUX-1\' ' + offstr)

        if status[5] == 2 and not self.radioButton_Aux1.isChecked():
            self.radioButton_Aux1.setChecked(True)
            self.updatelogFrame( '\'AUX-1\' ' + onstr)

        if status[9] == 1 and self.radioButton_Reset.isChecked():
            self.radioButton_Reset.setChecked(False)
            self.updatelogFrame( '\'Reset\' ' + stopstr)

        if status[9] == 2 and not self.radioButton_Reset.isChecked():
            self.radioButton_Reset.setChecked(True)
            self.updatelogFrame( '\'Reset\' ' + startstr)

        if status[53] == 1 and self.radioButton_Auto.isChecked():
            self.radioButton_Auto.setChecked(False)
            self.updatelogFrame( '\'Auto\' ' + stopstr)

        if status[53] == 2 and not self.radioButton_Auto.isChecked():
            self.radioButton_Auto.setChecked(True)
            self.updatelogFrame( '\'Auto\' ' + startstr)


        #------

        if status[36] == 1 and self.radioButton_0.isChecked():
            self.radioButton_0.setChecked(False)
            self.updatelogFrame( '\'0\' ' + offstr)

        if status[36] == 2 and not self.radioButton_0.isChecked():
            self.radioButton_0.setChecked(True)
            self.updatelogFrame( '\'0\' ' + onstr)

        if status[30] == 1 and self.radioButton_1.isChecked():
            self.radioButton_1.setChecked(False)
            self.updatelogFrame( '\'1\' ' + offstr)

        if status[30] == 2 and not self.radioButton_1.isChecked():
            self.radioButton_1.setChecked(True)
            self.updatelogFrame( '\'1\' ' + onstr)

        if status[35] == 1 and self.radioButton_2.isChecked():
            self.radioButton_2.setChecked(False)
            self.updatelogFrame( '\'2\' ' + offstr)

        if status[35] == 2 and not self.radioButton_2.isChecked():
            self.radioButton_2.setChecked(True)
            self.updatelogFrame( '\'2\' ' + onstr)

        if status[33] == 1 and self.radioButton_3.isChecked():
            self.radioButton_3.setChecked(False)
            self.updatelogFrame( '\'3\' ' + offstr)

        if status[33] == 2 and not self.radioButton_3.isChecked():
            self.radioButton_3.setChecked(True)
            self.updatelogFrame( '\'3\' ' + onstr)

        if status[6] == 1 and self.radioButton_4.isChecked():
            self.radioButton_4.setChecked(False)
            self.updatelogFrame( '\'4\' ' + offstr)

        if status[6] == 2 and not self.radioButton_4.isChecked():
            self.radioButton_4.setChecked(True)
            self.updatelogFrame( '\'4\' ' + onstr)

        if status[8] == 1 and self.radioButton_5.isChecked():
            self.radioButton_5.setChecked(False)
            self.updatelogFrame( '\'5\' ' + offstr)

        if status[8] == 2 and not self.radioButton_5.isChecked():
            self.radioButton_5.setChecked(True)
            self.updatelogFrame( '\'5\' ' + onstr)

        if status[26] == 1 and self.radioButton_6.isChecked():
            self.radioButton_6.setChecked(False)
            self.updatelogFrame( '\'6\' ' + offstr)

        if status[26] == 2 and not self.radioButton_6.isChecked():
            self.radioButton_6.setChecked(True)
            self.updatelogFrame( '\'6\' ' + onstr)

        if status[23] == 1 and self.radioButton_7.isChecked():
            self.radioButton_7.setChecked(False)
            self.updatelogFrame( '\'7\' ' + offstr)

        if status[23] == 2 and not self.radioButton_7.isChecked():
            self.radioButton_7.setChecked(True)
            self.updatelogFrame( '\'7\' ' + onstr)

        if status[29] == 1 and self.radioButton_8.isChecked():
            self.radioButton_8.setChecked(False)
            self.updatelogFrame( '\'8\' ' + offstr)

        if status[29] == 2 and not self.radioButton_8.isChecked():
            self.radioButton_8.setChecked(True)
            self.updatelogFrame( '\'8\' ' + onstr)

        if status[11] == 1 and self.radioButton_9.isChecked():
            self.radioButton_9.setChecked(False)
            self.updatelogFrame( '\'9\' ' + offstr)

        if status[11] == 2 and not self.radioButton_9.isChecked():
            self.radioButton_9.setChecked(True)
            self.updatelogFrame( '\'9\' ' + onstr)

        if status[18] == 1 and self.radioButton_10.isChecked():
            self.radioButton_10.setChecked(False)
            self.updatelogFrame( '\'10\' ' + offstr)

        if status[18] == 2 and not self.radioButton_10.isChecked():
            self.radioButton_10.setChecked(True)
            self.updatelogFrame( '\'10\' ' + onstr)

        if status[20] == 1 and self.radioButton_11.isChecked():
            self.radioButton_11.setChecked(False)
            self.updatelogFrame( '\'11\' ' + offstr)

        if status[20] == 2 and not self.radioButton_11.isChecked():
            self.radioButton_11.setChecked(True)
            self.updatelogFrame( '\'11\' ' + onstr)

        if status[17] == 1 and self.radioButton_12.isChecked():
            self.radioButton_12.setChecked(False)
            self.updatelogFrame( '\'12\' ' + offstr)

        if status[17] == 2 and not self.radioButton_12.isChecked():
            self.radioButton_12.setChecked(True)
            self.updatelogFrame( '\'12\' ' + onstr)

        if status[14] == 1 and self.radioButton_13.isChecked():
            self.radioButton_13.setChecked(False)
            self.updatelogFrame( '\'13\' ' + offstr)

        if status[14] == 2 and not self.radioButton_13.isChecked():
            self.radioButton_13.setChecked(True)
            self.updatelogFrame( '\'13\' ' + onstr)

        if status[12] == 1 and self.radioButton_14.isChecked():
            self.radioButton_14.setChecked(False)
            self.updatelogFrame( '\'14\' ' + offstr)

        if status[12] == 2 and not self.radioButton_14.isChecked():
            self.radioButton_14.setChecked(True)
            self.updatelogFrame( '\'14\' ' + onstr)

        if status[2] == 1 and self.radioButton_15.isChecked():
            self.radioButton_15.setChecked(False)
            self.updatelogFrame( '\'15\' ' + offstr)

        if status[2] == 2 and not self.radioButton_15.isChecked():
            self.radioButton_15.setChecked(True)
            self.updatelogFrame( '\'15\' ' + onstr)

        if status[3] == 1 and self.radioButton_16.isChecked():
            self.radioButton_16.setChecked(False)
            self.updatelogFrame( '\'16\' ' + offstr)

        if status[3] == 2 and not self.radioButton_16.isChecked():
            self.radioButton_16.setChecked(True)
            self.updatelogFrame( '\'16\' ' + onstr)

        if status[27] == 1 and self.radioButton_17.isChecked():
            self.radioButton_17.setChecked(False)
            self.updatelogFrame( '\'17\' ' + offstr)

        if status[27] == 2 and not self.radioButton_17.isChecked():
            self.radioButton_17.setChecked(True)
            self.updatelogFrame( '\'17\' ' + onstr)

         #------

        if status[38] == 1 and self.radioButton_S1.isChecked():
            self.radioButton_S1.setChecked(False)
            self.updatelogFrame( '\'S1\' ' + stopstr)

        if status[38] == 2 and not self.radioButton_S1.isChecked():
            self.radioButton_S1.setChecked(True)
            self.updatelogFrame( '\'S1\' ' + startstr)

        if status[32] == 1 and self.radioButton_S2.isChecked():
            self.radioButton_S2.setChecked(False)
            self.updatelogFrame( '\'S2\' ' + stopstr)

        if status[32] == 2 and not self.radioButton_S2.isChecked():
            self.radioButton_S2.setChecked(True)
            self.updatelogFrame( '\'S2\' ' + startstr)

        if status[24] == 1 and self.radioButton_S3.isChecked():
            self.radioButton_S3.setChecked(False)
            self.updatelogFrame( '\'S3\' ' + stopstr)

        if status[24] == 2 and not self.radioButton_S3.isChecked():
            self.radioButton_S3.setChecked(True)
            self.updatelogFrame( '\'S3\' ' + startstr)

        if status[57] == 1 and self.radioButton_S4.isChecked():
            self.radioButton_S4.setChecked(False)
            self.updatelogFrame( '\'S4\' ' + stopstr)

        if status[57] == 2 and not self.radioButton_S4.isChecked():
            self.radioButton_S4.setChecked(True)
            self.updatelogFrame( '\'S4\' ' + startstr)

        if status[44] == 1 and self.radioButton_S5.isChecked():
            self.radioButton_S5.setChecked(False)
            self.updatelogFrame( '\'S5\' ' + stopstr)

        if status[44] == 2 and not self.radioButton_S5.isChecked():
            self.radioButton_S5.setChecked(True)
            self.updatelogFrame( '\'S5\' ' + startstr)

    def updatePressures_ui(self, values):    
        self.lcdNumber_IVC.display('%.1E' % values[5])
        self.lcdNumber_STIL.display('%.1E' % values[4])
        
    def updatelogFrame(self,message):
        timeStamp=datetime.today().strftime(' [%H:%M:%S, %d-%m-%Y]')
        self.textBrowser.append(message + timeStamp)
        
    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_Escape:
            self.stop()
            time.sleep(0.2)
            self.close()        
         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
#    app.connect(form.startButton, SIGNAL("clicked()"), app, SLOT("quit()"))
    app.exec_()
