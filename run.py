from os import system

def main_menu():
    """
    Displays the main menu ion the terminal
    """
    system('clear')
    print("MAIN MENU")
    print("---------------")  
    print("1. Vehicles")
    print("2. Bookings")
    print("3. Reports")
    print("---------------")
    choice = input("Enter Choice: ")
    
    # To Do: validation on user input

    if choice == "1":
        vehicle_menu()
    elif choice == "2":
        booking_menu()
    elif choice == "3":
        report_menu()
    else:
        print("Invalid choice !!!")


def vehicle_menu():
    """
    Display Vehicle menu option

    """
   
    system('clear')
    print("VEHICLE MENU")
    print("---------------")
    print("1. Add new")
    print("2. Update")
    print("3. Remove")
    print("4. List All")
    print("0. Main Menu")
    print("---------------")
    choice = input("Enter Choice: ")

    if choice == "1":
        new_vehicle = get_new_vehicle_details()
        print(new_vehicle)
    elif choice == "2":
        print("Not Implemented")
    elif choice == "3":
        print("Not Implemented")
    elif choice == "4":
        print("Not Implemented")
    elif choice == "0":
        main_menu()
    else:
        print("Invalid choice !!!")


def booking_menu():
    """
    Display booking menu option

    """
   
    system('clear')
    print("BOOKING MENU")
    print("---------------")
    print("1. New Booking")
    print("2. List Bookings")
    print("3. Find Booking")
    print("0. Main Menu")
    print("---------------")
    choice = input("Enter Choice: ")

    if choice == "1":
        print("Not Implemented")
    elif choice == "2":
        print("Not Implemented")
    elif choice == "3":
        print("Not Implemented")
    elif choice == "0":
        main_menu()
    else:
        print("Invalid choice !!!")


def report_menu():
    """
    Display report menu options

    """
   
    system('clear')
    print("REPORT MENU")
    print("---------------")
    print("1. Todays Bookings")
    print("2. Bike Service Report")
    print("3. Sales Report")
    print("0. Main Menu")
    print("---------------")
    choice = input("Enter Choice: ")

    if choice == "1":
        print("Not Implemented")
    elif choice == "2":
        print("Not Implemented")
    elif choice == "3":
        print("Not Implemented")
    elif choice == "0":
        main_menu()
    else:
        print("Invalid choice !!!")


def get_new_vehicle_details():
    """
    Get vehicle details from user and return as a dictionary object
    """
    registration = input("Enter vehicle registration: ")
    make = input("Enter make: ")
    model = input("Enter model: ")
    mileage = input("Enter current mileage: ")

    vehicle = {
        "reg": registration,
        "make": make,
        "model": model,
        "mileage": mileage 
    }
    return vehicle


def main():
    """
    Run all program functions
    """
    main_menu()


print("\n\nWelcome to Motorcycle Rental Management.\n")
main()