import mysql.connector
from mysql.connector import Error
import bcrypt
import pyotp
import qrcode

# Function to generate a random salt
def generate_salt():
    return bcrypt.gensalt()

# Function to hash a password with a given salt
def hash_password(password, salt):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to generate an MFA secret key
def generate_mfa_secret():
    return pyotp.random_base32()
    
# Function to generate a QR code containing the secret key
def generate_qr_code(secret_key, username):
    totp_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(username, issuer_name="YourApp")
    img = qrcode.make(totp_uri)
    img.save(f"{username}_qr.png")

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
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        # Function to get user input
        def get_user_input():
            username = input("Enter your username: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            return username, email, password

        # Get user input
        username, email, password = get_user_input()

        # Generate a salt
        salt = generate_salt()

        # Hash the password with the salt
        hashed_password = hash_password(password, salt)

        # Generate an MFA secret key
        mfa_secret = generate_mfa_secret()

        # Generate a QR code with the secret key
        generate_qr_code(mfa_secret, username)

        # Insert user information into the database
        insert_query = "INSERT INTO users (username, salt, password, email, totp_secret) VALUES (%s, %s, %s, %s, %s)"
        user_data = (username, salt.decode('utf-8'), hashed_password, email, mfa_secret)
        cursor.execute(insert_query, user_data)
        connection.commit()

        print("User registration successful.")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

