import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
from datetime import datetime, date, time,timedelta
import pickle
import sqlite3
from sqlite3 import Error
import datetime

class DecisionTree():
    def __init__(self, hour,minute):
        self.hour = hour
        self.minute = minute
        
    def create_connection(self,db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None
    
    def get_db_Time(self,conn):
        cur = conn.cursor()
        cur.execute("SELECT Wake, Breakfast, Lunch, Dinner, Sleep From questions WHERE Name = 'Louis Kueh'")
        rows = cur.fetchall()
        return rows

    def get_db_daily_time(self,conn):
        cur = conn.cursor()
        cur.execute("SELECT Timestamp From timeTaken")
        rows = cur.fetchall()
        return rows
    
    def get_init(self):
        database = './storage.db'
        conn = create_connection(database)
        with conn:
            init_time = get_db_Time(conn)
        year = '19'
        month = '01'
        day = '01'
        time = year+'/'+month+'/'+day+ ' ' + init_time[0][0]
        init_wake = datetime.datetime.strptime(time, "%y/%m/%d %H:%M")
        # print(init_wake)

        time = year+'/'+month+'/'+day+ ' ' + init_time[0][1]
        init_morning = datetime.datetime.strptime(time, "%y/%m/%d %H:%M")
        # print(init_morning)

        time = year+'/'+month+'/'+day+ ' ' + init_time[0][2]
        init_noon = datetime.datetime.strptime(time, "%y/%m/%d %H:%M")
        # print(init_noon)

        time = year+'/'+month+'/'+day+ ' ' + init_time[0][3]
        init_evening = datetime.datetime.strptime(time, "%y/%m/%d %H:%M")
        # print(init_evening)

        time = year+'/'+month+'/'+day+ ' ' + init_time[0][4]
        init_sleep = datetime.datetime.strptime(time, "%y/%m/%d %H:%M")
        # print(init_sleep)

        init = [init_wake,init_morning,init_noon,init_evening,init_sleep]
        return init
    
    def analysis(self):
        year = '19'
        month = '01'
        day = '01'
        time = year+'/'+month+'/'+day+ ' ' + self.hour + ':' + self.minute
        test_time = datetime.datetime.strptime(time, "%y/%m/%d %H:%M")
        
        init_time = self.get_init() #get initial setting time to take the medcine
        diff = test_time-init_time[1] # find difference between actual and pre-set
        x_in = np.array([(diff.total_seconds()/60)]) # convert to minutes
        
        # Load model for testing
        filename = 'notification_model.sav'
        model = pickle.load(open(filename, 'rb'))
        y_predict = model.predict(x_in.reshape(-1,1))
        
        return y_predict # notification level