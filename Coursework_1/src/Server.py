##  @package docstring
#   Documentation for MQTT server.
#
#'''********************** MQTT Server to receive msg from client(broad) via broker ***************************'''

import paho.mqtt.client as mqtt
import time
import json
import csv
import datetime
import subprocess


#''' ********************** DEFINE BEFORE USED*************************** '''
# Since we used Apollo as broker, Username, password and port number
# connected to the broker required to be set before use

#USERNAME = "admin"
#PWD = "password"
#PORT = 61613

## Port = 1883 for Mosquitto
PORT = 1883

##Broker server address and port
#HOST = "127.0.0.1" #localhost IP for testing
#HOST = "192.168.8.101" Marcus without internet
#HOST = "172.20.10.2" #Div 
HOST = "172.20.10.4" # Marcus with internet
#HOST = "192.168.43.236" # Aufar internet

##''' ********************** MQTT Topics *************************** '''
# Subscribe topic:
TOPIC_SUB = "Client"

## Publish topic:
TOPIC_PUB = "Server"

## Output file name
file = 'data/actual_data.csv'

## Global variable to store message from the pillow
data = []

## Client operations
def client_loop():
    ## Client id must be unique, use time to make the client_id unique
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    ## Set client id
    client = mqtt.Client(client_id) 
    
    ## Connect to broker
    client.on_connect = on_connect 
    ## Start to received message
    client.on_message = on_message 
     
    ##60 is the maximum period in seconds allowed between communications with the broker. 
    # If no other messages are being exchanged, this controls the rate at which the client 
    # will send ping messages to the broker.
    # Maximum connection of 60 times per second
    client.connect(HOST, PORT, 60) 
    
    ## Server continues to receive the sleep information and export to csv file
    client.loop_forever() 

## Connect to broker -> Publish
    #   @param client The client pointer
    #   @param userdata Userdata
    #   @param flags  Connection flags
    #   @param rc  Connection result code
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    ## Subscribe topics from broker
    client.subscribe(TOPIC_SUB)
	#Told user conncected to broker
    #client.publish(TOPIC_PUB, json.dumps({"From server": "Server connected to broker"}))

## Receive from broker -> Subscribe.
    #   @param client The client pointer
    #   @param userdata Userdata
    #   @param msg Message received from broker
def on_message(client, userdata, msg):
    ## print message from subscribe.
    print("From " + msg.topic + " received " +": "+msg.payload.decode("utf-8"))
    
    ## Parsed json format message after decoded the message.
    json_parsed = json.loads(msg.payload.decode("utf-8"))
    ## Extract the required information: "Sleep Phase" that we get after parsed the message
    msg_phase = json_parsed['phase'] 

    ##server time as timestamp
    time = datetime.datetime.now().time().replace(microsecond=0)
    #time = datetime.datetime.now().strftime("%H:%M:%S")
    
    ##print server time in terminal
    print(time)
    
    ## Append timestamp to data
    data.append([str(time), int(msg_phase)])
    print(data)
    ## Output to csv file.
    # need newline = '', because in Python 3.6 after each row has written, /n was inserted,
    # hence need to delete the new line
    with open(file, "w", newline='') as f:
        csv_out = csv.writer(f)
        csv_out.writerows(data)
    
    subprocess.call("sh send.sh", shell=True)
	
if __name__ == '__main__':
   client_loop()
