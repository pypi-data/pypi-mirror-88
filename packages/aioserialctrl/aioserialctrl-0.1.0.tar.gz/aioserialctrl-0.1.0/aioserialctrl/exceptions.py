class SerialPortNotConnected(Exception):
    def __str__(self):
        return "Serial port is not connected"


class CommandMustBytesType(TypeError):
    def __str__(self):
        return "Command must be bytes type."


class OutOfRange(Exception):
    def __init__(self, num=0):
        self.msg = "Serial control error"
        if num:
            self.msg = f"{self.msg}: index: {num}"

    def __str__(self, extra_msg=None):
        return self.msg


class SerialPortConnectError(Exception):
    def __init__(self, extra_msg=None):
        self.msg = ""
        if extra_msg:
            self.msg = extra_msg

    def __str__(self, extra_msg=None):
        return self.msg


class SerialCtrlError(Exception):
    def __init__(self, extra_msg=None):
        self.msg = ""
        if extra_msg:
            self.msg = extra_msg

    def __str__(self, extra_msg=None):
        return self.msg