import serial
import serial.tools.list_ports
import time


sleep_time = 0.01

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
    print('Writing Data ...')
    #print(command)
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
    print('hexval is '+str(hexval))
    if len(hexval) != 4:
        print('Invalid Hex Value')
        return False
    else:
        '''
        send MSB and LSB all together
        calculate the CRC bytes by 
        '''
        STX = bytes.fromhex('02')
        CDE = bytes.fromhex('37')
        N_data = bytes.fromhex('02')
        ADD_LSB = bytes.fromhex('00')
        ADD_MSB = bytes.fromhex('01')
        Data_MSB = bytes.fromhex(hexval[0:2])
        Data_LSB = bytes.fromhex(hexval[2:4])
        #print('data_msb is' + str(Data_MSB))
        #print('data_lsb is '+str(Data_LSB))

        CRC_pre = [STX[0] + CDE[0] + ADD_LSB[0] + N_data[0] + Data_LSB[0]+Data_MSB[0]]
        CRC = bytes([CRC_pre[0] % 256])
        command = STX + CDE + ADD_LSB + N_data + Data_LSB + Data_MSB + CRC

        print('Writing data at ' + str(intval))
        ser.write(command)
        response = ser.read(4)

        if response == b'\x027\x06?':
             print('Write Successful')
             response_ret = True
        elif response == b'\x027\x15N':
             print('Write Unsuccessful')
             response_ret = False
        else:
             print('Unknown Response')
             response_ret = None

    return response_ret

def get_focus_value(ser):
    STX = bytes.fromhex('02')
    CDE = bytes.fromhex('38')
    ADD_LSB = bytes.fromhex('00')
    N_data = bytes.fromhex('02')
    CRC = bytes([STX[0] + CDE[0] + ADD_LSB[0] + N_data[0]])

    command_read = STX + CDE + ADD_LSB + N_data + CRC

    ser.write(command_read)

    response_read = ser.read(20).hex()
    print(response_read)
    print('LSB is ' + response_read[4:6])
    print('MSB is ' + response_read[6:10])
    #LSB_value = int('0x'+response_read[4:6], 0)
    #print(LSB_value)
    #MSB_value = int('0x'+response_read[6:10],0)
    #print(MSB_value)
    intval = LSB_value+MSB_value
    
    return intval