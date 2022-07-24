from fastapi import FastAPI
import serial


app = FastAPI()


@app.get("/")
async def root():
    ser = serial.Serial(port='/dev/ttyUSB0',timeout=1000)
    print(ser.name)
    ser.write(b'show vlan\n')
    outputlist = []
    text = ""
    keepreading = True
    for i in range(10:
        outputlist.append(ser.readline())
    
    outputlist.append(ser.read(64))

    ser.close()
    return {
        "line1": outputlist
    }
