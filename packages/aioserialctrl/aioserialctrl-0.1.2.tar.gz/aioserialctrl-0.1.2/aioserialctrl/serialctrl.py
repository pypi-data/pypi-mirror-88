import threading
from time import sleep
from contextlib import contextmanager

import seriallib

from .constants import ByteSize, Parity, StopBits, fDtrControl, BaudRate
from .exceptions import (
    SerialPortNotConnected, CommandMustBytesType, OutOfRange,
    SerialCtrlError, SerialPortConnectError,
)

class RWLock:
    def __init__(self, timeout=-1):
        self._lock = threading.Lock()
        self._timeout = timeout

    def acquire(self, timeout=None):
        if timeout == None:
            current_timeout = self._timeout
        else:
            current_timeout = timeout

        self._lock.acquire(timeout=current_timeout)

    def release(self):
        self._lock.release()

    @contextmanager
    def locked(self, timeout=None):
        try:
            self.acquire(timeout=timeout)
            yield self._lock
        finally:
            self.release()

class DataBuf:
    def __init__(self):
        self._buf = bytes(b"")
        self.rwlock = RWLock(timeout=3)

    def size(self):
        return len(self._buf)

    def is_empty(self):
        return True if self.size() == 0 else False

    def append(self, bytes_data):
        with self.rwlock.locked():
            self._buf += bytes_data

    def pop(self, num):
        with self.rwlock.locked():
            ret = self._buf[:num]
            self._buf = self._buf[num:]
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
        self._store_buf_threading_exception = None
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

        if not self._connected:
            raise SerialPortNotConnected()

        error_code, error_msg = seriallib.write(self._handler, buf, len(buf))
        if error_code != -1:
            raise SerialCtrlError(self.error_format(error_code, error_msg))

    def read(self, size=1):
        if not self._connected:
            raise SerialPortNotConnected()
        return self._buf.bytes(size)

    def reads(self):
        if not self._connected:
            raise SerialPortNotConnected()
        return self._buf.get_all()

    def read_until(self, expected, timeout=5):
        if not self._connected:
            raise SerialPortNotConnected()
        expected_len = len(expected)
        ret = bytes(b"")
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
            try:
                self.store_data_to_buffer()
            except Exception as err:
                if not self._store_buf_threading_event.is_set():
                    self._store_buf_threading_exception = err
                break
            sleep(0.1)
        if not self._store_buf_threading_event.is_set():
            self.close()

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
            try:
                self._store_buf_threading_task.join()
            except:
                pass
            self._store_buf_threading_event = None
            self._store_buf_threading_task = None
            error_code, error_msg = seriallib.close(self._handler)
            if error_code != -1:
                raise SerialCtrlError(self.error_format(error_code, error_msg))
            self._handler = 0
            self._connected = False

            if self._store_buf_threading_exception:
                temp_exception = self._store_buf_threading_exception
                self._store_buf_threading_exception = None
                raise temp_exception

    def error_format(self, error_code, error_msg):
        return f"Error code({error_code}): {error_msg.decode('utf-16', errors='ignore')}"

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()


