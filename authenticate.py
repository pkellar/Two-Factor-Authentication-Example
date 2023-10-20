import mysql.connector
from mysql.connector import Error
import bcrypt

# Function to validate the entered password against the stored hash
def validate_password(entered_password, stored_salt, stored_hashed_password):
    entered_password_bytes = entered_password.encode('utf-8')
    hashed_password = bcrypt.hashpw(entered_password_bytes, stored_salt.encode('utf-8'))
    return hashed_password.decode('utf-8') == stored_hashed_password

try:
    # Create a connection to the database.
    connection = mysql.connector.connect(
        host='localhost',
        user='',  # replace with your MySQL username
        password='',  # replace with your MySQL password
        database=''  # replace with your MySQL database name
    )

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        
        # Create a cursor object using the connection.
        cursor = connection.cursor()

        # Ask the user for their username and password
        username = input("Enter your username: ")
        entered_password = input("Enter your password: ")

        # Retrieve the stored hashed password and salt for the entered username
        cursor.execute("SELECT salt, password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_salt, stored_hashed_password = result

            # Validate the entered password
            if validate_password(entered_password, stored_salt, stored_hashed_password):
                print("Authentication successful. Welcome, {}!".format(username))
            else:
                print("Authentication failed. Incorrect password.")
        else:
            print("User not found. Please check the username.")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
