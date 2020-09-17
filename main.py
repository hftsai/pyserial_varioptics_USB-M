from cameralibnew import *

print(serial.__version__)
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

ser = serial.Serial('COM5')
ser.baudrate = 57600
ser.timeout = 2

print(camera_init(ser))
for i in range(0,46000,100):
    print(set_focus_value(ser, i))
    time.sleep(1)
    
    volt = get_focus_value(ser)
    volt_converted = volt*0.001+24
    print('Voltage is ' + str(volt_converted))
    print('=============')


# ser.close()