import os
from pymongo import MongoClient

if os.path.exists("env.py"):
    import env


cluster = os.environ.get("CLUSTER")

client = MongoClient(cluster)


def main_menu():
    """
    Displays the main menu ion the terminal
    """

    os.system('clear')
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
   
    os.system('clear')
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
        # TO DO: get user to verify details before saving to DB
        save_vehicle_details(new_vehicle)
    elif choice == "2":
        print("Not Implemented")
    elif choice == "3":
        print("Not Implemented")
    elif choice == "4":
        list_all_vehicles()
    elif choice == "0":
        main_menu()
    else:
        print("Invalid choice !!!")


def booking_menu():
    """
    Display booking menu option

    """
   
    os.system('clear')
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
   
    os.system('clear')
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
    while True:
        try:
            mileage = int(input("Enter current mileage: "))
            break
        except:
            print("Only whole numbers can be entered !")
    while True:
        try:
            service_interval = int(input("Enter service interval: "))
            break
        except:
            print("Only whole numbers can be entered !") 
    next_service_due = mileage + service_interval
    miles_left_until_service = next_service_due - mileage
    #create a dictionary to store vehicle details  
    vehicle = {
        "reg": registration,
        "make": make,
        "model": model,
        "mileage": mileage,
        "service_intervals": service_interval,
        "service_due_distance": miles_left_until_service
    }
    return vehicle


def save_vehicle_details(vehicle_dict):
    """
    save the vehicle details to database
    """
    db = client.rentalsDB
    vehicles = db.vehicles
    result = vehicles.insert_one(vehicle_dict)
    print(result)


def list_all_vehicles():
    """
    Gets a list of all the vehicles in inventory
    """
    db = client.rentalsDB
    vehicles = db.vehicles
    results = vehicles.find({})
    for result in results:
        print(result)


def main():
    """
    Run all program functions
    """
    main_menu()

print("\n\nWelcome to Motorcycle Rental Management.\n")
main()