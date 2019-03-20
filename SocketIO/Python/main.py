import socketio
import sys
import client
from os import environ
'''
1. Initialise the socket object
    msg_sender = client.socket_sender()
2. Set topic, current server only receives:
    topic = 'new message'
3. sendMsg
    msg_sender.sendMsg(topic, 'Hello, start')
'''
msg_sender = client.socket_sender()
topic = 'new message'
msg_sender.sendMsg(topic, 'Hello, start')
for i in range(5):
    msg_to_send = 'Hello, jupyter ' + str(i)
    msg_sender.sendMsg(topic, msg_to_send)
