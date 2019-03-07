import time
import machine
import network
import json
import utime
from umqtt.simple import MQTTClient
    
    '''********************** MQTT Client to send msg to broker ***************************'''


class EClient:
    
    # Publish test messages e.g. with:
    # in mosquitto used: mosquitto_pub -t foo_topic -m hello
    ''' ********************** DEFINE BEFORE USED*************************** '''
    # Since we used Apollo as broker, Username, password and port number
    # connected to the broker required to be set before use
    USER = "admin"
    PWD = "password"
    port_num = 61613# 61613 is FTP port in Apollo server
    
    #Host IP ipconfig before used
    Host = "192.168.8.102"
    #WIFI SSID and password
    SSID = 'HUAWEI-B050'
    WIFIPWD = '04247095'
    
    ''' ********************** MQTT Topics *************************** '''
    # SUBSCRIBE topic
    TOPIC_S = b"Server"
    
    # Publish topic name
    TOPIC_P = b"Client" 
    
    
    def __init__(self):
        # Connecting to Wifi
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.SSID,self.WIFIPWD)
        #print(sta_if.isconnected())
    
    # Function to send sleep data to broker
    def send(self, send_msg, server="localhost",port_num):
        #define client block, including unique name of the client, server & port of the server
        #and Username and Password to connect to the server
        c = MQTTClient("CLIENT_ID", server,port,self.USER, self.PWD)
        
        #connect to broker use details above
        c.connect()
        #publish the Sleep phase with topic to the broker
        c.publish(self.TOPIC_P,json.dumps(send_msg))
        
        #once sent, disconnect
        c.disconnect()
    
    #function to be called from the previous stage to send message
    def write(self, msg):
    	#please edit server ip before setup
        self.send(msg, self.Host)