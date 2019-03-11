import socketio
import decision_tree
#ip = 'http://35.246.29.217:65080/' 
ip = 'http://146.169.173.109:65080/' 
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on('newTime')
def on_message(data):
    hour = data[hour]
    minute = data[minute]
    second = data[second]
    # call function to increase level
    

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

sio.connect(ip)
sio.wait()