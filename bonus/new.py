#!/usr/bin/env python
# This script reads modbus devices, a multiparameter power meter and the modbus device in this repo

import serial
import minimalmodbus
from registers import *
from settings import *
from time import sleep, strftime, localtime, time

filedata = open(filedir, "a")
ser = serial.Serial(rf_port)
power_meter = minimalmodbus.Instrument(modbus_port, 12)
power_meter.serial.baudrate = 9600
power_meter.serial.bytesize = 8
power_meter.serial.parity = serial.PARITY_NONE
power_meter.serial.stopbits = 1
power_meter.serial.timeout = 1
power_meter.mode = minimalmodbus.MODE_RTU
power_meter.debug = modbus_debug

instrument = minimalmodbus.Instrument(modbus_port, 10)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

pressure_cal = 5/1023.0
temp_cal = 100/65025.0
ambient_temp_register = 0
shaft_temp_register = 1
pressure_register = 2

def save_record(file, line):
    f = open(file, "a")
    f.write(line)
    f.close()


def read_register(device, reg, dec):
    for i in range(2):
        sleep(0.1)
        try:
            return device.read_register(reg, dec)
        except:
            return 0
            pass


def is_verified(frequency):
    if frequency > 40 and frequency < 99:
        return True
    return False


def read_data():
    frequency = None
    for i in range(2):
        apparent_power = read_register(power_meter, rS_T,  0)
        test_frequency = read_register(power_meter, rFrec, 2)
        temperature = read_register(instrument, shaft_temp_register, 0)
        pressure = read_register(instrument, pressure_register, 0)
        if is_verified(test_frequency):
            frequency = test_frequency
            break
    return {
      "frequency": frequency,
      "power": apparent_power,
      "temperature": temp_cal*temperature,
      "pressure": pressure_cal*pressure,
      }


def checktime(sec):
    return round(time() % sec) == 0

count = 0
while True:
    if (checktime(2)):
        count = count +1
        data = read_data()
        date_time = strftime('%Y-%m-%d %H:%M:%S', localtime())
        if data["frequency"]:
            human_message = "%s: %dW, %.1fHz, %.1f*C, %.1fbar" % (
                date_time,
                data["power"],
                data["frequency"],
                data["temperature"],
                data["pressure"]
                )
            print(human_message)
        else:
            print("... modbus error")

        rf_message = "%4d%3d%3d%2d\r" % (
          data["power"],
          int(data["frequency"]*10),
          int(data["temperature"]*10),
          int(data["pressure"]*10),
        )
        print(rf_message)
        ser.write(rf_message.encode())
        print(rf_message)

    

    sleep(0.5)
