# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 10:54:14 2014

@author: Andrey A. Sidorenko

MicroTask.py is a part of software for reading values/keys from
the gas handling system of the Dilution Refrigerator DRS1000

MicroTask.py is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MicroTask.py is distributed in the hope that it will be useful,
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
"""

import serial
import time
import signal
import math

class GHSPanel(object):
    def __init__(self, serialPort, baud=9600, debug=False):
        self.debug=debug
        try:
            self.connection = serial.Serial(port=serialPort, baudrate=baud, bytesize=8, parity='N', stopbits=1, timeout=1)
        except serial.serialutil.SerialException as se:
            raise se
            pass
        self.logfilename = ''
        
    def checkStatus(self):
        id = self.send('STATUS?')
        return id
    
    def errorCode(self):
        pass
    
    def getADC(self):
        Poffset = [0.6098,0.6083,0.61409,1,0.6073,0.6081,0.60849,0.0468]
        status, values = self.send('ADC?')
        valuescorr = [int(values[i] * Poffset[i]) for i in range(8)]
        return status, valuescorr
        
    def getKeys(self):
        status, keymap = self.send('KEYS?')
        return status, keymap
    
    def send(self, command):
        self.connection.flushInput()
        self.connection.write(command + LINE_TERMINATION_GHS)
        response_str = self.connection.readline().split("\n")[0]
        response = response_str.split("\t")
        errcode = int(response[0])
        vals = response[1].split(",")
        data = []
        for raw_vals in vals:
            data.append(int(raw_vals))
        return errcode, data
     
     
    def __del__(self):
#        self.disconnect()
        if hasattr(self,'connection') and self.connection: self.connection.close()

    
### Special characters: command end or command separators    
SPECIAL_CHARACTERS_GHS = { 
  'CR':  "\x0D", # Carriage Return
  'LF':  "\x0A", # Line Feed
  'HT': "\x09", # Command Separator
  'SPACE': "\x20", # Empty Character Place
}

LINE_TERMINATION_GHS = SPECIAL_CHARACTERS_GHS['LF']

### Functional command set
COMMAND_GHS = {
  'ID?',      # Get identification of panel
  'ID2?',     # Get identification 2 of panel
  'ADC?',     # Ask adc values of on-board measuremnts
  'KEYS?',    # 
  'STATUS?',  # 
}

### Acknowledge types. Return value after sending a command
ERR_ID_GHS = {
  0:  "No error",
  1:  "Command error",
  2:  "Syntax error",
  3:  "Parameter error",
  4:  "Communication error",
  5:  "Execution error",
}

### System Status
STATUS_ID_GHS = {
  1:  "Start",
  2:  "3He",
  3:  "4He",
  4:  "Normal circulation",
  5:  "Recovery",
}
