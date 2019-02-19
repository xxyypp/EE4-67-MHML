##  @package docstring
#   Documentation for MAX4465 Microphone
#
#   Implements the method to get reading and the convertion.


import machine
import utime
import math

## MAX4465 Microphone readings.
class MAX4465:
    ## Number of time to get the reading from MAX4465.
    tries = 30

    ## Constructor to initialise ADC to 0.
    #   @param self The object pointer
    def __init__(self):
        self.adc = machine.ADC(0)
    
    ## Returns Microphone value from 0 to 1024.
    #   @param self The object pointer
    def readValue(self):
        ## Accumulator for recording the reading
        acc = 0
        for i in range(self.tries):
            acc += self.adc.read()
            utime.sleep_us(500)
        
        ## MAX4465 Microphone reading with offset.
        # As the values are between 512 and -512, range = 1024.
        # Offeset by 512 to give 0 to 1023.
        value = acc/self.tries + 512
        
        ## Convert ADC value to actual readable data in dB
        db_value = 20*(math.log(value/1024)/math.log(10))
        ## Custom offsetting
        if (db_value < 0):
            return -(db_value - 0.005)*100
        else:
            return (db_value - 0.005)*100
