from msvcrt import getch
import database


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


class User:

    def __init__(self, f_name, l_name, username, password, is_admin, rental_list = []):
        self.f_name = f_name
        self.l_name = l_name
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.rental_list = rental_list


class Bike:

    def __init__(self, serial_number, is_rented = False):
        self.serial_number = serial_number
        self.is_rented = is_rented


class Electric_bike(Bike):

    def __init__(self, serial_number, is_rented = False, is_charged = True):
        super().__init__(serial_number, is_rented)
        self.type = "Electric"
        self.is_charged = is_charged


class Road_bike(Bike):

    def __init__(self, serial_number, is_rented = False):
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
    return uname


def sign_in(username, password):
    pass


def creat_account():
    pass


def main():

    while True:

        print(heading_text)

        print(sign_in_text)
    
        input_list = ["1", "2", "3"]
        while (user_input := str(getch())[2]) not in input_list:
            print("[-] You can only select 1, 2 or 3")
            user_input = str(getch())[2]

        match user_input:

            case "1":
                pass

            case "2":
                pass
                
            case "3":
                return 0


if __name__ == "__main__":
    main()
