class User:

    def __init__(self, f_name, l_name, username, rental_list = []):
        self.f_name = f_name
        self.l_name = l_name
        self.username = username
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


def main():
    pass


if __name__ == "__main__":
    main()
