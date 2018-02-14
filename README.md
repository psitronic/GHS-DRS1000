# GHS-DRS1000

<img src="https://cpvv6a.db.files.1drv.com/y4mjSkWNxlNnNxA1f8QJ-xInh4R6KzbS1rcGwmCPgt_jLiaSO9zy9DP8R_6QFS65yLIKwd7LqMoCeh_lSCPn840A9CMRTzdpnld_tC2T4fekPXFoa1t8T7RRiZ-mGAHS6BxA_BTpS1u6i7JGJdjTR48s0dTejtwOlCpvu9O3rP_17HA166Wxt6MsZEvadKTjWqqD05UhxMcdWH-7526Ysv9Hw?width=660&height=529&cropmode=none" width="660" height="529" />

The GUI application for monitoring the gas handling system of
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

- This module depends on Qt 4.8 and PyQt 4.11

- This module depends on PfeifferVacuum, a Python Code to communicate with
the 6 channel Pfeiffer Vacuum TPG256A MaxiGauge pressure gauge controller
via a serial connection.
https://gist.github.com/pklaus/1378695
