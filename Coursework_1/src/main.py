##  @package docstring
#   Documentation for the main function of the device.

from machine import Pin,I2C
import ustruct
import lis3dh
import MAX4465
import utime
import AnalyseSleep
import Client_Mosquitto

## Initialise the function to get acceleration from lis3dh accelerometer.
accel = lis3dh.LIS3DH()
## Initialise the function to get microphone reading from MAX4465 Microphone.
micr = MAX4465.MAX4465()
## Initialise the function to get current sleep phases. 
anal = AnalyseSleep.AnalyseSleep()
## Initialise the function to call MQTT publisher to send the phases to server
client = Client_Mosquitto.EClient()

## Get acceleration from lis3dh accelerometer.
#   @param num Accelerometer reading.
def get_reading(num):
    ## Initialise 2D array acc to store accelerometer reading.
    acc = [[0, 0, 0], 0]
    for i in range(num):
        ## Acceleration values are in m/s^2
        a = [accel.getX(), accel.getY(), accel.getZ()]

        ## Microphone has units of dB
        m = micr.readValue()

        ## 2 second period between getting next sample 
        utime.sleep(2)
        
        ## X-axis
        acc[0][0] += a[0] 
        ## Y-axis
        acc[0][1] += a[1]   
        ## Z-axis
        acc[0][2] += a[2] - 1   
        
        ## Microhpone has a bias, so we subtract ~500 in the driver
        if acc[1] < 0:
            # Rather than work with a negative value, add an offset 
            acc[1] += 40 
        else:
            acc[1] += m
    
    # Convert sensor reading to correct and understandable reading
    acc[1] /= num
    acc[0][0] /= num
    acc[0][1] /= num
    acc[0][2] /= num
    return acc


while 1:
    ## Gets a reading once every 10 minutes
    values = get_reading(300) 
    
    ## Get sleep phase from Analysis_Sleep Function
    phase = anal.categ_sleep(values[0], values[1])
    print("The 10 minute microphone average: ", values[1],"Accelerometer: " , values[0], "Sleep stage: ", phase['phase'], "Sleep Toggle: ", phase['sleeptoggle'], sep="\n")
    
    ## Send data to server
    client.write(phase)
    
