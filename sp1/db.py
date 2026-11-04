import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="sp",
        auth_plugin="mysql_native_password"
    )