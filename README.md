# Cozy
### peer-to-peer marketplace for short-term rentals and lodging

# My Django Project

This is a Django project for managing destinations and bookings.

## Description

This project allows users to view, search, and book accommodations (destinations) hosted by various hosts. Users can sign up, log in, and save their favorite destinations. Hosts can manage their listings, view bookings, and interact with guests.

## Features

- User authentication (sign up, login, logout)
- Destination listing and details view
- Search functionality to find destinations based on city and number of guests
- Booking system for users to reserve accommodations
- Host dashboard to manage listings and bookings
- User profile pages

## Technologies Used

- Django: Python web framework for building web applications
- HTML/CSS: Frontend languages for structuring and styling web pages
- Bootstrap: CSS framework for responsive web design
- SQLite: Lightweight relational database used for development
- Heroku: Cloud platform for deploying and hosting web applications

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/samuelmideksa/cozy.git
    ```

2. Install dependencies:

    ````bash
    pip install -r requirements.txt
    ```


3. Run migrations:

    ```bash
    python manage.py migrate
    ```


4. Start the development server:

    ```bash
    python manage.py runserver
    ```


5. Access the application at http://localhost:8000 in your web browser.

## Usage

- Sign up for a user account to access full functionality.
- Explore destinations, search for accommodations, and make bookings.
- Hosts can log in to manage their listings and view bookings.
- Users can save their favorite destinations for future reference.

## Credits

This project was created by Samuel Mideksa.
