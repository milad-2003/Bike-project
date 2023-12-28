# Bike Rental

This is the final project of the "Special topics" lesson in the university.\
There are 2 types of users in this program with different capablities:
1. Regular users
2. Admin users

## Regular users

Regular users are able to:
1. See a table of available bikes
2. Return a bike of their own
3. Rent a bike for themselves
4. See a table of their own bikes

## Admin users

Admins are able to:
1. See a table of available bikes
2. See a table of rented bikes
3. Return a bike of their own
4. Rent a bike for themselves
5. Add a bike to the table of bikes
6. Charge an electric bike
7. See a table of all the bikes
8. See a table of all the users
9. Set a user as admin
10. See a table of their own bikes

## Rules

1. Usernames can not contain "Space"
2. Passwords must be at least 8 characters
3. Serial number of the bikes can not contain "Space"
4. No user is allowed to rent more than 3 bikes

## Modules

### 1. sqlite3

This is used to create the database using SQLite and interact with it.

### 2. getch from msvcrt

This function is used to get input from the user without the need for pressing "Enter"

### 3. console & table from rich

This module is used to print tables in the terminal

### 4. system from os

This function is used to run commands in the terminal.\
In this project, I used it to clear the terminal screen at some points.

### 5. system from platform

This function is used to get the operating system of the user.\
To clear the terminal in windows, we use the command "cls". However, in Linux and MAC we use "clear".\
Though, we need to get the os of the user to know which of these commands should we run in terminal, using the previously explained function.
