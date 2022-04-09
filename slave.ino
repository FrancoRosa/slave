#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <SoftwareSerial.h>
#include "src/ModbusRTUSlave/ModbusRTUSlave.h"

const byte ledPin = 13,
           rxPin = 10, txPin = 11, dePin = 3,
           id = 10,
           sensorPin = A0;

const word bufSize = 256, numHoldingRegisters = 3,
           ambientTempAddress = 0, shaftTempAddress = 1, pressureAddress = 2;
const unsigned long baud = 9600;

byte buf[bufSize];
byte amb_temp;
byte shaft_temp;

SoftwareSerial mySerial(rxPin, txPin);
ModbusRTUSlave modbus(mySerial, buf, bufSize, dePin);
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
const float temp_constant = 65025 / 100.0;

long holdingRegisterRead(word address)
{
  digitalWrite(ledPin, !digitalRead(ledPin));
  switch (address)
  {
  case ambientTempAddress:
    return mlx.readAmbientTempC() * temp_constant;
    break;

  case shaftTempAddress:
    return mlx.readObjectTempC() * temp_constant;
    break;

  case pressureAddress:
    return analogRead(sensorPin);
    break;

  default:
    return false;
    break;
  }
}

boolean holdingRegisterWrite(word address, word value)
{
  return true;
}

void setup()
{
  mlx.begin();
  pinMode(ledPin, OUTPUT);
  mySerial.begin(baud);
  modbus.begin(id, baud);
  modbus.configureHoldingRegisters(numHoldingRegisters, holdingRegisterRead, holdingRegisterWrite);
}

void loop()
{
  modbus.poll();
}