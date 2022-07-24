import itertools
from os.path import exists
from fastapi import FastAPI, Request
import glob
import serial
from serial import Serial
from pydantic import BaseModel
import re
import collections

category_descriptions = [
    {"name": "Serial Devices", "description": "Methods for listing and working with serial devices."},
    {"name": "Serial IO", "description": "Methods for reading from and writing to serial devices."},
    {"name": "Cached Data", "description": "Methods for reading data that has been cached by the API to either deduce the state of the serial device, or to prevent unnecessary device interaction."}
]

app = FastAPI(
    title="http-to-serial",
    description="REST API for interacting with serial ports.",
    openapi_tags=category_descriptions
)

open_ports = {}

last_chars = collections.deque(maxlen=4096)
last_lines = collections.deque(maxlen=32)

#class


@app.get("/")
async def root():
    return {
        "a": "b"
    }

@app.get("/api/v1/devices", tags=["Serial Devices"])
async def list_available_devices():
    return {
        "usb_devices": list(map(lambda x : x[5:], glob.glob("/dev/ttyUSB*"))),
        "acm_devices": list(map(lambda x : x[5:], glob.glob("/dev/ttyACM*"))),
        "ama_devices": list(map(lambda x : x[5:], glob.glob("/dev/ttyAMA*")))
    }

@app.get("/api/v1/device/{device_name}", tags=["Serial Devices"])
async def check_port_exists(device_name: str):
    if "." not in device_name:
        return {
            "device": device_name,
            "exists": exists("/dev/" + device_name)
        }


@app.get("/api/v1/device/{device_name}/lastlines/{line_count}", tags=["Cached Data"])
async def get_last_n_lines_from_device(device_name: str, line_count: int):
    return {}

@app.get("/api/v1/device/{device_name}/lastchars/{char_count}", tags=["Cached Data"])
async def get_last_n_characters_from_device(device_name: str, char_count: int):
    print(last_chars)
    return {
        "device": device_name,
        "last": char_count,
        "result": list(itertools.islice(last_chars, 0, char_count))
    }



@app.get("/api/v1/device/{device_name}/waiting/in", tags=["Buffers"])
async def get_input_buffer_byte_count(device_name: str):
    if device_name in list(open_ports.keys()):
        return {
            "device_name": device_name,
            "in_waiting": open_ports[device_name].in_waiting
        }
    else:
        return {
            "device_name": device_name,
            "in_waiting": -1
        }

@app.get("/api/v1/device/{device_name}/waiting/out", tags=["Buffers"])
async def get_output_buffer_byte_count(device_name: str):
    if device_name in list(open_ports.keys()):
        return {
            "device_name": device_name,
            "out_waiting": open_ports[device_name].out_waiting
        }
    else:
        return {
            "device_name": device_name,
            "out_waiting": -1
        }


@app.get("/api/v1/device/{device_name}:{baud_rate}/open", tags=["Serial Devices"])
async def open_device(device_name: str, baud_rate: int):
    state = ""
    if device_name not in list(open_ports.keys()):
        open_ports[device_name] = serial.Serial(port='/dev/'+device_name,baudrate=baud_rate,timeout=1)
        state = "opened"
    else:
        state = "already_open"

    return {
        "device_name": open_ports[device_name].name,
        "state": state
    }

@app.get("/api/v1/device/{device_name}:{baud_rate}/close", tags=["Serial Devices"])
async def close_device(device_name: str):
    state = ""
    if device_name in list(open_ports.keys()):
        open_ports[device_name].close()
        state = "closed"
        open_ports.pop(device_name)
    else:
        state = "already_closed"

    return {
        "device_name": device_name,
        "state": state
    }


@app.get("/api/v1/write/{device_name}/{string}", tags=["Serial IO"])
async def write_to_device(device_name: str, string: str):
    if device_name in list(open_ports.keys()):
        return {
            "status": "success",
            "write_result": open_ports[device_name].write(string.encode())
        }
    else:
        return {
            "status": "device not open",
            "write_result": ""
        }

@app.post("/api/v1/write/{device_name}", tags=["Serial IO"])
async def write_raw_to_device(device_name: str, request: Request):
    if device_name in list(open_ports.keys()):
        return {
            "status": "success",
            "write_result": open_ports[device_name].write(request.data)
        }
    else:
        return {
            "status": "device not open",
            "write_result": ""
        }


@app.get("/api/v1/writeline/{device_name}/{string}", tags=["Serial IO"])
async def writeline_to_device(device_name: str, string: str):
    if device_name in list(open_ports.keys()):
        string += "\r\n"
        return {
            "status": "success",
            "write_result": open_ports[device_name].write(string.encode())
        }
    else:
        return {
            "status": "device not open",
            "write_result": ""
        }


@app.get("/api/v1/read/{device_name}/{count}", tags=["Serial IO"])
async def read_n_bytes_from_device(device_name: str, count: int):
    if device_name in list(open_ports.keys()):
        read_result = open_ports[device_name].read(count)
        last_chars.append(read_result)
        return {
            "status": "success",
            "read_result": read_result
        }
    else:
        return {
            "status": "device not open",
            "read_result": ""
        }

@app.get("/api/v1/readline/{device_name}", tags=["Serial IO"])
async def read_line_from_device(device_name: str):
    if device_name in list(open_ports.keys()):
        read_result = open_ports[device_name].readline()
        last_chars.append(read_result)
        return {
            "status": "success",
            "read_result": read_result
        }
    else:
        return {
            "status": "device not open",
            "read_result": ""
        }

@app.get("/api/v1/readall/{device_name}", tags=["Serial IO"])
async def read_all_from_device(device_name: str):
    if device_name in list(open_ports.keys()):
        read_result = open_ports[device_name].readall()
        last_chars.append(read_result)
        return {
            "status": "success",
            "read_result": read_result
        }
    else:
        return {
            "status": "device not open",
            "read_result": ""
        }
