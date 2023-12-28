from msvcrt import getch
import database
from os import system as command
from platform import system as os
from rich.console import Console
from rich.table import Table


heading_text = """
================================================================          
    ____  ______ __ ______   ____  _______   ___________    __ 
   / __ )/  _/ //_// ____/  / __ \/ ____/ | / /_  __/   |  / / 
  / __  |/ // ,<  / __/    / /_/ / __/ /  |/ / / / / /| | / /  
 / /_/ // // /| |/ /___   / _, _/ /___/ /|  / / / / ___ |/ /___
/_____/___/_/ |_/_____/  /_/ |_/_____/_/ |_/ /_/ /_/  |_/_____/
          
================================================================
                                                        
"""

sign_in_text = """
1.Sign in
2.Create account
3.Exit
          
Enter a number:"""

admin_menu_text = """
1.Available bikes
2.Rented bikes
3.Return a bike
4.Rent a bike
5.Add a bike
6.Charge a bike
7.List of bikes
8.List of users
9.Set a user as admin
0.Log out
"""

user_menu_text = """
1.Available bikes
2.Return a bike
3.Rent a bike
4.My bikes
0.Log out
"""


class User:

    def __init__(self, f_name, l_name, username, password, is_admin, rental_list = ""):
        self.f_name = f_name
        self.l_name = l_name
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.rental_list = rental_list

    def add_to_database(self):
        connection = database.connect("data.db")
        database.add_user(connection,
                          self.f_name,
                          self.l_name,
                          self.username,
                          self.password,
                          self.is_admin,
                          self.rental_list)


class Bike:

    def __init__(self, serial_number, type, is_rented = 0):
        self.serial_number = serial_number
        self.is_rented = is_rented
        self.type = type


class Electric_bike(Bike):

    def __init__(self, serial_number, type, is_rented = 0, is_charged = 1):
        super().__init__(serial_number, type, is_rented)
        self.is_charged = is_charged

    
    def add_to_database(self):
        connection = database.connect("data.db")
        database.add_bike(connection,
                          self.serial_number,
                          self.type,
                          self.is_rented,
                          self.is_charged)


class Road_bike(Bike):

    def __init__(self, serial_number, type, is_rented = 0):
        super().__init__(serial_number, type, is_rented)

    
    def add_to_database(self):
        connection = database.connect("data.db")
        database.add_bike(connection,
                          self.serial_number,
                          self.type,
                          self.is_rented,
                          None)


def check_space_existance(variable, word):
    while " " in word:
        print(f"[-] {variable} can not contain spaces!")
        word = input(f"Press 'Enter' to exit or Type in the {variable} again: ")
        if not word:
            return None
    
    return word


def check_username(uname):
    connection = database.connect("data.db")
    usernames = [x[2] for x in database.get_all_users(connection)]
    while uname in usernames:
        print("Username already exists!")
        uname = input("Press 'Enter' to exit or Type in a new username: ")
        if not uname:
            return None
        
        uname = check_space_existance("Username", uname)
        if not uname:
            return None
        
    return uname.lower()


def check_password_length(pswrd):
    while len(pswrd) < 8:
        print("Password should be at least 8 characters!")
        pswrd = input("Press 'Enter' to exit or Type in a new password: ")
        if not pswrd:
            return None
        
    return pswrd


def check_password_confirmation(pswrd, confirm_pswrd):
    while pswrd != confirm_pswrd:
        print("Passwords do not match!")
        password = input("Press 'Enter' to exit or Type in a new password: ")
        if not password:
            return None
        pswrd = check_password_length(password)
        if not pswrd:
            return None
        confirm_pswrd = input("Enter your password again: ")

    return confirm_pswrd


def cls():
    if os() == "Windows":
        command("cls")
    else:
        command("clear")
    

def sign_in(uname):
    connection = database.connect("data.db")
    user = database.get_user_by_username(connection, uname)

    # Ask for creating an account with the username if its not found
    if not user:
        print("Username not found!")
        print(f"Create an account with '{uname}'? (Y/N)")

        user_input = str(getch())[2]
        input_list = ["y", "n", "Y", "N"]
        while user_input not in input_list:
            print("[-] You can only enter 'Y' or 'N'")
            user_input = str(getch())[2]

        if user_input == "y":
            cls()
            print(f"Creating account with username: {uname}")
            return create_account(uname)
        else:
            return None
    
    password = input("Enter your password: ")
    while password != user[3]:
        print("Username and password do not match!")
        password = input("Press 'Enter' to exit or Type in your password again: ")
        
        if not password:
            return None
    
    return uname


def create_account(uname):

    connection = database.connect("data.db")
    database.create_users_table(connection)

    is_admin = 0
    # The first person who creates an account becomes admin
    if not len(database.get_all_users(connection)):
        is_admin = 1

    space_checked_username = check_space_existance("Username", uname)
    if not space_checked_username:
        return None

    checked_username = check_username(space_checked_username)
    if not checked_username:
        return None
        
    password = input("Enter your password (At least 8 characters): ")
    length_checked_password = check_password_length(password)
    if not length_checked_password:
        return None
        
    confirm_password = input("Enter your password again: ")
    confirm_password_checked = check_password_confirmation(length_checked_password, confirm_password)
    if not confirm_password_checked:
        return None
    
    f_name = input("Enter your first name: ")
    l_name = input("Enter your last name: ")

    new_user = User(f_name, l_name, checked_username, password, is_admin)
    new_user.add_to_database()

    return checked_username


def check_serial_number_exists(serial_num):
    connection = database.connect("data.db")
    serial_numbers = [x[0] for x in database.get_all_bikes(connection)]

    while serial_num in serial_numbers:
        print("[-] Serial number already exists!")
        serial_num = input("Press 'Enter' to exit or Type in a new serial number: ")
        if not serial_num:
            return None
        
        serial_num = check_space_existance("Serial Number", serial_num)
        if not serial_num:
            return None
    
    return serial_num


def add_bike():
    print("Adding a bike...")
    connection = database.connect("data.db")
    database.create_bikes_table(connection)

    serial_number = input("Enter the serial number: ")
    space_checked_serial_number = check_space_existance("Username", serial_number)
    if not space_checked_serial_number:
        return None

    full_checked_serial_number = check_serial_number_exists(space_checked_serial_number)
    if not full_checked_serial_number:
        return None
    
    input_list = ["r", "e"]
    print("What's the type of the bike?\nEnter 'R' for 'Road' or 'E' for 'Electric': ")
    type = (str(getch())[2]).lower()
    while type not in input_list:
        print("[-] Invalid input!")
        print("Enter 'R' for 'Road' or 'E' for 'Electric' or Press 'Enter' to exit: ")
        user_input = (str(getch())).lower()
        if user_input[2:4] == "\\r":
            return None
        type = user_input[2]

    match type:
        case "r":
            bike = Road_bike(full_checked_serial_number, "Road")
            bike.add_to_database()

        case "e":
            bike = Electric_bike(full_checked_serial_number, "Electric")
            bike.add_to_database()

    print("[+] Bike added successfully!")
    input("Press 'Enter' to exit")


def print_table(title, columns, rows):
    table = Table(title=title)

    for column in columns:
        table.add_column(column)

    # Converting all the values of the rows to string so they are renderable by the table
    str_rows = [[str(value) for value in row] for row in rows]

    for row in str_rows:
        table.add_row(*row, style="bright_green")

    console = Console()
    console.print(table)


def get_all_users():
    connection = database.connect("data.db")
    users = database.get_all_users(connection)

    columns = ["First name", "Last name", "Username", "Password", "Admin", "Rental list"]

    print_table("Users", columns, users)

    input("\n\nPress 'Enter' to exit")


def get_all_bikes(availables_only = False, rented_only = False):
    connection = database.connect("data.db")

    columns = ["Serial number", "Type", "Rented", "Charged"]

    if availables_only:
        bikes = database.get_bikes_by_rented(connection, 0)
        for bike in bikes:
            if bike[3] == 0:
                bikes.remove(bike)

        table_title = "Available bikes"

    elif rented_only:
        columns.append("Rented by")

        tuple_bikes = database.get_bikes_by_rented(connection, 1)
        users = database.get_all_users(connection)
        bikes = []
        for bike in tuple_bikes:
            bikes.append(list(bike))

        for bike in bikes:
            for user in users:
                if bike[0] in user[5].split(" "):
                    bike.append(user[2])
                    break

        table_title = "Rented bikes"

    else:
        bikes = database.get_all_bikes(connection)
        table_title = "All bikes"

    print_table(table_title, columns, bikes)

    input("\n\nPress 'Enter' to exit")


def set_admin():
    print("Setting a user as admin...")

    connection = database.connect("data.db")
    usernames = [user[2] for user in database.get_all_users(connection)]

    username = input("Enter the username of the user: ")
    while username not in usernames:
        print("[-] User not found!")
        username = input("Press 'Enter' to exit or Type in the username again: ")
        if not username:
            return None
    
    print(f"Setting username '{username}' as admin...")
    confirmation = input("Type 'CONFIRM' to continue: ")
    while confirmation != "CONFIRM":
        print("[-] Confirmation failed!")
        confirmation = input("Press 'Enter' to exit or Type 'CONFIRM' to continue: ")
        if not confirmation:
            return None

    database.set_as_admin(connection, username)


def check_serial_number_not_exists(serial_num):
    connection = database.connect("data.db")
    serial_numbers = [x[0] for x in database.get_all_bikes(connection)]

    while serial_num not in serial_numbers:
        print("[-] Bike not found!")
        serial_num = input("Press 'Enter' to exit or Type in the serial number again: ")
        if not serial_num:
            return None

    return serial_num


def check_bike_availablity(serial_num):
    connection = database.connect("data.db")
    bike = database.get_bike_by_serial_number(connection, serial_num)

    if bike[2]:
        print("[-] This bike is not available!")
        input("\nPress 'Enter' to exit")
        return False
    
    if bike[3] == 0:
        print("[-] This bike has ran out of charge!")
        input("Press 'Enter' to exit")
        return False
    
    return True


def rent_bike(uname):
    print("Renting a bike...")
    connection = database.connect("data.db")
    user = database.get_user_by_username(connection, uname)

    rental_list = user[5].split(" ")
    if len(rental_list) == 3:
        print("[-] Renting limit reached!\nReturn a bike before renting another one")
        input("\nPress 'Enter' to exit")
        return None

    serial_number = input("Enter the serial number of the bike: ")
    checked_serial_number = check_serial_number_not_exists(serial_number)
    if not checked_serial_number:
        return None
    
    if check_bike_availablity(checked_serial_number):
        rental_list.append(checked_serial_number)
        rental_str = " ".join(rental_list).strip()
    
        database.add_to_rented(connection, rental_str, uname)
        database.set_rented(connection, 1, checked_serial_number)
    
        print("[+] Bike was successfully rented!")
        input("\nPress 'Enter' to exit")


def return_bike(username):
    print("Returning a bike...")
    connection = database.connect("data.db")
    rental_list = database.get_user_by_username(connection, username)[5].split(" ")

    serial_number = input("Enter the serial number of the bike: ")
    while serial_number not in rental_list:
        print("[-] You do not have this bike!")
        serial_number = input("Press 'Enter' to exit or Type in the serial number again: ")
        if not serial_number:
            return None
        
    rental_list.remove(serial_number)
    rental_str = " ".join(rental_list)

    database.add_to_rented(connection, rental_str, username)
    database.set_rented(connection, 0, serial_number)
    
    bike = database.get_bike_by_serial_number(connection, serial_number)
    if bike[3]:
        database.set_charge(connection, 0, serial_number)

    print("[+] Bike was successfully returned!")
    input("\nPress 'Enter' to exit")


def charge_bike():
    print("Charging a bike...")

    serial_number = input("Enter the serial number of the bike: ")
    checked_serial_number = check_serial_number_not_exists(serial_number)

    connection = database.connect("data.db")
    bike = database.get_bike_by_serial_number(connection, checked_serial_number)

    if bike[3]:
        print("[-] This bike is already charged!")
    
    elif bike[3] == 0:
        database.set_charge(connection, 1, checked_serial_number)
        print("[+] Bike was successfully charged!")

    else:
        print("[-] This bike is not electric!")

    input("\nPress 'Enter' to exit")


def admin_login(uname):
    while True:
        connection = database.connect("data.db")
        user = database.get_user_by_username(connection, uname)

        print(f"Welcome {user[0]} {user[1]}!   ### Admin ###")

        print(admin_menu_text)

        input_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        user_input = str(getch())[2]
        while user_input not in input_list:
            print("[-] Invalid input!")
            user_input = str(getch())[2]

        cls()
        match user_input:
            case "1":
                get_all_bikes(availables_only=True)

            case "2":
                get_all_bikes(rented_only=True)

            case "3":
                return_bike(uname)

            case "4":
                rent_bike(uname)

            case "5":
                add_bike()

            case "6":
                charge_bike()
            
            case "7":
                get_all_bikes()

            case "8":
                get_all_users()

            case "9":
                set_admin()

            case "0":
                cls()
                return None
            
        cls()


def my_bikes(username):
    try:
        connection = database.connect("data.db")
        bikes = database.get_user_by_username(connection, username)[5].split(" ")

        bike_rows = []
        for bike in bikes:
            row = database.get_bike_by_serial_number(connection, bike)
            bike_rows.append(row)

        columns = ["Serial number", "Type", "Rented", "Charged"]

        print_table("My bikes", columns, bike_rows)

    except:
        print("[-] You have no bikes!")

    finally:
        input("\nPress 'Enter' to exit")


def user_login(uname):
    while True:
        connection = database.connect("data.db")
        user = database.get_user_by_username(connection, uname)
            
        print(f"Welcome {user[0]} {user[1]}!")
    
        print(user_menu_text)
    
        input_list = ["1", "2", "3", "4", "0"]
        user_input = str(getch())[2]
        while user_input not in input_list:
            print("[-] Invalid input!")
            user_input = str(getch())[2]

        cls()
        match user_input:
            case "1":
                get_all_bikes(availables_only=True)

            case "2":
                return_bike(uname)

            case "3":
                rent_bike(uname)
            
            case "4":
                my_bikes(uname)

            case "0":
                cls()
                return None
        
        cls()


def main():

    while True:

        print(heading_text)

        print(sign_in_text)
    
        input_list = ["1", "2", "3"]
        while (user_input := str(getch())[2]) not in input_list:
            print("[-] You can only select 1, 2 or 3")
            user_input = str(getch())[2]

        cls()
        match user_input:

            case "1":
                print("Signing in...")
                username = input("Enter your username: ")

                logged_in_user = sign_in(username.lower())
                cls()

            case "2":
                print("Creating account...")
                username = input("Enter a username: ")

                logged_in_user = create_account(username)
                cls()
                 
            case "3":
                return 0
            
        if logged_in_user:
            connection = database.connect("data.db")
            user = database.get_user_by_username(connection, logged_in_user)
            
            if user[4]:
                logged_in_user = admin_login(logged_in_user)
            else:
                logged_in_user = user_login(logged_in_user)


if __name__ == "__main__":
    main()
