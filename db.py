import sqlite3
from sqlite3 import Error, Connection as Sqlite3Conn
from collections import OrderedDict


class DatabaseConnection:
    global_connection=None
    # global_table_names=[]
    def create_tables_if_needed():
        # Using an OrderedDict because, each subsequent table definition may rely on prior ones. OrdredDict ensures that
        # Our key value pairs would be read in the order that they're inserted. We're to take care to insert each table with their
        # Dependencies added prior. This is for foreign key relations primarily
        tables_dict=OrderedDict()

        create_users_f=open('./sql/create_users.sql')
        tables_dict['users']=create_users_f.read()
        create_users_f.close()

        conn=DatabaseConnection.global_connection
        for table_name, table_query in tables_dict.items():
            # DatabaseConnection.global_table_names.append(table_name)
            cur=conn.cursor()
            cur.execute(table_query)

    def __init__(self, db_file):
        if not isinstance(DatabaseConnection.global_connection, Sqlite3Conn):
            try:
                DatabaseConnection.global_connection=sqlite3.connect(db_file)
                # Ensure that the DatabaseConnection is established first before checking for and creating tables
                DatabaseConnection.create_tables_if_needed()
                print("Database Connection intiailized with SQLite Version: {version}".format(version=sqlite3.version))
            except Error as e:
                print("Failed to initialize Database Connection")
                raise e
        else:
            print("Database Connection Object initialized")

    def get_conn(self):
        return DatabaseConnection.global_connection

"""
conn=None

def create_db_connection(db_file):
    conn=None
    if conn!=None:
        return conn
    try:
        conn = sqlite3.connect(db_file)
        return conn
        print(sqlite3.version)
    except Error as e:
        print(e)
        raise e
"""

