# Medical Diagnostic

## Overview

Medical Diagnostic is a Django web application designed for scheduling medical examinations with specified devices,date and
time. The application also sends an email to the user with a confirmation of their appointment and a password for accessing
the system. Within the system, users can cancel or modify their appointments.

## Features

- **Appointment Scheduling**: Users can schedule medical examinations, specifying date, time, and their contact
  information.
- **Email Confirmation**: The application automatically sends an email to the user with a confirmation of their appointment and
  a unique password for accessing the system.
- **Appointment Management**: Users can log in to the system to view, change, or cancel their appointments.
- **User Authentication**: Secure user authentication system for protecting their data.
- **Admin Panel**: Django admin panel for managing users, appointments, and emails.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/borik1and/medicine_diagnostic.git

2. Navigate to the project directory:

    ```bash
    cd medicine_diagnostic

3. Install dependencies:

    ```bash
    pip install -r requirements.txt

4. Apply database migrations:

    ```bash
   python manage.py migrate
   
5. You should rename ".env-example" to ".env" and fill in the data.
   
## Usage

1. Run the Django development server:
    ```bash
   python manage.py runserver
   
2. Open a web browser and go to http://127.0.0.1:8000 to access the application.
3. Users can schedule their medical examinations by providing the date, time, and contact information.
4. The user receives an email reminder of their appointment along with a password to access the system.
5. Users can log in to the system using their password to view, modify, or delete their examination appointments.

## Contact

For any questions or suggestions, please contact us at borik1and@gmail.com.

