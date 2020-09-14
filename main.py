from cameralib import *

print(serial.__version__)
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 57600
ser.timeout = 2

print(camera_init(ser))
for i in range(0,46000,1000):
    print(set_focus_value(ser, i))
    time.sleep(1)
    print('focus value is now at ')
    print(get_focus_value(ser))

# ser.close()