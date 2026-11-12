import mysql.connector
from werkzeug.security import generate_password_hash
from getpass import getpass

# Connect to your MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter your MySQL password: "),
    database="sp"
)

cursor = connection.cursor()

# Get faculty login details
username = input("Enter faculty username: ").strip()
password = getpass("Enter faculty password: ")

if not username or not password:
    print("Username and password cannot be empty.")
else:
    # Hash the faculty password
    password_hash = generate_password_hash(password)

    try:
        query = """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """
        cursor.execute(query, (username, password_hash))
        connection.commit()
        print("Faculty account created successfully!")

    except mysql.connector.IntegrityError:
        connection.rollback()
        print("That username already exists.")

cursor.close()
connection.close()