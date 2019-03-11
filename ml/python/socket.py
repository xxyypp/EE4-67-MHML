import socketio
import json
import decision_tree

'''Edit ip address before use'''
#ip = 'http://35.246.29.217:65080/' 
#ip = 'http://146.169.173.109:65080/' 
ip = 'http://192.168.0.27:65080'

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('connection established')


'''change topic name before use'''
@sio.on('new message')
def on_message(data):
    # might need to change the first line base on different
    # enivronment, e.g. might not have 'message' before msg
    data = json.loads(data['message'])

    # Decode json:
    hour = data['hour']
    minute = data['minute']
    second = data['second']
    # call function to increase level
    t = DecisionTree(hour,minute)
    level = t.analysis()
    print('predicted level: ', level)
    
    #sio.emit('topic', level)


@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

sio.connect(ip)
sio.wait()
#sio.sleep(1)