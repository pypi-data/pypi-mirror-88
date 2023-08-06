import threading
from time import sleep

import seriallib

from .constants import ByteSize, Parity, StopBits, fDtrControl, BaudRate
from .exceptions import (
    SerialPortNotConnected, CommandMustBytesType, OutOfRange,
    SerialCtrlError, SerialPortConnectError,
)

class DataBuf:
    def __init__(self):
        self.__buf = bytes()

    def size(self):
        return len(self.__buf)

    def is_empty(self):
        return True if self.size() == 0 else False

    def append(self, bytes_data):
        self.__buf += bytes_data

    def pop(self, num):
        ret = self.__buf[:num]
        self.__buf = self.__buf[num:]
        return ret

    def get_all(self):
        num = self.size()
        return self.bytes(num)

    def byte(self):
        return self.bytes(1)

    def bytes(self, num):
        if self.size() < num:
            raise OutOfRange(num)
        return self.pop(num)


class SerialCtrl:
    def __init__(
        self,
        port,
        baudrate=BaudRate.CBR_115200,
        byte_size=ByteSize.EIGHT,
        stop_bits=StopBits.ONESTOPBIT,
        parity=Parity.NOPARITY,
        dtr_control_enable=fDtrControl.DTR_CONTROL_ENABLE,
    ):
        self.port = f"\\\\.\\{port}"
        self.baudrate = int(baudrate)
        self.byte_size = int(byte_size)
        self.stop_bits = int(stop_bits)
        self.parity = int(parity)
        self.dtr_control_enable = int(dtr_control_enable)

        self._handler = 0
        self._connected = False
        self._buf = DataBuf()
        self._store_buf_threading_event = None
        self._store_buf_threading_task = None
        self._is_read_canceled = False

    def open(self):
        error_code, error_msg, self._handler = seriallib.open(
            self.port,
            self.baudrate,
            self.byte_size,
            self.stop_bits,
            self.parity,
            self.dtr_control_enable,
        )
        if error_code == -1:
            self._connected = True
            self._store_buf_threading_event = threading.Event()
            self._store_buf_threading_task = threading.Thread(target=self.__store_data_to_buffer_task)
            self._store_buf_threading_task.start()
        else:
            raise SerialPortConnectError(self.error_format(error_code, error_msg))

    def write(self, buf):
        if not isinstance(buf, bytes):
            raise CommandMustBytesType()

        if self._connected:
            error_code, error_msg = seriallib.write(self._handler, buf, len(buf))
            if error_code != -1:
                raise SerialCtrlError(self.error_format(error_code, error_msg))
        else:
            raise SerialPortNotConnected()

    def read(self, size=1):
        return self._buf.bytes(size)

    def reads(self):
        return self._buf.get_all()

    def read_until(self, expected, timeout=5):
        expected_len = len(expected)
        ret = bytes()
        sleep_time = 0.1

        while timeout >= 0 and not self._is_read_canceled:
            while ret[-expected_len:] != expected:
                if self._buf.is_empty():
                    break
                ret += self._buf.byte()
            else:
                return ret
            timeout -= sleep_time
            sleep(sleep_time)
        return ret

    def cancel_read(self):
        self._is_read_canceled = True

    def __store_data_to_buffer_task(self):
        while not self._store_buf_threading_event.is_set():
            self.store_data_to_buffer()
            sleep(0.1)

    def store_data_to_buffer(self):
        if self._connected:
            error_code, error_msg, data = seriallib.recv(self._handler)
            if error_code != -1:
                raise SerialCtrlError(self.error_format(error_code, error_msg))
            self._buf.append(data)
        else:
            raise SerialPortNotConnected()

    def close(self):
        if self._connected:
            self.cancel_read()
            self._store_buf_threading_event.set()
            self._store_buf_threading_task.join()
            self._store_buf_threading_event = None
            self._store_buf_threading_task = None
            error_code, error_msg = seriallib.close(self._handler)
            if error_code != -1:
                raise SerialCtrlError(self.error_format(error_code, error_msg))
            self._handler = 0
            self._connected = False

    def error_format(self, error_code, error_msg):
        return f"Error code({error_code}): {error_msg.decode('utf-16', errors='ignore')}"

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()


