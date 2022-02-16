# Motorcycle Rental Management

TODO Gif of live site

## Table Of Contents

* [Introduction](#Introduction)
    * [Site Goals](#Site-Goals)
    * [Target Audience](#Target-Audience)
    * [User stories](#User-Stories)
    * [Features Planned](#Features-Planned)
- [Structure](#Structure)
    * [Logical Flow](#Logical-Flow)
    * [Features](#Features)
    * [Features left to Implement](#Features-Left-to-Implement)
* [Technologies](#Technologies)
* [Testing](#Testing)
    * [Functional Testing](#Functional-Testing)
    * [Pep8 Validation](#Pep8-Validation)
    * [Bugs and Fixes](#Bugs-and-Fixes)
* [Deployment](#Deployment)
    * [Version Control](#Version-Control)
    * [MongoDB Setup](#MongoDB-Setup)
    * [Heroku Deployment](#Heroku-Deployment)
    * [Clone Locally](Clone-Locally)
* [Credits](#Credits)
  * [Content](#Content)
  * [Acknowledgements](#Acknowledgements)

## Introduction

This project was created in order for small businesses to easily keep track of their Vehicle rentals. It will allow them to keep track of vehicle and bookings information as well as update them.

### Site Goals

* Provide a simple application to allow the site owner to keep track of vehicles, bookings and maintenance for their rental business.

### Target Audience

* Small vehicle rental companies that want to keep track of stock, bookings and view daily reports.

### User Stories

* As a User, I would like to be able to easily find the various menus so that I can view information or add / edit records.
* As a User, I would like to be able to manage my vehicles so that I can easily keep track of what vehicles I have available and edit / remove as neccessary.
* As a User, I would like to be able to manage bookings so that I can add, delete and find customer bookings with ease.
* As a User, I would like to be able to view sevice records so I can see estimate when a new service is due.
* As a User, I would like to be able to return to the main menu without having to restart the application.

### Features Planned

* Simple, easy to use application with clear navigation.
* Simple database storage for:
    * Create, read, update and delete functionality for vehicles.
    * Create, read and delete functionality for vehicle bookings.
* Ability to view service records.
* Return to main menu option through sub menus.

## Structure

### Features

USER STORY

`
As a User, I would like to be able to easily find the various menus so that I can view information or add / edit records.
`

IMPLEMENTATION
* Main Menu
    * When the application starts, a main menu will appear with the following options:
        * 1) Vehichles
        * 2) Bookings
    * The user must input a correct number corresponding to each menu or they will be alerted of an inccorect choice and the menu will be presented again.
    * This feature will allow the user to easily access the sub menus to each category in order to perform the operations needed.

USER STORY

`
As a User, I would like to be able to manage my vehicles so that I can easily keep track of what vehicles I have available and edit / remove as neccessary.
`

`
As a User, I would like to be able to view sevice records so I can see estimate when a new service is due. (Fulfilled on option 4)
`

IMPLEMENTATION
* Vehicle Menu
    * When the user selects Vechicles from the main menu, the following menu options will appear:
        * 1) Add new - This option will ask for user input on the vehicle and once all data is input, will save the data to MongoDB.
        * 2) Update - This option will open the Vehicle Update Menu, implementation described below.
        * 3) Remove - This option will allow the user to delete a vehicle from MongoDB after inputting registration and confirming deletion.
        * 4) Service History - This option whille allow the user to view a vehicles service history.
        * 5) List All - This option will display all vehicles currently stored in mongoDB.
        * 0) Main Menu - This option will return the user to the main menu.
    * The user must input a correct number corresponding to each menu or they will be alerted of an inccorect choice and the menu will be presented again.
    * This feature will allow the user to easily view, add, edit and delete vehicles. 

* Vehicle Update Menu
    * When vehicle update menu has been selected, the following menu options appear:
        * 1) Add new milage - This will allow user to find vehicle and update milage. This also sets the next service due field.
        * 2) Add service - This will allow the user to find vehicle and add new service details.
        * 3) Back to vehicle menu -0 This will allow the user to go back to the vehicle menu.
        * 0) Main Menu - This option will return the user to the main menu.

USER STORY

`
As a User, I would like to be able to manage bookings so that I can add, delete and find customer bookings with ease.
`

IMPLEMENTATION
* Booking Menu
    * When the user selects Bookings from the main menu, the following menu options will appear:
        * 1) New Booking - This option will ask for user input on the new booking and once all data is input, will save the data to MongoDB.
        * 2) List Bookings - This option will display all upcoming bookings for number of days specified on input for bookings currently stored in MongoDB.
        * 3) Find Booking - This option will allow the user to search for a specific booking, view details and the following option will be available:
            * Cancel booking (Enter "c") - This will allow the user to cancel the booking.
        * 4) Check availability - One - This will allow the user to check the availability of one vehicle between 2 dates. If vehicle is available, an option is given to add a booking and the new booking function is called.
        * 5) Check availability - All - This lists all available vehicles between 2 dates and takes an input of start date and end date.
       * 0) Main Menu - This option will return the user to the main menu.
    * The user must input a correct number corresponding to each menu or they will be alerted of an inccorect choice and the menu will be presented again.
    * This feature will allow the user to easily view, add and search for a booking.

USER STORY

`
As a User, I would like to be able to return to the main menu without having to restart the application.
`

IMPREMENTATION
* All sub menus will have an option to return to the main menu, this will typically be 0.
* This will allow the user to return to the main menu if they selected the wrong option or are finished with the particular menu.

### Features Left to Implement

As a future enhancement, I would like to add some basic functionality to calculate pricing and keep track of sales. I would also like to implement reporting to the application that will allow users to view sales records.

### Logical Flow

**Main Menu**

![Main Menu](docs/flow/main_menu.JPG)

**Vehicle Menu**

![Vehicle Menu](docs/flow/vehicle_menu.JPG)

**Vehicle Update Menu**

![Vehicle Update Menu](docs/flow/vehicle_update_menu.JPG)

**Booking Menu**

![Booking Menu](docs/flow/booking_menu.JPG)

## Technologies

## Testing

### Functional Testing

### Pep8 Validation

### Bugs and Fixes

## Deployment

## Credits

### Code

### Acknowledgements