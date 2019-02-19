##  @package docstring
#   Documentation for LIS3DH Accelerometer
#
#   Implements the function get the actual acceleration.
#   Initialise variables for the accelerometer.


from machine import Pin,I2C
import ustruct

## LIS3DH Accelerometer readings.
class LIS3DH:

    ## I2C
    i2c = None
    
    ## SDA PIN
    PIN_SDA = Pin(4)
    ## SCL PIN
    PIN_SCL = Pin(5)

    ## I2C ADDRESS 1
    I2C_ADDRESS_1 = 0x18
    
    ## I2C ADDRESS 2
    I2C_ADDRESS_2 = 0x19
    
    ## Default setting
    I2C_DEFAULT = I2C_ADDRESS_1

    ## Bus number
    BUS_NUMBER = 1  # -1

    ## Ranges for the accelerometer.
    # Different sensitivity.
    RANGE_2G  = 0b00  # default
    RANGE_4G  = 0b01
    RANGE_8G  = 0b10
    RANGE_16G = 0b11
    
    ## Default setting
    RANGE_DEFAULT = RANGE_2G

    ## Refresh rates for standard mode.
    OP_freq_standard_max          = 100000 
    OP_freq_standard_mid          = 50000  
    OP_freq_fast_max              = 400000 
    OP_freq_fast_mid              = 200000 
    
    ## Default setting
    OP_freq_DEFAULT = OP_freq_standard_max 
   
    ## Different data rates
    DataRate_0                    = 0b00000000
    DataRate_1                    = 0b00010000
    DataRate_10                   = 0b00100000
    DataRate_25                   = 0b00110000
    DataRate_50                   = 0b01000000
    DataRate_100                  = 0b01010000
    DataRate_200                  = 0b01100000  
    DataRate_400                  = 0b01110000
    DataRate_normal               = 0b10011000
    OP_DataRate_DEFAULT = DataRate_normal

    ## Registers
    REG_STATUS1       = 0x07
    REG_OUTADC1_L     = 0x08
    REG_OUTADC1_H     = 0x09
    REG_OUTADC2_L     = 0x0A
    REG_OUTADC2_H     = 0x0B
    REG_OUTADC3_L     = 0x0C
    REG_OUTADC3_H     = 0x0D
    REG_INTCOUNT      = 0x0E
    ## Device identification register
    REG_WHOAMI        = 0x0F  
    REG_TEMPCFG       = 0x1F
    ## Used for data rate selection, and enabling/disabling individual axis
    REG_CTRL1         = 0x20  
    REG_CTRL2         = 0x21
    REG_CTRL3         = 0x22
    ## Used for BDU, scale selection, resolution selection and self-testing
    REG_CTRL4         = 0x23  
    REG_CTRL5         = 0x24
    REG_CTRL6         = 0x25
    REG_REFERENCE     = 0x26
    REG_STATUS2       = 0x27
    REG_OUT_X_L       = 0x28
    REG_OUT_X_H       = 0x29
    REG_OUT_Y_L       = 0x2A
    REG_OUT_Y_H       = 0x2B
    REG_OUT_Z_L       = 0x2C
    REG_OUT_Z_H       = 0x2D
    REG_FIFOCTRL      = 0x2E
    REG_FIFOSRC       = 0x2F
    REG_INT1CFG       = 0x30
    REG_INT1SRC       = 0x31
    REG_INT1THS       = 0x32
    REG_INT1DUR       = 0x33
    REG_CLICKCFG      = 0x38
    REG_CLICKSRC      = 0x39
    REG_CLICKTHS      = 0x3A
    REG_TIMELIMIT     = 0x3B
    REG_TIMELATENCY   = 0x3C
    REG_TIMEWINDOW    = 0x3D

    ## Values
    DEVICE_ID  = 0x33
    ## GPIO pin for interrupt
    INT_IO     = 0x04  
    CLK_NONE   = 0x00
    CLK_SINGLE = 0x01
    CLK_DOUBLE = 0x02

    AXIS_X = 0x00
    AXIS_Y = 0x01
    AXIS_Z = 0x02

    ## Changed busnumber to 1 (from -1).
    # Alternative i2c address=0x19.
    #   @param self The object pointer
    #   @param address Address to communicate with the broad
    #   @param bus Bus number
    #   @param g_range Ranges for the accelerometer.
    #   @param OP_fr Frequency
    #   @param datarate Data rate
    def __init__(self, address=I2C_DEFAULT, bus=BUS_NUMBER,
                 g_range=RANGE_DEFAULT, OP_fr=OP_freq_DEFAULT, datarate = OP_DataRate_DEFAULT):
                 
        ## Initialise i2c, setting pin and frequency
        self.i2c = I2C(scl=Pin(5), sda=Pin(4), freq=OP_fr)
        
        ## Set connection address
        self.address = address
        
        ## Connect to device
        connectedDevices = self.i2c.scan()
        try:
            if len(connectedDevices) == 0:
                raise Exception(("At address {:x}, " +
                                 "bus {:x} datarate 0x{:x}").format(
                                     self.address, bus, datarate))

        except Exception as e:
            print("Error connecting to LIS3DH")
            print(e)

        ## Set refresh rate (default: 400Hz)
        self.setDataRate(datarate)
        self.enableAxis()
        self.setHighResolution()
        self.setBDU()
        self.setRange(g_range)

    ## Get reading from X axis
    #   @param self The object pointer
    def getX(self):
        return self.getAxis(self.AXIS_X)

    ## Get reading from Y axis
    #   @param self The object pointer
    def getY(self):
        return self.getAxis(self.AXIS_Y)

    ## Get reading from Z axis
    #   @param self The object pointer
    def getZ(self):
        return self.getAxis(self.AXIS_Z)

    ## Enable accelerometer to take axis
    #   @param self The object pointer
    def enableAxis(self):
        r1 = int.from_bytes(self.readRegister(self.REG_CTRL1), 'big')
        r1 = r1 | 7
        self.writeRegister(self.REG_CTRL1, int.to_bytes(r1, 1, 1))
   
    ##Set data rate
    #   @param self The object pointer
    #   @param dr Datarates
    def setDataRate(self, dr):
        r1 = int.from_bytes(self.readRegister(self.REG_CTRL1), 'big')
        r1 = r1 | dr
        self.writeRegister(self.REG_CTRL1, int.to_bytes(r1, 1, 1))
   

    ## Get a reading from the desired axis.
    #   @param axis X/Y/Z axis
    def getAxis(self, axis):
        ## Determine which register we need to read from (2 per axis).
        base = self.REG_OUT_X_L + (2 * axis)

        ## Read the first register (lower bits).
        low = int.from_bytes(self.readRegister(base), 'big')
        
        ## Read the next register (higher bits).
        high = int.from_bytes(self.readRegister(base + 1), 'big')
        
        ## Combine the two components.
        res = low | (high << 8)
        
        ## Calculate the twos compliment of the result.
        res = self.twosComp(res)

        ## Fetch the range we're set to, so we can
        # accurately calculate the result
        g_range = self.getRange()
        
        ## Divisor to calculate the range of g for the accelerometer.
        divisor = 1
        if g_range == self.RANGE_2G:    divisor = 16380
        elif g_range == self.RANGE_4G:  divisor = 8190
        elif g_range == self.RANGE_8G:  divisor = 4096
        elif g_range == self.RANGE_16G: divisor = 1365.33

        return float(res) / divisor


    ## Get the range that the sensor is currently set to.
    #   @param self The object pointer
    def getRange(self):
        ## Get value from register.
        val = self.readRegister(self.REG_CTRL4) 
        
        ## Read data from register.
        v = int.from_bytes(val, 'big')
        
        ## Remove lowest 4 bits.
        vv = (v >> 4)  
        
        ## Mask off two highest bits.
        v &= 0b0011  

        if v == self.RANGE_2G:   return self.RANGE_2G
        elif v == self.RANGE_4G: return self.RANGE_4G
        elif v == self.RANGE_8G: return self.RANGE_8G
        else:                      return self.RANGE_16G

    ## Set the range of the sensor (2G, 4G, 8G, 16G)
    #   @param g_range Range of g in the accelerometer.
    def setRange(self, g_range):
        if g_range < 0 or g_range > 3:
            raise Exception("Tried to set invalid range")
        
        ## Get value from register.
        val = int.from_bytes(self.readRegister(self.REG_CTRL4), 'big') 
        
        ## Mask off lowest 4 bits.
        val &= ~(0b110000) 
        
        ## Write in our new range.
        val |= (g_range << 4)  
        
        v = int.to_bytes(val, 1, 1)
        ## Write back to register.
        self.writeRegister(self.REG_CTRL4, v)  

    ## Enable or disable an individual axis.
    # Read status from CTRL_REG1, then write back with
    # appropriate status bit changed.
    #   @param self The object pointer
    #   @param axis X/Y/Z axis
    #   @param enable Boolean to set status
    def setAxisStatus(self, axis, enable):
        if axis < 0 or axis > 2:
            raise Exception("Tried to modify invalid axis")

        current = self.readRegister(self.REG_CTRL1)
        status = 1 if enable else 0
        final = self.setBit(current, axis, status)
        self.writeRegister(self.REG_CTRL1, final)

    ## Set interrupt    
    #   @param self The object pointer
    #   @param mycallback GPIO callback
    def setInterrupt(self, mycallback):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.INT_IO, GPIO.IN)
        GPIO.add_event_detect(self.INT_IO, GPIO.RISING, callback=mycallback)

    ## Set setClick    
    #   @param self The object pointer
    #   @param clickmode Mode of the click   
    #   @param clickthresh Threshold of the click
    #   @param timelimit Timing parameters
    #   @param timelatency Timing parameters
    #   @param timewindow Timing parameters
    #   @param mycallback Timing parameters
    def setClick(self, clickmode, clickthresh=80,
                 timelimit=10, timelatency=20, timewindow=100,
                 mycallback=None):
        if (clickmode == self.CLK_NONE):
            ## Get value from register.
            val = self.readRegister(self.REG_CTRL3)  
            
            ## unset bit 8 to disable interrupt.
            val &= ~(0x80)  
            
            ## Write back to register.
            self.writeRegister(self.REG_CTRL3, val)  
            
            ## disable all interrupts.
            self.writeRegister(self.REG_CLICKCFG, 0)  
            return
            
        ## Turn on int1 click. 
        self.writeRegister(self.REG_CTRL3, 0x80)  
        ## Latch interrupt on int1.
        self.writeRegister(self.REG_CTRL5, 0x08)  

        if (clickmode == self.CLK_SINGLE):
            ## Turn on all axes & singletap.
            self.writeRegister(self.REG_CLICKCFG, 0x15)
            
        if (clickmode == self.CLK_DOUBLE):
            ## Turn on all axes & doubletap.
            self.writeRegister(self.REG_CLICKCFG, 0x2A)

        ## set timing parameters
        self.writeRegister(self.REG_CLICKTHS, clickthresh)
        self.writeRegister(self.REG_TIMELIMIT, timelimit)
        self.writeRegister(self.REG_TIMELATENCY, timelatency)
        self.writeRegister(self.REG_TIMEWINDOW, timewindow)

    ## Get the click from register
    #   @param self The object pointer
    def getClick(self):
        ## read click register
        reg = self.readRegister(self.REG_CLICKSRC) 

        ## reset interrupt flag
        self.readRegister(self.REG_INT1SRC)         
        return reg

    ## Set whether we want to use high resolution or not
    #   @param self The object pointer
    #   @param highRes High Resolution
    def setHighResolution(self, highRes=True):
        ## Get current value
        val = self.readRegister(self.REG_CTRL4)  
        
        ##Accelerometer status
        status = 1 if highRes else 0

        ## High resolution is bit 4 of REG_CTRL4
        final = int.from_bytes(val, 'big') | 8
        
        f = int.to_bytes(final, 1, 1)
        self.writeRegister(self.REG_CTRL4, f)

    ## Set whether we want to use block data update or not.
    # False = output registers not updated until MSB and LSB reading
    #   @param self The object pointer
    #   @param bdu Boolean to set BDU
    def setBDU(self, bdu=True):
        ## Get current BDU value.
        val = self.readRegister(self.REG_CTRL4)  
        
        ## Status.
        status = 1 if bdu else 0

        ## Block data update is bit 8 of REG_CTRL4.
        v = int.from_bytes(val, 'big')
        
        ## Set BDU bits.
        final = self.setBit(v, 7, status)
        
        ## Value to be wrote to register to set BDU.
        val = int.to_bytes(final, 1, 1) 
        
        ## Write val to register.
        self.writeRegister(self.REG_CTRL4, val)

    ## Write the given value to the given register.
    #   @param self The object pointer
    #   @param register Written location
    #   @param value Value to be wrote to register
    def writeRegister(self, register, value):
        self.i2c.writeto_mem(self.address, register, value)

    ## Read the given value from the given register.
    #   @param self The object pointer
    #   @param register Read location  
    def readRegister(self, register):
        return self.i2c.readfrom_mem(self.address, register, 1)

    ## Set the bit at index 'bit' to 'value' on 'input' and return.
    #   @param self The object pointer
    #   @param input Input from setBDU
    #   @param bit Number of bits to shift the input
    #   @param value Status from setBDU
    def setBit(self, input, bit, value):
        mask = 1 << bit
        input &= ~mask
        if value:
            input |= mask
        return input

    ## Return a 16-bit signed number (two's compliment).
    # Thanks to http://stackoverflow.com/questions/16124059/trying-to-
    #   read-a-twos-complement-16bit-into-a-signed-decimal
    #   @param self The object pointer
    #   @param x Input to be changed to two's complement
    def twosComp(self, x):
        if (0x8000 & x):
            x = - (0x010000 - x)
        return x

    ## Debug function
    #   @param self The object pointer
    #   @param message Message to be print to debug
    def debug(self, message):
        if not self.isDebug:
            return
        print(message)
