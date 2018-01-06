#! /usr/bin/env python3

# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
from operator import itemgetter


def printDB():
    try:
        results = theCursor.execute(
            "SELECT ID, Condition, OTemp, WindSpeed, FeelsLike, DewPoint, RelHumidity, Barometer, TDate, Zip FROM high ")

        for row in results:
            print("ID :", row[0])
            print("Condition :", row[1])
            print("Outdoor Temp :", row[2])
            print("Wind Speed :", row[3])
            print("Feels Like :", row[4])
            print("Dew Point :", row[5])
            print("Rel. Humidity :", row[6])
            print("Barometer :", row[7])
            print("Date :", row[8])
            print("Zip :", row[9])
            print(" ")
    except sqlite3.OperationalError as e:
        print("The Table Doesn't Exist: " + str(e))
        pass
def high_low_temp_today(cursor,conn):
        cursor = conn.cursor()
        results = cursor.execute("SELECT * from weather where TDate =  DATE('now', 'localtime')" )
        try:
            today = list(results)
            high_low = sorted(today, key=itemgetter(2), reverse=True)
            low_high = sorted(today, key=itemgetter(2))
            high = high_low[0]
            low = low_high[0]
            return high, low
        except IndexError as e:
            print(e)
            pass
                    
def high_temp(cursor,conn):
    cursor = conn.cursor()
    
    try:
        results = cursor.execute("SELECT * from high where TDate =  DATE('now', 'localtime', '-1 day')" )
        today = list(results)
        #high_low = sorted(today, key=itemgetter(2), reverse=True)
        high = today[0]
        #print(today)
        return high
    except IndexError as e:
        print(e)
        pass
    
def high_temp(cursor,conn):
        cursor = conn.cursor()
    
        try:
            results = cursor.execute("SELECT * from high where TDate =  DATE('now', 'localtime', '-1 day')" )
            today = list(results)
            high = today[0]
            return high
        except IndexError as e:
            print(e)
            pass
            
def low_temp(cursor,conn):
        cursor = conn.cursor()
    
        try:
            results = cursor.execute("SELECT * from low where TDate =  DATE('now', 'localtime', '-1 day')" )
            today = list(results)
            low = today[0]
            return low
        except IndexError as e:
            print(e)
            pass
            
def get_resource_path(rel_path):
        dir_of_py_file = os.path.dirname(sys.argv[0])
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

def delete_table(cursor,conn,table_name):
        """ You can delete a table if it exists like this """
        cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
        conn.commit()

db_conn = sqlite3.connect(get_resource_path('weather.db'))
print(get_resource_path('weather.db'))

print("Database Created")

theCursor = db_conn.cursor()
# delete_table(theCursor,db_conn,"high")
high_tp = high_temp(theCursor,db_conn)
low_tp = low_temp(theCursor,db_conn)
low_high = high_low_temp_today(theCursor,db_conn)
#lowt = low_high[1]
#hight= low_high[0]
#print(lowt)
#print(hight)
#high_ = high_tp[0]
#low_ = high_tp[0]
#print(high_)
#print(low_)
print(high_tp)
print(low_tp)

#printDB()

with open(get_resource_path('dump.sql'), 'w') as f:
    # iterdump() returns an iterator to dump the database
    # in SQL format
    for line in db_conn.iterdump():
        f.write('%s\n' % line)

# Closes the database connection
db_conn.close()

