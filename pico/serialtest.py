# read json recored from serial 

import serial
import json

ser_device='/dev/ttyACM0'
baudrate=115200
ser = serial.Serial(ser_device, baudrate, timeout=1)
ser.flush()
print("Serial port opened")
while True:
    if ser.in_waiting > 0:
        print("reading")
        line = ser.readline().decode('utf-8').rs trip()
        print(line)
        record = json.loads(line)
        if record['event'] == 'change':
            if(record['state'].get('re0')) != None:
                print(f"Encoder 0 {record['state']['re0']['direction']} {record['state']['re0']['position']}")
            elif(record['state'].get('re1')) != None:
                print(f"Encoder 1 {record['state']['re1']['direction']} {record['state']['re1']['position']}")
        elif record['event'] == 'init':
            print("Init event received")