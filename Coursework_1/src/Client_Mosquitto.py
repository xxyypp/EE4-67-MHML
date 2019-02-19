##  @package docstring
#   Documentation for Client(the Smart Pillow) to send information via MQTT 
#
#   Implements the MQTT using UMQTT for micropython

import time
import machine
import network
import json
import utime
from umqtt.simple import MQTTClient

## MQTT Publisher Class

class EClient:
    ''' ********************** Client for Mosquitto ***************************     '''
    # Publish test messages e.g. with:
    # mosquitto_pub -t foo_topic -m hello
    #''' ********************** DEFINE BEFORE USED***************************     '''
    
    ## Server username.
    USER = "admin"
    ## Server password.
    PWD = "password"
    ## Host IP 
    #Host = "172.20.10.2" #Div internet
    #Marcus without internet: Host = "192.168.8.102"
    Host = "172.20.10.4" # Marcus internet
    #Host = "192.168.43.236" # Aufar internet

    ## WIFI username and password
    #SSID = 'HUAWEI-B050'
    #SSID = 'Div_phone' # Div phone
    SSID = '12233' # Marcus phone
    #SSID = 'blazingasian' # Aufar phone

    ## WIFI password
    #WIFIPWD = 'Aewie9dgG' # Div password
    WIFIPWD = 'qwertyuiop' # Marcus password
    #WIFIPWD = 'getshreddedbrah' #Aufar password

    ## SUBSCRIBE topic
    TOPIC_S = b"Server"
    
    ## Publish topic
    TOPIC_P = b"Client" 
    
    ## Constructor to connect to Wifi
    def __init__(self):
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        #sta_if.connect('12233', 'qwertyuiop')
        sta_if.connect(self.SSID,self.WIFIPWD)
        #print(sta_if.isconnected())
        self.Sleep_toggle = 0
    
    
    
    ## Received messages from subscriptions will be delivered to this callback. 
    # Put message, local host(since server is local), port number to communicate with broker. 
    #   @param self The object pointer
    #   @param send_msg message to be sent to broker
    #   @param server  Server is local host
    #   @param port  Port = 1883 for Mosquitto
    def send(self, send_msg, server="localhost",port = 1883):
    
        ## Initialise mqtt client.
        c = MQTTClient("CLIENT_ID", server,port,self.USER, self.PWD)
        ## Connect to broker.
        c.connect()
        ## Publish data using json format(json.dumps)
        c.publish(self.TOPIC_P,json.dumps(send_msg))
        
        ## Disconnect after publish to broker
        c.disconnect()
    
    ## Check whether the device need to send the message or not.
    #   @param self The object pointer
    #   @param msg message to be sent to broker
    def write(self, msg):
        if (msg['sleeptoggle'] == 1):
            if (self.Sleep_toggle == 0):
                self.Sleep_toggle = 1
            else:
                self.Sleep_toggle = 0
        #please edit server ip before setup
        if (self.Sleep_toggle == 1):
            self.send(msg, self.Host)

# t = EClient()
# data = {
#            'Phase': 100
#     }     
# t.write(data)         
