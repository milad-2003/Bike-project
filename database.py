import sqlite3


queries = {
    "create_users_table_query": """CREATE TABLE IF NOT EXISTS users (
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        password TEXT,
        is_admin INTEGER,
        rental_list TEXT
    );""",

    "create_bikes_table_query": """CREATE TABLE IF NOT EXISTS bikes (
        serial_number TEXT,
        type TEXT,
        is_rented INTEGER,
        is_charged INTERGER
    );""",

    "get_all_users_query": "SELECT * FROM users;",

    "add_user_query": "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);",

    "get_user_by_username_query": "SELECT * FROM users WHERE username = ?;",

    "add_bike_query": "INSERT INTO bikes VALUES (?, ?, ?, ?);",

    "get_all_bikes_query": "SELECT * FROM bikes;",

    "available_bikes_query": "SELECT * FROM bikes WHERE is_rented = 0;",

    "set_as_admin_query": "UPDATE users SET is_admin = 1 WHERE username = ?;"
}


def connect(database_name):
    return sqlite3.connect(database_name)
    

def create_users_table(connection):
    with connection:
        connection.execute(queries["create_users_table_query"])


def create_bikes_table(connection):
    with connection:
        connection.execute(queries["create_bikes_table_query"])


def get_all_users(connection):
    with connection:
        return connection.execute(queries["get_all_users_query"]).fetchall()


def add_user(connection, first_name, last_name, username, password, is_admin, rental_list):
    with connection:
        connection.execute(queries["add_user_query"],
                           (first_name, last_name, username, password, is_admin, rental_list))


def get_user_by_username(connection, username):
    with connection:
        return connection.execute(queries["get_user_by_username_query"], (username, )).fetchone()


def add_bike(connection, serial_number, type, is_rented, is_charged):
    with connection:
        connection.execute(queries["add_bike_query"],
                           (serial_number, type, is_rented, is_charged))


def get_all_bikes(connection):
    with connection:
        return connection.execute(queries["get_all_bikes_query"]).fetchall()


def available_bikes(connection):
    with connection:
        return connection.execute(queries["available_bikes_query"]).fetchall()


def set_as_admin(connection, username):
    with connection:
        connection.execute(queries["set_as_admin_query"], (username, ))
