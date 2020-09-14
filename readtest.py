import serial
import time

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 57600
ser.timeout = 2

STX = bytes.fromhex('02')
CDE = bytes.fromhex('38')
ADD_LSB = bytes.fromhex('00')
ADD_MSB = bytes.fromhex('01')
N_data = bytes.fromhex('01')
CRC_LSB = bytes([STX[0] + CDE[0] + ADD_LSB[0] + N_data[0]])
CRC_MSB = bytes([STX[0] + CDE[0] + ADD_MSB[0] + N_data[0]])
command_LSB = STX + CDE + ADD_LSB + N_data + CRC_LSB
command_MSB = STX + CDE + ADD_MSB + N_data + CRC_MSB

ser.write(command_MSB)
time.sleep(2)
resp_MSB = ser.read(5).hex()
ser.write(command_LSB)
time.sleep(2)
resp_LSB = ser.read(5).hex()

hexval = '0x' + resp_MSB[4:6] + resp_LSB[4:6]
intval = int(hexval,0)

print(resp_MSB)
print(resp_LSB)
print(intval)


