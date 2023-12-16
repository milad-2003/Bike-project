import sqlite3


def connect(database_name):
    return sqlite3.connect(database_name)
    
