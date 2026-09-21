
# Surgi-Assist

Surgi-Assist is a healthcare web application that helps users find and compare hospitals for a particular surgery. It provides information about hospital details, surgery costs, and applicable government healthcare schemes.

## Features

- User Registration and Login
- Surgery Listing and Search
- Hospital Comparison
- Surgery Cost Range
- Government Scheme Information
- Cost-based Filtering
- Scheme-based Filtering
- Hospital Contact and Address Details
- Google Maps Location

## Tech Stack

- HTML
- CSS
- JavaScript
- Python
- Flask
- MySQL

## Project Workflow

1. User registers or logs into the application.
2. User views the available surgeries.
3. User selects a particular surgery.
4. The Flask backend retrieves the relevant hospital information from MySQL.
5. SQL JOINs combine hospital, surgery, cost, and scheme information.
6. The user can filter hospitals based on cost and scheme availability.
7. Hospital details and location are displayed.

## Database

The database contains multiple related tables:

- Hospital
- Procedure
- Procedure_Offering
- Scheme
- Scheme_Coverage
- User

The `Procedure_Offering` table connects hospitals and procedures and stores the cost range for a particular hospital-procedure combination.

## SQL

SQL JOINs are used to combine information from multiple tables.

- INNER JOIN is used when matching records are required.
- LEFT JOIN is used for optional scheme information so that hospitals without scheme coverage can still be displayed.

## Project Structure

```text
surgiassist/
│
├── app.py
├── hospital_details.html
├── login.html
├── signup.html
├── surgery_details.html
├── surgery_list.html
├── styles.css
├── requirements.txt
└── README.md
