# Two-Factor-Authentication-Example

Python scripts showing how to validate a using using a mysql database, hashed passwords and multifactor authentication. You must have a mysql database set up with your database credentials added to this scripts in order to execute them.

Running testMySQLConn.py will have you enter in new user information like username, email, and password. A salt is then randomly generated that is then used to hash the password. The user info is then stored in the database.

Running authenticate.py will have you enter your username and password. It will then attempt to retrieve the stored information for that user from the database. Then, it will validate the password against the hashed password that was created and stored using testMySQLConn.py. It will then inform the user if they were authenticated or not.

Running registerMFA.py will also have you enter in new user information, but it will also now create a multifactor authorization secret and generate a QR code with this secret. This is all then stored in the database. The user will then need to use a mobile multifactor authentication app to scan the QR code and add this user to the list on that app.

Running MFA.py will have you enter the username and password for the user created using register MFA.py. It will validate the entered password against the hash password that was previously stored. Next it will have you enter the current authentication app code that was set up during the registration process. If the correct code is entered, the user is then authenticated.
