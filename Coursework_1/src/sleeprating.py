##  @package docstring
#   Documentation for Sleep Rating

import csv
import numpy as np
from numpy import genfromtxt

## Read data from csv file
a = genfromtxt('data/example_data.csv', delimiter=',')

## Get sleep phase column
b = a[:,1] 

## Remove title row containing "Phase"
idealSleepData = np.delete(b,0) 

## Read data from ideal sleep data csv file
a = genfromtxt('data/nearly_ideal_data.csv', delimiter=',')

## Get sleep phase column
b = a[:,1]

## Last nights data
realSleepData = np.delete(b,0) 

## Compare the data
#CC: 573 (Exactly the same)
CC = np.correlate(idealSleepData,realSleepData) 
 
## Calculate normalized cross correlation 
# x squared
dataA = np.sum(np.square(idealSleepData)) 

## Calculate normalized cross correlation 
# y squared
dataB = np.sum(np.square(realSleepData)) 

## 1 = exactly the same, -1 completely opposite
# CC / root(x^2 y^2)
normalizedCC = CC/np.sqrt(dataA*dataB) 

## Adjust normalized value
output = normalizedCC[0]*10

##Limit to 1 decimal place
output = str(round(output,1))

## Write to txt file
f = open('data/sleeprating.txt', 'w')
f.write(output)
f.close()

print(output)
print(normalizedCC[0]*100, "%") 
