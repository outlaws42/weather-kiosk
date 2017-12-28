#! /usr/bin/env python3

# -*- coding: utf-8 -*-

import sqlite3

class Database():
    def __init__(self):
        pass

    def printDB(self, cursor, conn):

        try:
            cursor = conn.cursor()
            results = cursor.execute("SELECT ID, Condition, OTemp, WindSpeed, FeelsLike, DewPoint, RelHumidity, Barometer, TDate, Zip FROM Weather ")

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
        except sqlite3.OperationalError:
            print("The Table Doesn't Exist")


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
            cursor.execute("INSERT INTO weather (Condition, OTemp, WindSpeed, FeelsLike, DewPoint, RelHumidity, Barometer, TDate, Zip)"
            "VALUES (?,?,?,?,?,?,?,DATE('now'),?);",(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]))
            print("added row")

        except sqlite3.IntegrityError as e:
            print("test to see error" + str(e))

    def delete_table(cursor,conn,table_name):
        """ You can delete a table if it exists like this """
        cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
        conn.commit()


if __name__ == '__main__':
    app = Database()
