import asyncio
import concurrent.futures
from typing import Optional

from .constants import ByteSize, Parity, StopBits, fDtrControl, BaudRate
from .serialctrl import SerialCtrl


class AioSerialCtrl(SerialCtrl):
    def __init__(
        self,
        port: str,
        baudrate=BaudRate.CBR_115200,
        byte_size=ByteSize.EIGHT,
        stop_bits=StopBits.ONESTOPBIT,
        parity=Parity.NOPARITY,
        dtr_control_enable=fDtrControl.DTR_CONTROL_ENABLE,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        cancel_read_timeout: int = 1,
    ):
        super().__init__(
            port=port,
            baudrate=baudrate,
            byte_size=byte_size,
            stop_bits=stop_bits,
            parity=parity,
            dtr_control_enable=dtr_control_enable,
        )
        self._loop = loop if loop else asyncio.get_event_loop()
        self._cancel_read_timeout = cancel_read_timeout
        self.__read_lock = asyncio.Lock()
        self.__write_lock = asyncio.Lock()
        self._write_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._read_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._cancel_read_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    async def async_write(self, buf):
        async with self.__write_lock:
            try:
                return await self._loop.run_in_executor(
                    self._write_executor, self.write, buf)
            except asyncio.CancelledError:
                raise

    async def async_read(self, size=1):
        async with self.__read_lock:
            try:
                return await self._loop.run_in_executor(
                    self._read_executor, self.read, size)
            except asyncio.CancelledError:
                raise

    async def async_reads(self):
        async with self.__read_lock:
            try:
                return await self._loop.run_in_executor(
                    self._read_executor, self.reads)
            except asyncio.CancelledError:
                raise

    async def async_read_until(self, expected, timeout=5):
        async with self.__read_lock:
            try:
                return await self._loop.run_in_executor(
                    self._read_executor, self.read_until, expected, timeout)
            except asyncio.CancelledError:
                await asyncio.shield(self._cancel_read_async())
                raise

    async def _cancel_read_async(self):
        await asyncio.wait_for(
            self._loop.run_in_executor(
                self._cancel_read_executor, self.cancel_read
            ),
            self._cancel_read_timeout
        )