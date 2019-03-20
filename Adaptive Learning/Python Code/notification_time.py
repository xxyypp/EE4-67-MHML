import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime, date, time,timedelta
import pickle
import sqlite3
from sqlite3 import Error
import datetime

class NotificationTime():
    def __init__(self):
        pass
        
    def create_connection(self,db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None
    
    def get_db_Time(self,conn):
        cur = conn.cursor()
        cur.execute("SELECT ((Wake) ), Breakfast, Lunch, Dinner, Sleep From questions WHERE Name = 'Louis Kueh'")
        rows = cur.fetchall()
        return rows
    
    def get_db_daily_time_morning(self,conn):
        cur = conn.cursor()
        cur.execute("SELECT Timestamp From timeTaken WHERE Username = 'user' AND BoxNo = 1")
        rows = cur.fetchall()
        return rows

    def get_db_daily_time_afternoon(self,conn):
        cur = conn.cursor()
        cur.execute("SELECT Timestamp From timeTaken WHERE Username = 'user' AND BoxNo = 2")
        rows = cur.fetchall()
        return rows

    def get_db_daily_time_evening(self,conn):
        cur = conn.cursor()
        cur.execute("SELECT Timestamp From timeTaken WHERE Username = 'user' AND BoxNo = 3")
        rows = cur.fetchall()
        return rows
    
    def get_init(self):
        database = './storage.db'
        conn = self.create_connection(database)
        with conn:
            init_time = self.get_db_Time(conn)
        year = '19'
        month = '01'
        day = '01'
        time_zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
        
        #time = year+'/'+month+'/'+day+ ' ' + init_time[0][0]
        #init_noon = datetime.datetime.strptime(time, "%y/%m/%d %H:%M")-time_zero
        time = init_time[0][0]
        init_wake = datetime.datetime.strptime(time, "%H:%M")-time_zero
        # print(init_wake)
        #set_trace()
        
        #time = year+'/'+month+'/'+day+ ' ' + init_time[0][1]
        time = init_time[0][1]
        init_morning = datetime.datetime.strptime(time, "%H:%M")-time_zero
        # print(init_morning)

        #time = year+'/'+month+'/'+day+ ' ' + init_time[0][2]
        time = init_time[0][2]
        init_noon = datetime.datetime.strptime(time, "%H:%M")-time_zero
        # print(init_noon)

        #time = year+'/'+month+'/'+day+ ' ' + init_time[0][3]
        time = init_time[0][3]
        init_evening = datetime.datetime.strptime(time, "%H:%M")-time_zero
        # print(init_evening)

        #time = year+'/'+month+'/'+day+ ' ' + init_time[0][4]
        time = init_time[0][4]
        init_sleep = datetime.datetime.strptime(time, "%H:%M")-time_zero
        # print(init_sleep)

        init = [init_wake,init_morning,init_noon,init_evening,init_sleep]
        #print(init[1])
        return init
    
        
    
    def get_daily(self):
        database = './storage.db'
        conn = self.create_connection(database)
        with conn:
            morning = self.get_db_daily_time_morning(conn)
            
        #print('init_time  ', morning)
        actual_time = [x[0][3:24] for x in morning]
        actual_time_converted = [((a.replace('Mar','03').replace(' ','/'))[12:]) for a in actual_time]
        #print('convert morning = ', actual_time_converted)
        
        time_zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
        datetime_converted = [datetime.datetime.strptime(t, '%H:%M:%S') - time_zero for t in actual_time_converted]
        mean_morning = sum(datetime_converted, datetime.timedelta(0)) / len(datetime_converted)
        
        #print('convert morning = ',mean_morning)
        
        #--------------------------
        with conn:
            afternoon = self.get_db_daily_time_afternoon(conn)
        
        actual_time = [x[0][3:24] for x in afternoon]
        actual_time_converted = [((a.replace('Mar','03').replace(' ','/'))[12:]) for a in actual_time]
        
        datetime_converted = [datetime.datetime.strptime(t, '%H:%M:%S') - time_zero for t in actual_time_converted]
        mean_afternoon = sum(datetime_converted, datetime.timedelta(0)) / len(datetime_converted)
        
        #print('convert afternoon = ',mean_afternoon)
        
        #--------------------------
        with conn:
            evening = self.get_db_daily_time_evening(conn)
        
        actual_time = [x[0][3:24] for x in evening]
        actual_time_converted = [((a.replace('Mar','03').replace(' ','/'))[12:]) for a in actual_time]
               
        datetime_converted = [datetime.datetime.strptime(t, '%H:%M:%S') - time_zero for t in actual_time_converted]
        mean_evening = sum(datetime_converted, datetime.timedelta(0)) / len(datetime_converted)
        
        #print('convert evening = ',mean_evening)
        
        init = [mean_morning,mean_afternoon,mean_evening]
        
        return init
        
    def analysis(self):
        daily_time_avg = np.array(self.get_daily()) # get average daily pill taken time
        init_time = np.array(self.get_init()) # get initial setting time to take the medcine
        diff = abs(init_time[1]-init_time[0]) # ideal diff between wake & breakfast pill
        
        # if init wake up time >= daily_avg
        # delay the notification time
        if(init_time[0] >= daily_time_avg[0]): 
            daily_time_avg += diff
            return daily_time_avg
        return daily_time_avg