#! /usr/bin/env python3

# -*- coding: utf-8 -*-

import sqlite3
import os
import sys


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

printDB()

with open(get_resource_path('dump.sql'), 'w') as f:
    # iterdump() returns an iterator to dump the database
    # in SQL format
    for line in db_conn.iterdump():
        f.write('%s\n' % line)

# Closes the database connection
db_conn.close()

