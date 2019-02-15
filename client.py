import socketio
import sys
from os import environ

class socket_sender:
    # init
    sio = socketio.Client()
    # init server ip
    ip = 'http://35.246.29.217:65080/' 
    
    def __init__(self):
        pass
        
    # connect to server    
    @sio.on('connect')
    def on_connect():
        print('connection established')
        #sio.emit(getTopic(),getMsg())

    # client receiver
    @sio.on('new message')
    def on_message(data):
        print('message received with ', data)
        #sio.emit('my response', {'response': 'my response'})

    @sio.on('disconnect')
    def on_disconnect():
        print('disconnected from server')

    # not used...
    def connect_to_server(self):
        print('connect function...')
        print(self.ip)
        sio.connect(self.ip)
        sio.wait()    

    def getMsg():
        return msg

    def getTopic():
        return topic
    
    # function to send msg to server
    def sendMsg(self, topic, msg):
        sio = socketio.Client()
        sio.connect(self.ip)
        sio.emit(topic, msg)
        sio.sleep(1)
        sio.disconnect()
        
   