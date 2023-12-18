from msvcrt import getch
import database
from os import system as command
from platform import system as os


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
6.Delete a user
7.List of bikes
8.List of users
9.Set a user as admin
0.Log out
"""

user_menu_text = """
1.Available bikes
2.Return a bike
3.Rent a bike
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

    def __init__(self, serial_number, is_rented = 0):
        self.serial_number = serial_number
        self.is_rented = is_rented


class Electric_bike(Bike):

    def __init__(self, serial_number, is_rented = 0, is_charged = 1):
        super().__init__(serial_number, is_rented)
        self.type = "Electric"
        self.is_charged = is_charged


class Road_bike(Bike):

    def __init__(self, serial_number, is_rented = 0):
        super().__init__(serial_number, is_rented)
        self.type = "Road"


def check_username(uname):
    connection = database.connect("data.db")
    usernames = [x[2] for x in database.get_all_users(connection)]
    while uname in usernames:
        print("Username already exists!")
        uname = input("Press 'Enter' to exit or Type in a new username: ")
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
            cls()
            return None
    
    password = input("Enter your password: ")
    while password != user[3]:
        print("Username and password do not match!")
        password = input("Press 'Enter' to exit or Type in your password again: ")
        
        if not password:
            cls()
            return None
    
    cls()
    return uname


def create_account(uname):

    connection = database.connect("data.db")
    database.create_users_table(connection)

    is_admin = 0
    # The first person who creates an account becomes admin
    if not len(database.get_all_users(connection)):
        is_admin = 1

    checked_username = check_username(uname)
    if not checked_username:
        cls()
        return None
        
    password = input("Enter your password (At least 8 characters): ")
    length_checked_password = check_password_length(password)
    if not length_checked_password:
        cls()
        return None
        
    confirm_password = input("Enter your password again: ")
    confirm_password_checked = check_password_confirmation(length_checked_password, confirm_password)
    if not confirm_password_checked:
        cls()
        return None
    
    f_name = input("Enter your first name: ")
    l_name = input("Enter your last name: ")

    new_user = User(f_name, l_name, checked_username, password, is_admin)
    new_user.add_to_database()

    cls()
    return checked_username


def admin_login():
    pass


def user_login():
    pass


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

            case "2":
                print("Creating account...")
                username = input("Enter a username: ")

                logged_in_user = create_account(username)
                 
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
