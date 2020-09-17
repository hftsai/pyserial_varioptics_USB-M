import serial
import serial.tools.list_ports
import time


sleep_time = 0.001

def camera_init(ser, Analog=False, Standby=False):
    STX = bytes.fromhex('02')
    CDE = bytes.fromhex('37')
    ADD = bytes.fromhex('03')
    N_data = bytes.fromhex('01')
    if Analog == True:
        if Standby == True:
            Data = bytes.fromhex('03')
        else:
            Data = bytes.fromhex("02")
    else:
        if Standby == True:
            Data = bytes.fromhex("01")
        else:
            Data = bytes.fromhex("00")
    CRC = bytes([STX[0]+CDE[0]+ADD[0]+N_data[0]+Data[0]])
    command = STX + CDE + ADD + N_data + Data + CRC
    ser.write(command)
    print('Writing Data ...')
    print(command)
    time.sleep(sleep_time)
    response =  ser.read(4)

    if response == b'\x027\x06?':
        print('Write Successful')
        print('Camera Initialized')
        return True
    elif response == b'\x027\x15N':
        print('Write Unsuccessful')
        return False
    else:
        print('Unknown Resposne')
        return None


def save_enable(ser, boolval):
    STX = bytes.fromhex('02')
    CDE = bytes.fromhex('37')
    ADD = bytes.fromhex('02')
    N_data = bytes.fromhex('01')
    if boolval == True:
        Data = bytes.fromhex('01')
    else:
        Data = bytes.fromhex('00')

    CRC = bytes([STX[0] + CDE[0] + ADD[0] + N_data[0] + Data[0]])
    command = STX + CDE + ADD + N_data + Data + CRC
    ser.write(command)
    print('Writting Data ...')
    print(command)
    time.sleep(sleep_time)
    response = ser.read(4)

    if response == b'\x027\x06?':
        print('Write Successful')
        return True
    elif response == b'\x027\x15N':
        print('Write Unsuccessful')
        return False
    else:
        print('Unknown Resposne')
        return None


def set_focus_value(ser, intval):
    value = intval
    padding = 6
    mainhex = f"{value:#0{padding}x}"
    hexval = mainhex[2:]

    if len(hexval) != 4:
        print('Invalid Hex Value')
        return False
    else:
        STX = bytes.fromhex('02')
        CDE = bytes.fromhex('37')
        N_data = bytes.fromhex('01')
        ADD_LSB = bytes.fromhex('00')
        ADD_MSB = bytes.fromhex('01')
        Data_MSB = bytes.fromhex(hexval[0:2])
        Data_LSB = bytes.fromhex(hexval[2:])
        CRC_LSB = [STX[0] + CDE[0] + ADD_LSB[0] + N_data[0] + Data_LSB[0]]
        CRC_LSB = bytes([CRC_LSB[0] % 256])
        CRC_MSB = [STX[0] + CDE[0] + ADD_MSB[0] + N_data[0] + Data_MSB[0]]
        CRC_MSB = bytes([CRC_MSB[0] % 256])
        command_LSB = STX + CDE + ADD_LSB + N_data + Data_LSB + CRC_LSB
        command_MSB = STX + CDE + ADD_MSB + N_data + Data_MSB + CRC_MSB

        ser.write(command_LSB)
        print('Writting Data ...')
        print(command_LSB)
        time.sleep(sleep_time)
        resp_LSB = ser.read(4)
        ser.write(command_MSB)
        print('Writting Data ...')
        print(command_MSB)
        time.sleep(sleep_time)
        resp_MSB = ser.read(4)

        if resp_LSB == b'\x027\x06?':
            print('LSB Write Successful')
            lsb_ret = True
        elif resp_LSB == b'\x027\x15N':
            print('LSB Write Unsuccessful')
            lsb_ret = False
        else:
            print('Unknown Resposne')
            lsb_ret = None

        if resp_MSB == b'\x027\x06?':
            print('MSB Write Successful')
            msb_ret = True
        elif resp_MSB == b'\x027\x15N':
            print('MSB Write Unsuccessful')
            msb_ret = False
        else:
            print('Unknown Resposne')
            msb_ret = None

    return lsb_ret, msb_ret

def get_focus_value(ser):
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
    time.sleep(sleep_time)
    resp_MSB = ser.read(5).hex()
    ser.write(command_LSB)
    time.sleep(sleep_time)
    resp_LSB = ser.read(5).hex()

    hexval = '0x' + resp_MSB[4:6] + resp_LSB[4:6]
    intval = int(hexval, 0)

    return intval