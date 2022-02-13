import os
from datetime import date, datetime, timedelta

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
    print("5. Check availabilty - One")
    print("6. Check availabilty - All")
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
        elif choice == "5":
            check_availability_one_vehicle()
            break
        elif choice == "6":
            list_all_vehicles_available()
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
        except ValueError:
            print("Only whole numbers can be entered !")
    while True:
        try:
            service_interval = int(input("Enter service interval: "))
            break
        except ValueError:
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
    print(f"Make: {make} Model: {model}")
    print(f"Reg: {reg} Mileage: {mileage}")


def vehicle_update_mileage(registration=None):
    """
    Update the mileage on vehicle. 
    Default of None if registration is not passed
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
        except ValueError:
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


def check_availability_one_vehicle():
    """
    checks if vehicle is available in date range
    converts date range to a list and checks if 
    any date in the list is in date ranges of bookings
    for the vehicle 
    """
    registration = (input("Enter reg: ")).upper()
    vehicle = find_vehicle_by_reg(registration)
    display_vehicle_summary(vehicle)
    booking_number_list = vehicle["bookings"]
    
    # Get the start and end date from user 
    start_date = input("Enter Start Date (dd/mm/yyyy): ")
    date_strt = datetime.strptime(start_date, '%d/%m/%Y')
    end_date = input("Enter Start Date (dd/mm/yyyy): ")
    date_end = datetime.strptime(end_date, '%d/%m/%Y')

    # inialize as available 
    available = True    
    for booking_number in booking_number_list:
        # get the booking start and end date
        result = db.bookings.find_one({"booking_reference": booking_number})
        start = result["start_date"]
        end = result["end_date"]
        # calculte number of days for range       
        period = abs((end - start).days)
        daterange = []
        # add each date in the range to a list
        for day in range(period):
            my_date = (start + timedelta(days=day))
            daterange.append(my_date)
        # loop through each date in the list    
        for ele in daterange:
            # checking for date in range
            if ele >= date_strt and ele <= date_end:
                # set as unavailable
                available = False
    # print message to user if available or not
    if available:
        print("Vehicle is available for those dates")
        input("\nPress any key....")
    else:
        print("Not available for those dates")
        input("\nPress any key....")


def list_all_vehicles_available():
    """
    list all available vehicles within date range
    """
    # Get the start and end date from user
    start_date = input("Enter Start Date (dd/mm/yyyy): ")
    date_strt = datetime.strptime(start_date, '%d/%m/%Y')
    end_date = input("Enter Start Date (dd/mm/yyyy): ")
    date_end = datetime.strptime(end_date, '%d/%m/%Y')

    # Get list of all vehicles in system
    try:
        vehicles = db.vehicles.find({})
    except OperationFailure:
        print("oops ! Database error")
    vehicle_list = list(vehicles)
    if len(vehicle_list) == 0:
        print("No results found")
    else:
        for vehicle in vehicle_list:
            booking_number_list = vehicle["bookings"]
            # inialize as available 
            available = True    
            for booking_number in booking_number_list:
                # get the booking
                result = db.bookings.find_one({"booking_reference": booking_number})
                start = result["start_date"]
                end = result["end_date"]
                # calculte number of days for range       
                period = abs((end - start).days)
                daterange = []
                for day in range(period):
                    my_date = (start + timedelta(days=day))
                    daterange.append(my_date)

                for ele in daterange:
                    # checking for date in range
                    if ele >= date_strt and ele <= date_end:
                        # set as unavailable
                        available = False
            
            if available:
                display_vehicle_summary(vehicle)
            
    input("\nPress any key....")    

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
            create_booking()
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


def create_booking():
    """
    Function to get details of customer booking
    Function will ask for details and validate user input
    If customer has made previous bookings then details will be displayed
    and user does not need to enter.
    """
    
    # presume that customer is new
    new_customer = True

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

    # Check if customer with email exists and display details
    email = (input("Enter email: ")).upper()
    this_customer = find_customer(email)
    if this_customer is not None:
        display_customer(this_customer)
        answer = (input("Is this correct (y/n) ?")).upper()
        if answer == 'Y':
            # TO DO: validate the dates entered,
            # try to convert to date object in specified foramt ?
            new_customer = False
            name = this_customer["name"]
            tel_number = this_customer["email"]
            start_date = input("Enter Start Date (dd/mm/yyyy): ")
            end_date = input("Enter Return Date (dd/mm/yyyy): ")
    else:
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
        "name": name,
        "tel_no": tel_number,
        "email": email,
        "start_date": start_date_obj,
        "end_date": end_date_obj,
        "booking_reference": booking_number
    }
    save_booking_details(this_booking)
    if new_customer:
        this_customer = {
            "name": name,
            "tel_no": tel_number,
            "email": email,
            "bookings": [booking_number]
        }
        db.customers.insert_one(this_customer)
    else:
        booking_list = this_customer["bookings"]
        booking_list.append(booking_number)
        db.customers.update_one({"email": email}, {"$set": {"bookings": booking_list}})
    return


def find_booking_by_ref():
    """
    Function to find a booking with booking ref
    """
    while True:
        try:
            booking_ref = int(input("Enter Booking Reference Number: "))
            break
        except ValueError:
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


def find_customer(email_address):
    """
    Function to search for customer in DB by passing email address
    """
    try:
        result = db.customers.find_one({"email": email_address})
        return result
    except OperationFailure:
        print("oops ! Database error")
        return None


def display_customer(customer_obj):
    """
    Displays Customer details
    """
    name = customer_obj["name"]
    phone_no = customer_obj["tel_no"]
    email = customer_obj["email"]
    print(f"Name: {name}")
    print(f"Tel No: {phone_no}")
    print(f"Email: {email}")


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
