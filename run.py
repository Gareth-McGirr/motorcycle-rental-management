import os
from datetime import date, datetime
from pymongo import MongoClient
from pymongo.errors import OperationFailure
if os.path.exists("env.py"):
    import env


cluster = os.environ.get("CLUSTER")
client = MongoClient(cluster)
db = client.rentalsDB

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
    while True:
        try:
            choice = int(input("Enter Choice: "))
        except ValueError:
            print("You didn't enter a number !")
            continue
    
        if choice == 1:
            vehicle_menu()
            break
        elif choice == 2:
            booking_menu()
            break
        elif choice == 3:
            report_menu()
            break
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

    while True:
        choice = input("Enter Choice: ")
        if choice == "1":
            new_vehicle = get_new_vehicle_details()
            # TO DO: get user to verify details before saving to DB
            save_vehicle_details(new_vehicle)
            break
        elif choice == "2":
            vehicle_update_menu()
            break
        elif choice == "3":
            remove_vehicle()
            break
        elif choice == "4":
            list_all_vehicles()
            break
        elif choice == "0":
            main_menu()
            break
        else:
            print("Invalid choice !!!")
    
    # return back to vehicle menu when other function is complete
    vehicle_menu()


def get_new_vehicle_details():
    """
    Get vehicle details from user and return as a dictionary object
    """
    registration = (input("Enter vehicle registration: ")).upper()
    make = (input("Enter make: ")).upper()  
    model = (input("Enter model: ")).upper()   
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
    # create a dictionary to store vehicle details  
    vehicle = {
        "reg": registration,
        "make": make,
        "model": model,
        "mileage": mileage,
        "service_intervals": service_interval,
        "service_due_distance": miles_left_until_service,
        "bookings": [],
        "checked_out": False
    }
    return vehicle


def vehicle_update_menu():
    """
    Display update vehicle details menu and call functions for updates
    """

    os.system('clear')
    print("UPDATE VEHICLE MENU")
    print("---------------")
    print("1. Add new mileage")
    print("2. Add service")
    print("3. Back to vehicle menu")
    print("0. Main Menu")
    print("---------------")
    choice = input("Enter Choice: ")

    if choice == "1":
        vehicle_update_mileage()
    elif choice == "2":
        vehicle_add_service()
    elif choice == "3":
        vehicle_menu()
    elif choice == "0":
        main_menu()
    else:
        print("Invalid choice !!!")


def display_vehicle_summary(vehicle):
    """
    Display summary details of vehicle object
    """
    reg = vehicle["reg"]
    make = vehicle["make"]
    model = vehicle["model"]
    mileage = vehicle["mileage"]
    print()
    print(f"Make: {make}")
    print(f"Model: {model}")
    print(f"Reg: {reg}")
    print(f"Mileage: {mileage}")
    print()


def vehicle_update_mileage(registration=None):
    """
    Update the mileage on vehicle. Default of None if registration is not passed
    as an arguement. 
    """
    # if reg hasn't already been taken then get the reg to search for
    if registration is None:
        registration = (input("Enter reg: ")).upper()
    result = find_vehicle_by_reg(registration)
    display_vehicle_summary(result)
    while True:
        try:
            new_mileage = int(input("Enter new mileage: "))
            break
        except:
            print("Only whole numbers can be entered !")
    mileage_since_last_updated = new_mileage - result["mileage"]
    print(f"\nMileage since last update is: {mileage_since_last_updated}")
    new_service_due_distance = result["service_due_distance"] - mileage_since_last_updated
    print(f"Service due in {new_service_due_distance} miles")
    update_result = db.vehicles.update_one({"reg": registration}, {"$set": {"mileage": new_mileage, "service_due_distance": new_service_due_distance}})
    input("\nPress any key to continue...")


def vehicle_add_service():
    """
    Update the service date on vehicle. 
    reset the next service due distance. 
    """
    
    registration = (input("Enter reg: ")).upper()
    result = find_vehicle_by_reg(registration)
    display_vehicle_summary(result)
    choice = input("Update as serviced (y/n)?  ")
    if choice == "y":
        today = date.today()
        today_string = today.strftime("%d/%m/%Y")
        new_service_due_distance = result["service_intervals"]
        update_result = db.vehicles.update_one({"reg": registration}, {"$set": {"service_due_distance": new_service_due_distance, "last_serviced_date": today_string}})


def find_vehicle_by_reg(registration):
    """
    Find the vehicle in database that matches the registration
    """ 
    try:
        result = db.vehicles.find_one({"reg": registration})
        return result    
    except OperationFailure:
        print("oops ! Database error")  
        return None


def save_vehicle_details(vehicle):
    """
    save the vehicle details to database
    """
    try:
        db.vehicles.insert_one(vehicle)
        return True
    except OperationFailure:
        print("oops ! Database error: Vehicle was not added")
        input("\nPress any key to continue...")
        return False
        
    
def list_all_vehicles():
    """
    Gets a list of all the vehicles in inventory
    """
    try:
        result = db.vehicles.find({})
    except OperationFailure:
        print("oops ! Database error")
    results_list = list(result)
    if len(results_list) == 0:
        print("No results found")
    else:
        for result in results_list:
            display_vehicle_summary(result)
    input("\nPress any key to continue...")       


def remove_vehicle():
    """
    Get the user to enter registration, search database and remove item
    """
    registration = (input("Enter reg: ")).upper()
    result = find_vehicle_by_reg(registration)
    if result is not None:
        display_vehicle_summary(result)
        verify_delete = input("\n\nDo you want to delete? (y/n) : ")
        if verify_delete == 'y':
            db.vehicles.delete_one({"reg": registration})
            print("\nVehicle has been deleted")
        else:
            print("\nItem not deleted")
    else:
        print(f"\nNo results found for {registration}")
    input("\nPress any key to continue...")


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
    while True:
        try:
            choice = int(input("Enter Choice: "))
        except ValueError:
            print("You didn't enter a number !")
            continue

        if choice == 1:
            save_booking_details(get_booking_details())
            break
        elif choice == 2:
            print("Not Implemented")
            input("\nPress any key to continue...")
            break
        elif choice == 3:
            find_booking_by_ref()
            input("\nPress any key to continue...")
            break
        elif choice == 0:
            main_menu()
        else:
            print("Invalid choice !!!")
    booking_menu()


def get_booking_details():
    """
    Function to get details of customer booking
    Function will ask for details and validate user input
    If customer has made previous bookings then details will be displayed
    and user does not need to enter. 
    """
    # Chaeck that vehicle exists and display for confirmation of correct vehicle
    while True:
        registration = (input("Enter vehicle registration: ")).upper()
        this_vehicle = find_vehicle_by_reg(registration)
        if this_vehicle is not None:
            display_vehicle_summary(this_vehicle)
            answer = input("Is this correct (y/n) ?")
            if answer.upper() == 'Y':
                break 
        else:
            print("Vehicle not found")

    # TO DO: Check if customer with email exists and display details
    
    email = (input("Enter email: ")).upper()

    while True:
        try:
            tel_number = int(input("Enter contact number: "))
            break
        except ValueError:
            print("Phone number cannot contain letters !!")
    
    name = input("Enter Name: ")
    start_date = input("Enter Start Date (dd/mm/yyyy): ")
    end_date = input("Enter Return Date (dd/mm/yyyy): ")

    # get booking number for this booking
    # and generate next booking number to add to DB
    result = db.booking_reference.find_one()
    booking_number = result["next_booking_reference"]
    next_booking_number = booking_number + 1
    db.booking_reference.update_one({}, {"$set": {"next_booking_reference": next_booking_number}})
    
    # convert date strings to date objects
    start_date_obj = datetime.strptime(start_date, '%d/%m/%Y')
    end_date_obj = datetime.strptime(end_date, '%d/%m/%Y')

    this_booking = {
        "reg": registration,
        "email": email,
        "tel_no": tel_number,
        "name": name,
        "start_date": start_date_obj,
        "end_date": end_date_obj,
        "booking_reference": booking_number
    }
    return this_booking


def find_booking_by_ref():
    """
    Function to find a booking with booking ref 
    """
    while True:
        try:
            booking_ref = int(input("Enter Booking Reference Number: "))
            break
        except:
            print("Numbers only !!") 
    result = db.bookings.find_one({"booking_reference": booking_ref})
    if result is not None:
        print(result)
    else:
        print("Not found")


def save_booking_details(booking):
    """
    save the booking details to database
    """
    try:
        db.bookings.insert_one(booking)
        add_booking_to_vehicle(booking["booking_reference"], booking["reg"])
        print("Booking Saved")
        input("\nPress any key to continue...")
    except OperationFailure:
        print("oops ! Database error: Booking was not added")
        input("\nPress any key to continue...")
    return    


def add_booking_to_vehicle(booking_number, registration):
    """
    Adds the booking number to the vehicle
    """
    
    vehicle = find_vehicle_by_reg(registration)
    booking_list = vehicle["bookings"]
    booking_list.append(booking_number)
    update_result = db.vehicles.update_one({"reg": registration}, {"$set": {"bookings": booking_list}})


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
   

def main():
    """
    Run all program functions
    """
    main_menu()


print("\n\nWelcome to Motorcycle Rental Management.\n")
main()