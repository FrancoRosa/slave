echo '... compile & upload'
arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old ds_nano -u -p COM21
echo '... done'
 