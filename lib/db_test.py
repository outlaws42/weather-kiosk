#! /usr/bin/env python3

# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
from operator import itemgetter
import datetime

class Database():
    def __init__(self):
        self.db_config_wether()
        
        
    def get_resource_path(self,rel_path):
        dir_of_py_file = os.path.dirname(sys.argv[0])
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

    def printDB(self, cursor, conn, select):

        try:
            cursor = conn.cursor()
            results = cursor.execute(select)

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
        except sqlite3.OperationalError:
            print("The Table Doesn't Exist")
            
    def high_temp_today(self,cursor,conn):
        cursor = conn.cursor()
        results = cursor.execute("SELECT * from weather where TDate =  DATE('now')" )
        try:
            today = list(results)
            high_low = sorted(today, key=itemgetter(2), reverse=True)
            high = high_low[0]
        except IndexError as e:
            print(e)
            pass
        return high
        
    def create_connection(self,db_file):
         """ Make connection to an SQLite database file """
         try:
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            return conn, cur
         except sqlite3.OperationalError as e:
            print(e)

            return None

    def close(self,conn):
        """ Commit changes and close connection to the database """
        conn.commit()
        conn.close()

    def create_table(self,cursor, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            cursor.execute(create_table_sql)
            conn.commit()
            print('DB Created')
        except sqlite3.OperationalError as e:
            print(e)

    def add_column(self,cursor, table_name, new_column, column_type):
        cursor.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
            .format(tn=table_name, cn=new_column, ct=column_type))

    def show_columns(self,cursor, table_name):
        """ Retrieve column information
            Every column will be represented by a tuple """
        cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
        names = [tup[1] for tup in cursor.fetchall()]
        print(names)

    def add_row(self, cursor, *args):
        try:
            if args == 8:
                cursor.execute("INSERT INTO weather (Condition, OTemp, WindSpeed, FeelsLike, DewPoint, RelHumidity, Barometer, TDate, Zip)"
                "VALUES (?,?,?,?,?,?,?,DATE('now'),?);",(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]))
                print("added row")
            else:
                cursor.execute("INSERT INTO high (Condition, OTemp, WindSpeed, FeelsLike, DewPoint, RelHumidity, Barometer, TDate, Zip)"
                "VALUES (?,?,?,?,?,?,?,?,?);",(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8]))
                print("added row")

        except sqlite3.IntegrityError as e:
            print("test to see error" + str(e))

    def delete_table(cursor,conn,table_name):
        """ You can delete a table if it exists like this """
        cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
        conn.commit()
        
    def check_high_db_time(self):
        now = datetime.datetime.now()
        today1130pm = now.replace(hour=23, minute=30, second=0, microsecond=0)
        print(today1130pm)
        print(now)
        if now >= today1130pm:
            self.db_config_high()
        else:
            pass
        
    def db_config_high(self):
        (idr,con,tem,win,feel,dew,rel,bar,da,zi)= self.high
        create_table = """CREATE TABLE IF NOT EXISTS high(
                                                            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                            Condition TEXT NOT NULL, 
                                                            OTemp TEXT NOT NULL, 
                                                            WindSpeed INT NOT NULL, 
                                                            FeelsLike REAL, 
                                                            DewPoint REAL, 
                                                            RelHumidity REAL, 
                                                            Barometer REAL, 
                                                            TDate,
                                                            Zip TEXT
                                                    ); """
                                                    
        prin = """SELECT ID, Condition, OTemp, WindSpeed, 
                    FeelsLike, DewPoint, RelHumidity, Barometer, 
                    TDate, Zip FROM high """
        database_loc = 'weather.db'
        condition = con
        otemp = tem
        windspeed = win
        feelslike = feel
        dewpoint = dew
        relhumidity = rel
        barometer = bar
        date_today= da
        zip_code = zi
        self.write_high_db(database_loc,create_table,prin,condition,otemp, windspeed,feelslike,dewpoint,relhumidity,barometer,date_today,zip_code)
    
    def db_config_wether(self):
        create_table = """CREATE TABLE IF NOT EXISTS weather(
                                                            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                            Condition TEXT NOT NULL, 
                                                            OTemp TEXT NOT NULL, 
                                                            WindSpeed INT NOT NULL, 
                                                            FeelsLike REAL, 
                                                            DewPoint REAL, 
                                                            RelHumidity REAL, 
                                                            Barometer REAL, 
                                                            TDate,
                                                            Zip TEXT
                                                    ); """

        prin = """SELECT ID, Condition, OTemp, WindSpeed, 
                    FeelsLike, DewPoint, RelHumidity, Barometer, 
                    TDate, Zip FROM weather """
        database_loc = 'weather.db'
        condition = 'test'
        otemp = 50
        windspeed = 10
        feelslike = 20
        dewpoint = 30
        relhumidity = 45
        barometer = 28.4
        zip_code = 46764
        self.write_db(database_loc,create_table,prin,condition,otemp, windspeed,feelslike,dewpoint,relhumidity,barometer,zip_code)

    def write_db(self, *args):
        database_path = self.get_resource_path(args[0])
        print(database_path)

        # create a database connection
        conn, cur = self.create_connection(database_path)
        # create projects table
        self.create_table(cur, conn, args[1])
        #self.add_row(cur, args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10])
        self.printDB(cur, conn, args[2])
        self.high = self.high_temp_today(cur, conn)
        self.close(conn)

        
    def write_high_db(self, *args):
        database_path = self.get_resource_path(args[0])
        print(database_path)

        # create a database connection
        conn, cur = self.create_connection(database_path)
        # create projects table
        self.create_table(cur, conn, args[1])
        self.add_row(cur, args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10], args[11])
        self.printDB(cur, conn, args[2])
        self.close(conn)

if __name__ == '__main__':
    app = Database()
