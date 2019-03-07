"""
Output the sleep cycle data into a file
"""

from machine import Pin,I2C
import ustruct
######## Global variables ##########
retries = 5 		# Number of attempts to write - useful for higher frequencies
debug = 5			# Debug level
frequency = 100000 	# Frequency of port
time_period = 10*60 # Time period to average over: seconds
poll_time = 30		# How often to pull the data: seconds

######## Establish Connection ##########
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=frequency)

i2c.writeto(24, bytearray([0xf3]))

data=i2c.readfrom(24,2)

int.from_bytes(data,'big')



######## Settings #########
i2c.writeto_mem(0x18, 0x20, 0x9f)

i2c.writeto_mem(0x18, 0x20, bytearray([0x9f]))



# Writes with attempts to retry --> otherwise returns an IO error
def write_block(address, block):
	for i in range(retries):
		try:
			return i2c.writeto_mem(0x18, address, block)
		except IOError:
			if (debug > 2)
				print ("IOError")
	return -1

def read_block(num_bytes):
	for i in range(retries):
		try:
			return i2c.readfrom(0x18, num_bytes)
		except IOError:
			if (debug > 2)
				print("IOError")
	return -1


# Outputs the data in real time using MQTT
def buf_out ():
    	

# Outputs an average over the defined time period
def average_data():




def byte_convert(in_byte):
    return ustruct.unpack("<h", in_byte)) 
