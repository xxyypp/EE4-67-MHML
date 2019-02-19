from machine import Pin,I2C
import ustruct

def getAccelBusAddr(i2cHandle):
    connectedDevices = i2cHandle.scan()
    return connectedDevices[0]

#Setup I2C handle
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

#Get the Bus Address for sensor
slaveBusAddr = getAccelBusAddr(i2c)

#Testing purposes

#Set CTRL_REG1 (0x20) to 0x9F (10011111) / 0x97 (10010111) Not low power mode
#   Activates x,y,z directions
i2c.writeto_mem(slaveBusAddr, 0x20, bytearray([0x97]))

#Set CTRL_REG4 (0x23) to 0x08 (00001000) to set to high resolution mode 12 bit data output
i2c.writeto_mem(slaveBusAddr, 0x23, bytearray([0x08]))

# Sensor Registers
#   OUT_X_L 0x28    OUT_Y_L 0x2A    OUT_Z_L 0x2C
#   OUT_X_H 0x29    OUT_Y_H 0x2B    OUT_Z_H 0x2D
X_L = 0x28
X_H = 0x29
Y_L = 0x2A
Y_H = 0x2B
Z_L = 0x2C
Z_H = 0x2D

# Divider values
#   https://github.com/adafruit/Adafruit_LIS3DH/blob/master/Adafruit_LIS3DH.cpp
TWO_G = 16380
loop = 100

# Read sensor at address
# reg: hex 
def getRegister(reg):
    return i2c.readfrom_mem(slaveBusAddr, reg)


# Read all the sensor registers and output an array containing all the values for data manipulation
# Data: [X_L, X_H, Y_L, Y_H, Z_L, Z_H]
# All values in m/s^2
def getXYZ():
    counter = 0x28 # X_L register, all the others follow
    readings = []
    for counter in range(0, 5):
        data = getRegister(counter)
        data = ustruct.unpack("@H", data)[0] #Convert to int
        data = float(data)
        readings.append(data/TWO_G) #Convert to m/s^2

    return readings



for i in range(loop):
    r = getXYZ()
    print (r)

