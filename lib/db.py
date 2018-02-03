#! /usr/bin/env python3

# -*- coding: utf-8 -*-

import sqlite3
from operator import itemgetter

class Database():
    def __init__(self):
        pass

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

    def high_low_temp_today(self,cursor,conn):
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


    def past_temp(self,cursor,conn,table ):
        cursor = conn.cursor()

        try:
            results = cursor.execute(
            "SELECT * from {tb} where TDate =  DATE('now', 'localtime', '-1 day')".format(tb=table) )
            past = list(results)
            if past:
                high_low = past[0]
                return high_low
        except IndexError as e:
            print(e)
            pass

    def create_connection(self,db_file):
         """ Make connection to an SQLite database file """
         try:
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            return conn, cur
         except Error as e:
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

    def add_row(self, cursor, tablename, *args):
        try:
            if len(args) == 8:
                cursor.execute("INSERT INTO " + tablename + 
                " (Condition, OTemp, WindSpeed, FeelsLike, DewPoint, RelHumidity, Barometer, TDate, Zip)"
                "VALUES (?,?,?,?,?,?,?,DATE('now', 'localtime'),?);",
                (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]))
            else:
                cursor.execute("INSERT INTO " + tablename + 
                " (Condition, OTemp, WindSpeed, FeelsLike, DewPoint, RelHumidity, Barometer, TDate, Zip)"
                "VALUES (?,?,?,?,?,?,?,?,?);",
                (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8]))
        except sqlite3.OperationalError as e:
            print(e)
                
    def delete_table(cursor,conn,table_name):
        """ You can delete a table if it exists like this """
        cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
        conn.commit()


if __name__ == '__main__':
    app = Database()
