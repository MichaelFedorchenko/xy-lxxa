"""
    Author: Michael-F
    Version: 1.0
    Date: 2024-07-10
"""
import serial, time

class XYCTRL:
    def __init__(self, port=None, baudrate=None, timeout=None):
        self.streamStarted = False
        self.ser = serial.Serial(
                port='/dev/ttyUSB0' if port is None else port,
                baudrate=9600 if baudrate is None else baudrate,
                bytesize=8,
                parity='N',
                stopbits=1,
                xonxoff=0,
                timeout=10
                )
        # Timeout after send command to XY-LxxA
        self.timeout = 0.1  if timeout is None else timeout

    """ STREAM HANDLERS """
    # START STREAM
    def startStream(self):
        if self.streamStarted:
            raise Exception('STREAM_ALREADY_STARTED')
        try:
            self.ser.write(b'start')
            time.sleep(self.timeout)
            self.streamStarted = True
            return 'STREAM_STARTED'
        except Exception as e:
            raise Exception(f'ERROR: {str(e)}')

    # READ DATA FROM STREAM
    def readFromStream(self):
        if self.streamStarted:
            try:
                res = self.ser.readline().decode("utf-8")
                if len(res) > 0:
                    data = res.split('\n')[0].split(',')
                    return data[0], data[1], data[2], data[3]
                else:
                    return 'NO_DATA'
            except Exception as e:
                raise Exception(f'ERROR: {str(e)}')
        else:
            raise Exception('STREAM_IS_NOT_RUNNING')

    # STOP STREAM
    def stopStream(self):
        if self.streamStarted:
            try:
                self.ser.write(b'stop')
                time.sleep(self.timeout)
                self.streamStarted = False
                return 'STREAM_STOPPED'
            except Exception as e:
                raise Exception(f'ERROR: {str(e)}')
        else:
            raise Exception('STREAM_IS_NOT_RUNNING')

    # ONCE READ MEASURES
    def readMeasure(self):
        if self.streamStarted:
            raise Exception('STREAM_IS_ACTIVE')
        try:
            self.ser.write(b'start')
            time.sleep(self.timeout)
            self.streamStarted = True
            res = self.ser.readline().decode("utf-8")
            self.ser.write(b'stop')
            time.sleep(self.timeout)
            self.streamStarted = False
            if len(res) > 0:
                data = res.split('\n')[0].split(',')
                return data[0], data[1], data[2], data[3]
            else:
                return 'NO_DATA'
        except Exception as e:
            raise Exception(f'ERROR: {str(e)}')

    """ PARAMS HANDLERS """
    # READ PARAMS
    def readSettings(self):
        if self.streamStarted:
            raise Exception('STREAM_IS_RUNNING')
        try:
            self.ser.write(b'read')
            time.sleep(self.timeout)
            res = self.ser.readline().decode("utf-8")
            print(f'STRING FROM UART: {res}')
            if len(res) > 0:
                data = res.split(',')
                return data[0].split('dw')[1], data[1].split('up')[1], data[2].split('\n')[0]
            else:
                return 'NO_DATA'
        except Exception as e:
            raise Exception(f'ERROR: {str(e)}')

    # SETUP VOLTAGE GIST
    def setVoltage(self, s, e):
        try:
            f = '{:0>4.1f}'
            self.ser.write(b'dw' + f.format(s).encode())
            time.sleep(0.1)
            self.ser.write(b'up' + f.format(e).encode())
            time.sleep(self.timeout)
            return 'OK'
        except Exception as e:
            raise Exception(f'ERROR: {str(e)}')

    # SETUP CHARGING TIME
    def setTime(self, hh, mm):
        try:
            f = '{:02d}'
            self.ser.write(b'' + f.format(hh).encode() + ':'.encode() + f.format(mm).encode())
            time.sleep(self.timeout)
            return 'OK'
        except Exception as e:
            raise Exception(f'ERROR: {str(e)}')

    # COMMAND TO RELAY - ON/OFF (1/0)
    def control(self, type=None):
        if type == 1:
            self.ser.write(b'on')
            time.sleep(self.timeout)
            return 'ON'
        elif type == 0:
            self.ser.write(b'off')
            time.sleep(self.timeout)
            return 'OFF'
        else:
            raise Exception('ACCEPT_BINARY_CONTROL')

    """ DISCONNECTOR """
    # PORT DISCONNECT
    def disconnect(self):
        try:
            self.ser.close()
            return 'DISCONNECTED'
        except Exception as e:
            raise Exception(f'ERROR: {str(e)}')
