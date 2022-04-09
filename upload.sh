echo '... compile & upload'
arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old ds_nano -u -p /dev/ttyUSB1 
echo '... done'
 