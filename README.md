Employee Management System (EMS)
================================
Project Overview
------------------
The Employee Management System (EMS) is a Python-based CLI application to manage employees, attendance, leave, and payroll efficiently. It supports both Manager and Employee roles with role-specific dashboards and functionalities.

Key Features:
-------------
Employee registration and login
Password management with strong validation
Profile view and update
Attendance management: punch in/punch out with working hours and overtime calculation
Leave management: apply, track, and view leave balance
Payroll deductions for unpaid leave or insufficient working hours
Manager dashboard: add/edit/delete/search employees, approve/reject leaves, manage salaries

Requirements
-------------
Software Requirements:
----------------------
Python 3.8+
SQLite3

Python Libraries:
-----------------
sqlite3 (built-in)
getpass (built-in)
re (built-in)
datetime (built-in)
time (built-in)
tabulate (built-in)

Database Schema
----------------
1. User Table
| Column   | Type    | Description             |
| -------- | ------- | ----------------------- |
| user_id  | INTEGER | Primary key             |
| username | TEXT    | Login username          |
| password | TEXT    | User password           |
| role     | INTEGER | 1: Manager, 2: Employee |

2. Department Table
| Column    | Type    | Description     |
| --------- | ------- | --------------- |
| dept_id   | INTEGER | Primary key     |
| dept_name | TEXT    | Department name |

3. Manager Table
| Column          | Type    | Description         |
| --------------- | ------- | ------------------- |
| manager_id      | INTEGER | Primary key         |
| user_id         | INTEGER | Foreign key to User |
| dept_id         | INTEGER | Department ID       |
| name            | TEXT    | Manager name        |
| contact         | INTEGER | Contact number      |
| email           | TEXT    | Email ID            |

4. Employee Table
| Column          | Type    | Description         |
| --------------- | ------- | ------------------- |
| emp_id          | INTEGER | Primary key         |
| user_id         | INTEGER | Foreign key to User |
| dept_id         | INTEGER | Department ID       |
| manager_id      | INTEGER | Foreign key-Manager |
| name            | TEXT    | Employee name       |
| job_title       | TEXT    | Designation         |
| date_of_joining | TEXT    | YYYY-MM-DD          |
| salary          | REAL    | Monthly salary      |
| contact         | INTEGER | Contact number      |
| email           | TEXT    | Email ID            |

5. Attendance Table
| Column         | Type    | Description                      |
| -------------- | ------- | -------------------------------- |
| emp_id         | INTEGER | Employee ID                      |
| date           | TEXT    | Attendance date                  |
| clock_in       | TEXT    | Time of punch in                 |
| clock_out      | TEXT    | Time of punch out                |
| working_hours  | REAL    | Total worked hours               |
| overtime_hours | REAL    | Overtime hours                   |
| status         | TEXT    | PRESENT/HALF DAY/OVERTIME/ABSENT |

6. Leave_Record Table
| Column         | Type    | Description               |
| -------------- | ------- | ------------------------- |
| leave_id       | INTEGER | Primary key               |
| emp_id         | INTEGER | Employee ID               |
| leave_type     | TEXT    | Type of leave             |
| start_date     | TEXT    | YYYY-MM-DD                |
| end_date       | TEXT    | YYYY-MM-DD                |
| leave_duration | REAL    | Number of days            |
| status         | TEXT    | PENDING/APPROVED/REJECTED |

7. Leave_Balance Table
| Column      | Type    | Description          |
| ----------- | ------- | -------------------- |
| emp_id      | INTEGER | Employee ID          |
| total_leave | REAL    | Remaining leave days |

8. Payroll Table
| Column    | Type    | Description                      |
| --------- | ------- | -------------------------------- |
| emp_id    | INTEGER | Employee ID                      |
| basic_pay | REAL    | Monthly salary                   |
| deduction | REAL    | Deduction for leave/unpaid hours |

Usage Guide
-----------
Main Menu Options:
------------------
Register
Login
Exit

Manager Dashboard:
------------------
View/Add/Edit/Delete/Search Employees
Manage Attendance, Leave, and Salary

Employee Dashboard:
--------------------
Reset Password
View/Edit Profile
Punch In / Punch Out
Apply for Leave
View Leave Status
View Salary Details

Note:
Passwords must contain at least 1 uppercase, 1 lowercase, 1 digit, 1 special character, and minimum 6 characters.
Leave applications exceeding balance are automatically treated as Paid Leave and deducted from salary.
