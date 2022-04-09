import minimalmodbus
import serial
from time import sleep

modbus_port = "/dev/ttyUSB0"

instrument = minimalmodbus.Instrument(modbus_port, 10)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU
# instrument.debug = True

pressure_cal = 5/1023
temp_cal = 100/65025
ambient_temp_register = 0
shaft_temp_register = 1
pressure_register = 2


while True:
    sleep(1)
    try:
        ambient_temp = instrument.read_register(
            ambient_temp_register, 0)*temp_cal
        shaft_temp = instrument.read_register(shaft_temp_register, 0)*temp_cal
        pressure = instrument.read_register(pressure_register, 0)*pressure_cal
        txt = "%4.1f°C, %4.1f°C, %4.1fbar" % (
            ambient_temp, shaft_temp, pressure)
        print(txt)
    except:
        pass
