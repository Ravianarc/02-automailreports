#!/usr/bin/python
import psycopg2
import os
from sqlalchemy import create_engine
from pathlib import PurePath,Path

from config import DatabaseInit


#
#
# Ravikumar , June 14,2023
#
# code referred from many sites and  implemented my own. 
#


def sql_alchemy_connection():
    conn = None
    try:
        # read connection parameters
        params = DatabaseInit().set_params().config()
        user = params["user"]
        password=params["password"]
        host = params["host"]
        database = params["database"]
        conn_string = 'postgresql://'+user+':'+password+'@'+host+'/'+ database
        #print(conn_string)
        db = create_engine(conn_string)
        conn = db.connect()
        return conn
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
           conn.close()
           print('Database connection closed.')


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = DatabaseInit().set_params().config()
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            conn.close()
        raise error






if __name__ == '__main__':
    #connection = sqlalcheconnection()
    connection = connect()
    cur = connection.cursor()
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)
    connection.close()