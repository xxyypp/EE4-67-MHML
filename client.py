import socketio
import sys
from os import environ

class socket_sender:
    sio = socketio.Client()
    ip = 'http://35.246.29.217:65080/' 
    
    def __init__(self):
        pass
        
    
    @sio.on('connect')
    def on_connect():
        print('connection established')
        #sio.emit(getTopic(),getMsg())

    @sio.on('new message')
    def on_message(data):
        print('message received with ', data)
        #sio.emit('my response', {'response': 'my response'})

    @sio.on('disconnect')
    def on_disconnect():
        print('disconnected from server')

    def connect_to_server(self):
        print('connect function...')
        print(self.ip)
        sio.connect(self.ip)
        sio.wait()    

    def getMsg():
        return msg

    def getTopic():
        return topic
    
    def sendMsg(self, topic, msg):
        sio = socketio.Client()
        sio.connect(self.ip)
        sio.emit(topic, msg)
        sio.sleep(1)
        sio.disconnect()
        
   