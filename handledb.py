#! /usr/bin/env python3

# -*- coding: utf-8 -*-

import sqlite3
import datetime

def printDB(cursor, conn):

    try:
        cursor = conn.cursor()
        results = cursor.execute("SELECT ID, Condition, OTemp, WindSpeed, FeelsLike, DewPoint, RelHumidity, Barometer, TDate FROM Weather ")

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
    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")


def create_connection(db_file):
     """ Make connection to an SQLite database file """
     try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        return conn, cur
     except Error as e:
        print(e)

        return None

def close(conn):
    """ Commit changes and close connection to the database """
    # conn.commit()
    conn.close()

def create_table(cursor, conn, create_table_sql):
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

def add_column(cursor, table_name, new_column, column_type):
    cursor.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column, ct=column_type))

def show_columns(cursor, table_name):
    """ Retrieve column information
        Every column will be represented by a tuple """
    cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    names = [tup[1] for tup in cursor.fetchall()]
    print(names)

def add_row(cursor,*args):

    try:
        cursor.execute("INSERT INTO weather (Condition, OTemp, WindSpeed, FeelsLike, DewPoint, RelHumidity, Barometer, TDate)"
        "VALUES (?,?,?,?,?,?,?,DATE('now'));",(args[0], args[1], args[2], args[3], args[4], args[5], args[6]))

    except sqlite3.IntegrityError as e:
        print("test to see error" + str(e))

def delete_table(cursor,conn,table_name):
    """ You can delete a table if it exists like this """
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    conn.commit()

def main():
    database = "weather.db"

    create_weather_table = """CREATE TABLE IF NOT EXISTS weather(
                                                    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                    Condition TEXT NOT NULL, 
                                                    OTemp TEXT NOT NULL, 
                                                    WindSpeed INT NOT NULL, 
                                                    FeelsLike REAL, 
                                                    DewPoint REAL, 
                                                    RelHumidity REAL, 
                                                    Barometer REAL, 
                                                    TDate
                                            ); """

    condition = "Clear"
    otemp = 50
    windspeed = 5
    feelslike = 50
    dewpoint = 35
    relhumidity = 25
    barometer = 29.5


    # create a database connection
    conn, cur = create_connection(database)
    print(conn)
    if conn is not None:
        # create projects table
        create_table(cur,conn, create_weather_table)
        show_columns(cur, "weather")


    else:
        print("Error! cannot create the database connection.")
    add_row(cur, condition, otemp, windspeed, feelslike, dewpoint, relhumidity, barometer)
    # add_column(cur,"weather", "Dog", "TEXT")
    show_columns(cur, "weather")
    printDB(cur,conn)

    close(conn)

if __name__ == '__main__':
    main()