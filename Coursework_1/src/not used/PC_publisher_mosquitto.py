import paho.mqtt.publish as publish
import time
import json
import datetime

#'''********************** MQTT Server to receive msg from client(broad) via broker ***************************'''


#''' ********************** DEFINE BEFORE USED*************************** '''
# Since we used Apollo as broker, Username, password and port number
# connected to the broker required to be set before use

''' If APOLLO Server used '''
#USERNAME = "admin"
#PWD = "password"

#Broker server address and port
HOST = "192.168.8.102"

''' If APOLLO Server used '''
#PORT = 61613 #via TCP port (apollo)
''' If MOISQUITTO Server used '''
PORT = 1883

#Subscribe topic:
TOPIC_SUB = "Server"
#Publish topic:
TOPIC_PUB = "Client"

send_msg = {
       'Phase': 12
}
#send_msg = "hello div"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPIC_SUB)

def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))

if __name__ == '__main__':
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    date_time = datetime.datetime.now()
    time = date_time.time()
    print(str(time))
    print(str(time.hour) + ":" + str(time.minute) + ":" + str(time.second))
    ''' If MOISQUITTO Server used '''
    publish.single(TOPIC_PUB, json.dumps(send_msg), qos = 1,hostname=HOST,port=PORT, client_id=client_id)
    ''' If APOLLO Server used '''
    #publish.single(TOPIC_PUB, json.dumps(send_msg), qos = 1,hostname=HOST,port=PORT, client_id=client_id,auth = {'username':"admin", 'password':"password"})