import socketio
import json
#import decision_tree

#ip = 'http://35.246.29.217:65080/' 
#ip = 'http://146.169.173.109:65080/' 
#ip = 'http://localhost:65080'
ip = 'http://localhost:65080'

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on('newTime')
def on_message(data):
    print(data)
    #data = json.loads(data['message'])
    hour = data['hour']
    minute = data['minute']
    second = data['second']
    # call function to increase level
    print(hour)
    print(minute)
    print(second)
    t = DecisionTree(hour,minute)
    level = t.analysis()
    print('predicted level: ', level.tolist())
    print(level[0])
    print(type(level[0]))
    sio.emit('newAlertLevel', level[0]-0.)

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

sio.connect(ip)
sio.wait()
#sio.sleep(1)