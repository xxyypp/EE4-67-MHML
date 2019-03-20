import json
import decision_tree
import socketio
import notification_time

'''Edit ip address before use'''
#ip = 'http://35.246.29.217:65080/' 
#ip = 'http://146.169.173.109:65080/' 
#ip = 'http://192.168.0.27:65080'
ip = 'http://localhost:65080'

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('connection established')


'''change topic name before use'''
# for generating the new alert level
@sio.on('newAlert')
def on_message(data):
    print(data)
    hour = data['hour']
    minute = data['minute']
    second = data['second']
    # call function to increase level
    t = DecisionTree(hour,minute)
    level = t.analysis()
    sio.emit('newAlertLevel', level[0])

'''change topic name before use'''
# for estimating the new notification time
@sio.on('newTime')
def on_message(data):
    # call function to generate new time
    t = NotificationTime()
    update_time = t.analysis()
    print(update_time[0])
    print(update_time[1])
    print(update_time[2])
    sio.emit('newAlertTime', update_time)

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

sio.connect(ip)
sio.wait()