# GHS-DRS1000

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
to leverage the communication with the serial port.
http://pyserial.sourceforge.net/pyserial.html#installation
If you have `pip` installed on your computer, getting PySerial is as easy as
pip install pyserial

- This module depends on PfeifferVacuum, a Python Code to communicate with
the 6 channel Pfeiffer Vacuum TPG256A MaxiGauge pressure gauge controller
via a serial connection.
https://gist.github.com/pklaus/1378695
