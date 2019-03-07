from machine import Pin,I2C
import ustruct
import lis3dh

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

#Get the Bus Address for sensor
connectedDevices = i2c.scan()
slaveBusAddr = connectedDevices[0]

#Testing purposes
Loop_cycles = 100

#Set CTRL_REG1 (0x20) to 0x9F (10011111)
#   Activates x,y,z directions
i2c.writeto_mem(slaveBusAddr, 0x20, bytearray([0x9F]))

# Sensor Registers
#   OUT_X_L 0x28    OUT_Y_L 0x2A    OUT_Z_L 0x2C
#   OUT_X_H 0x29    OUT_Y_H 0x2B    OUT_Z_H 0x2D
X_L = 0x28
X_H = 0x29
Y_L = 0x2A
Y_H = 0x2B
Z_L = 0x2C
Z_H = 0x2D

accel = LIS3DH()

def byte_convert(in_byte):
    data = ustruct.unpack("<h", in_byte)[0]
    return data


while Loop_cycles >= 0:
'''    data = i2c.readfrom_mem(slaveBusAddr,Y_H,2)
    #out = int.from_bytes(data, 'big')
    d = ustruct.unpack("@h", data)'''
    
    d = accel.getX()
    print(d)
    Loop_cycles-=1



"""

{
"data":[
    {"Time":"John", "lastName":"Doe"}, 
    {"Phase":"Anna", "lastName":"Smith"},
    {"firstName":"Peter", "lastName":"Jones"}
]
}




"""
