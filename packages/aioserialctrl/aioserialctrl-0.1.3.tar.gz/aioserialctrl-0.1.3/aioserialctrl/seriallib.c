#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <SetupAPI.h>

#define MAX_DATA_LENGTH 65535
#define ERR_MSG_LENGTH 65535
#define PORT_INFO_LENGTH 65535


struct PortInfo {
    char portName[PORT_INFO_LENGTH];
    char physName[PORT_INFO_LENGTH];
    char friendName[PORT_INFO_LENGTH];
    char enumName[PORT_INFO_LENGTH];
};

void getDeviceProperty(HDEVINFO devInfo, PSP_DEVINFO_DATA devData, DWORD property, char* data) {
    DWORD buffSize = 0;
    SetupDiGetDeviceRegistryProperty(devInfo, devData, property, NULL, NULL, 0, & buffSize);
    char* buff = (char*)malloc(sizeof(char) * buffSize);
    if (!SetupDiGetDeviceRegistryProperty(devInfo, devData, property, NULL, (LPBYTE)buff, buffSize, NULL)) {
        printf("Can not obtain property: %ld", property); 
    }
    
    strncpy(data, buff, buffSize);
    free(buff);
}

void getRegKeyValue(HKEY key, LPCTSTR property, char* data) {
    DWORD size = 0;
    RegQueryValueEx(key, property, NULL, NULL, NULL, & size);
    char* buff = (char*)malloc(sizeof(char) * size);
    if (RegQueryValueEx(key, property, NULL, NULL, (LPBYTE)buff, &size) == ERROR_SUCCESS) {
        strncpy(data, buff, size);
    } else {
        printf("getRegKeyValue can not obtain value from registry");
    }
    free(buff);
}

int getAllSerialPortInfo(PyObject *serialPortList){
    HDEVINFO devInfo = INVALID_HANDLE_VALUE;

    DWORD dwGuids = 0;
    SetupDiClassGuidsFromName(TEXT("Ports"), NULL, 0, &dwGuids);
    if (dwGuids == 0) {
        printf("SetupDiClassGuidsFromName error: Error code: %ld", GetLastError());
        return INVALID_HANDLE_VALUE;
    }
    GUID *pGuids = (GUID*)malloc(sizeof(GUID) * dwGuids);
    if (!SetupDiClassGuidsFromName(TEXT("Ports"), pGuids, dwGuids, &dwGuids)) {
        printf("SetupDiClassGuidsFromName second call error: Error code: %ld", GetLastError());
        return INVALID_HANDLE_VALUE;
    }

    devInfo = SetupDiGetClassDevs(pGuids, NULL, NULL, DIGCF_PRESENT);
    if (devInfo == INVALID_HANDLE_VALUE) {
        printf("SetupDiGetClassDevs error: Error code: %ld", GetLastError());
        return INVALID_HANDLE_VALUE;
    }
    free(pGuids);

    int ok_flag = 1;
    SP_DEVINFO_DATA devData = {sizeof(SP_DEVINFO_DATA)};

    for (DWORD i = 0; ok_flag; i++) {
        ok_flag = SetupDiEnumDeviceInfo(devInfo, i, &devData);
        if (ok_flag) {
            struct PortInfo info;
            getDeviceProperty(devInfo, &devData, SPDRP_FRIENDLYNAME, info.friendName);
            getDeviceProperty(devInfo, &devData, SPDRP_PHYSICAL_DEVICE_OBJECT_NAME, info.physName);
            getDeviceProperty(devInfo, &devData, SPDRP_ENUMERATOR_NAME, info.enumName);
            HKEY devKey = SetupDiOpenDevRegKey(devInfo, &devData, DICS_FLAG_GLOBAL, 0, DIREG_DEV, KEY_READ);
            getRegKeyValue(devKey, TEXT("PortName"), info.portName);
            RegCloseKey(devKey);
            if (strncmp(info.portName, "COM", 3) == 0) {
                PyObject *tempTuple = PyTuple_New(4);
                PyTuple_SET_ITEM(tempTuple, 0, Py_BuildValue("y", info.portName));
                PyTuple_SET_ITEM(tempTuple, 1, Py_BuildValue("y", info.physName));
                PyTuple_SET_ITEM(tempTuple, 2, Py_BuildValue("y", info.friendName));
                PyTuple_SET_ITEM(tempTuple, 3, Py_BuildValue("y", info.enumName));
                PyList_Append(serialPortList, tempTuple);
            }
        } else {
            if (GetLastError() != ERROR_NO_MORE_ITEMS) {
                return 0;
            }
        }
    }
    return 0;
}

int serialPortOpen(char* port, int baudRate, int byteSize, int stopBits, int parity, int dtrControlEnable) {
    HANDLE handler = CreateFile(port,
                                GENERIC_READ | GENERIC_WRITE,
                                0,
                                NULL,
                                OPEN_EXISTING,
                                FILE_ATTRIBUTE_NORMAL,
                                NULL);

    if (handler == INVALID_HANDLE_VALUE) {
        if (GetLastError() == ERROR_FILE_NOT_FOUND) {
            puts("ERROR: Handle was not attached.Reason: not available");
        } else {
            puts("ERROR!");
        }
        return 0;
    }
    DCB dcbSerialParameters = {0};

    if (!GetCommState(handler, &dcbSerialParameters)) {
        puts("Failed to get current serial parameters");
    } else {
        dcbSerialParameters.BaudRate = baudRate;
        dcbSerialParameters.ByteSize = byteSize;
        dcbSerialParameters.StopBits = stopBits;
        dcbSerialParameters.Parity = parity;
        dcbSerialParameters.fDtrControl = dtrControlEnable;

        if (!SetCommState(handler, &dcbSerialParameters)) {
            puts("Could not set serial port parameters");
        } else {
            PurgeComm(handler, PURGE_RXCLEAR | PURGE_TXCLEAR);
            return (int)handler;
        }
    }
    return 0;
}

int serialPortWrite(int handler, const char *data, unsigned int dataSize) {
    COMSTAT status;
    DWORD errors;
    if (!WriteFile((HANDLE)handler, (void*)data, dataSize, NULL, 0)) {
        ClearCommError((HANDLE)handler, &errors, &status);
        return 0;
    }

    return 1;
}

int serialPortRecv(int handler, char *data, unsigned int dataSize) {
    DWORD bytesRead;
    COMSTAT status;
    DWORD errors;
    unsigned int toRead = 0;

    ClearCommError((HANDLE)handler, &errors, &status);

    if (status.cbInQue > 0) {
        if (status.cbInQue > dataSize) {
            toRead = dataSize;
        } else {
            toRead = status.cbInQue;
        }
    }
    memset((void*)data, 0, dataSize);
    if (ReadFile((HANDLE)handler, (void*)data, toRead, &bytesRead, NULL)) {
        return bytesRead;
    }

    return 0;
}

int serialPortClose(int handler) {
    return CloseHandle((HANDLE)handler);
}


static PyObject *_getAllSerialPortInfo(PyObject *self, PyObject *args, PyObject *kwargs) {
    PyObject *serialPortList = PyList_New(0);
    if (getAllSerialPortInfo(serialPortList) == INVALID_HANDLE_VALUE) {
        return NULL;
    }

    return serialPortList;
}

static PyObject *_serialPortOpen(PyObject *self, PyObject *args, PyObject *kwargs) {
    char* port;
    int baudRate;
    int byteSize;
    int stopBits;
    int parity;
    int dtrControlEnable;
    static char *kwlist[] = {
        "port", "baudRate", "byteSize", "stopBits",
        "parity", "dtrControlEnable", NULL};
    int handler;
    DWORD errCode = -1;
    wchar_t errMsg[ERR_MSG_LENGTH] = L"";

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ziiiii", kwlist,
            &port, &baudRate, &byteSize, &stopBits, &parity, &dtrControlEnable)) {
        return NULL;
    }

    handler = serialPortOpen(port, baudRate, byteSize, stopBits, parity, dtrControlEnable);
    if (handler == 0) {
        errCode = GetLastError();
        FormatMessageW(
            FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
            NULL,
            errCode,
            MAKELANGID(LANG_SYSTEM_DEFAULT, SUBLANG_SYS_DEFAULT),
            errMsg,
            ERR_MSG_LENGTH,
            NULL
        );
    }

    return Py_BuildValue("iyi", errCode, errMsg, handler);
}

static PyObject *_serialPortWrite(PyObject *self, PyObject *args, PyObject *kwargs) {
    int handler;
    char* cmd;
    int cmdLen;
    static char *kwlist[] = {"handler", "cmd", "cmdLen", NULL};
    int flag;
    DWORD errCode = -1;
    wchar_t errMsg[ERR_MSG_LENGTH] = L"";

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iyi", kwlist, &handler, &cmd, &cmdLen)) {
        return NULL;
    }

    flag = serialPortWrite(handler, cmd, cmdLen);
    if (flag == 0) {
        errCode = GetLastError();
        FormatMessageW(
            FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
            NULL,
            errCode,
            MAKELANGID(LANG_SYSTEM_DEFAULT, SUBLANG_SYS_DEFAULT),
            errMsg,
            ERR_MSG_LENGTH,
            NULL
        );
    }

    return Py_BuildValue("iy", errCode, errMsg);
}

static PyObject *_serialPortRecv(PyObject *self, PyObject *args, PyObject *kwargs) {
    int handler;
    static char *kwlist[] = {"handler", NULL};
    int len;
    char buf[MAX_DATA_LENGTH];
    DWORD errCode = -1;
    wchar_t errMsg[ERR_MSG_LENGTH] = L"";

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i", kwlist, &handler)) {
        return NULL;
    }

    len = serialPortRecv(handler, buf, MAX_DATA_LENGTH);
    errCode = GetLastError();
    if (errCode > 0) {
        errCode = GetLastError();
        FormatMessageW(
            FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
            NULL,
            errCode,
            MAKELANGID(LANG_SYSTEM_DEFAULT, SUBLANG_SYS_DEFAULT),
            errMsg,
            ERR_MSG_LENGTH,
            NULL
        );
    } else {
        errCode = -1;
    }

    return Py_BuildValue("iyy#", errCode, errMsg, buf, len);
}

static PyObject *_serialPortClose(PyObject *self, PyObject *args, PyObject *kwargs) {
    int handler;
    static char *kwlist[] = {"handler", NULL};
    int flag;
    DWORD errCode = -1;
    wchar_t errMsg[ERR_MSG_LENGTH] = L"";

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i", kwlist, &handler)) {
        return NULL;
    }

    flag = serialPortClose(handler);
    if (flag == 0) {
        errCode = GetLastError();
        FormatMessageW(
            FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
            NULL,
            errCode,
            MAKELANGID(LANG_SYSTEM_DEFAULT, SUBLANG_SYS_DEFAULT),
            errMsg,
            ERR_MSG_LENGTH,
            NULL
        );
    }

    return Py_BuildValue("iy", errCode, errMsg);
}

static PyMethodDef RunPEMethods[] = {
    {"get_all_serial_port_info", (PyCFunction) _getAllSerialPortInfo, METH_VARARGS | METH_KEYWORDS, "Get all serail port info."},
    {"open", (PyCFunction) _serialPortOpen, METH_VARARGS | METH_KEYWORDS, "Connect serail port."},
    {"write", (PyCFunction) _serialPortWrite, METH_VARARGS | METH_KEYWORDS, "Write to serail port."},
    {"recv", (PyCFunction) _serialPortRecv, METH_VARARGS | METH_KEYWORDS, "Recv from serail port."},
    {"close", (PyCFunction) _serialPortClose, METH_VARARGS | METH_KEYWORDS, "Close serail port."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef seriallibModule = {
    PyModuleDef_HEAD_INIT,
    "seriallib",
    "A module serail port control.",
    -1,
    RunPEMethods
};

PyMODINIT_FUNC PyInit_seriallib() {
    return PyModule_Create(&seriallibModule);
}