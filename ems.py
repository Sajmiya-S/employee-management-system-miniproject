#------------------------------------------- EMPLOYEE MANAGEMENT SYSTEM --------------------------------------#

import sqlite3
import getpass
import re
import datetime
import time
from tabulate import tabulate
#------------------------------------------- DATABASE SETUP ----------------------------------------------#

def setup_db():
    conn = sqlite3.connect('emp.db')
    cursor = conn.cursor()

    # USER RECORD
    cursor.execute('''

                    CREATE TABLE IF NOT EXISTS User(
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(20) UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role_id INTEGER
                )
                ''')

    # DEPARTMENT RECORD
    cursor.execute('''
                
                    CREATE TABLE IF NOT EXISTS Department(
                        dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        dept_name VARCHAR(20)
                )
                ''')

    # MANAGER RECORD
    cursor.execute('''

                    CREATE TABLE IF NOT EXISTS Manager(
                        manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        dept_id INTEGER,
                        name VARCHAR(20),
                        contact INTEGER,
                        email VARCHAR(30),
                        FOREIGN KEY (user_id) REFERENCES User(user_id),
                        FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
                )
                ''')

    # EMPLOYEE RECORD
    cursor.execute('''
                
                CREATE TABLE IF NOT EXISTS Employee(
                        emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        dept_id INTEGER,
                        manager_id INTEGER,
                        name VARCHAR(20),
                        job_title VARCHAR(20),
                        date_of_joining DATE,
                        salary INTEGER,
                        contact INTEGER,
                        email VARCHAR(30), 
                        FOREIGN KEY (user_id) REFERENCES User(user_id),
                        FOREIGN KEY (dept_id) REFERENCES Department(dept_id),
                        FOREIGN KEY (manager_id) REFERENCES Manager(manager_id)
                )
                ''')

    # ATTENDANCE RECORD
    cursor.execute('''
                
                CREATE TABLE IF NOT EXISTS Attendance(
                        att_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        emp_id INTEGER,
                        date DATE,
                        clock_in TIME,
                        clock_out TIME,
                        working_hours NUMERIC,
                        overtime_hours NUMERIC,
                        status VARCHAR(20),
                        FOREIGN KEY (emp_id) REFERENCES Employee(emp_id)
                )
                ''')

    # LEAVE RECORD
    cursor.execute('''
                
                CREATE TABLE IF NOT EXISTS Leave_Record(
                        leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        emp_id INTEGER,
                        leave_type VARCHAR(20),
                        start_date DATE,
                        end_date DATE,
                        leave_duration NUMERIC,
                        leave_balance NUMERIC,
                        status VARCHAR(20),
                        FOREIGN KEY (emp_id) REFERENCES Employee(emp_id)
                )
                ''')

    # LEAVE BALANCE RECORD
    cursor.execute('''
                
                CREATE TABLE IF NOT EXISTS Leave_Balance(
                   balance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   emp_id INTEGER,
                   total_leave NUMERIC,
                   FOREIGN KEY (emp_id) REFERENCES Employee(emp_id)
                   )
                   ''')
    

    # PAYROLL RECORD
    cursor.execute('''
                
                CREATE TABLE IF NOT EXISTS Payroll(
                        payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        emp_id INTEGER,
                        basic_pay NUMERIC NOT NULL,
                        allowance NUMERIC,
                        deduction NUMERIC,
                        overtime_pay NUMERIC,
                        net_pay NUMERIC,
                        pay_date DATE,
                        FOREIGN KEY (emp_id) REFERENCES Employee(emp_id)
                )
                ''')

    # cursor.executemany('''                   
    #                 INSERT OR IGNORE INTO Department(dept_name)
    #                     VALUES (?)''',
    #                             [('HR',),
    #                             ('FINANCE',),
    #                             ('IT',),
    #                             ('SALES',),
    #                             ('MARKETING',),
    #                             ('OPERATIONS',),
    #                             ('ADMINISTRATION',)])

    conn.commit()
    conn.close()

#----------------------------------------------- EXCEPTIONS  ----------------------------------------------------#

class emptyError(Exception):
    pass

class roleError(Exception):
    pass

class numError(Exception):
    pass

class rangeError(Exception):
    pass

class pwError(Exception):
    pass

class charError(Exception):
    pass

#----------------------------------------   USERNAME    --------------------------------------------------#

def get_username():
    while True:
        try:
            username = input('\nUsername : ')
            if not username:
                raise emptyError
            elif username.isdigit():
                raise numError
            elif len(username) <= 3:
                raise rangeError
            elif not username.isalnum():
                raise charError
        except emptyError:   
            print('\n ⚠️ User name is required!!!') 
            continue
        except numError:
            print('\n ⚠️ Invalid username!!! Username should contain letters')
            continue
        except rangeError:
            print('\n ⚠️ Username should contain more than 3 letters ')
            continue
        except charError:
            print('\n ⚠️ Username should not contain any special characters')
            continue
        else:
            return username

#--------------------------------------------- PASSWORD -----------------------------------------#

def get_password():
    while True:
        password = getpass.getpass('\nPassword : ')
        if len(password) < 6:
            print("⚠️ Password too short! Must be at least 6 characters.")
            continue
        elif not re.search(r"[A-Z]", password):
            print("⚠️ Password must contain at least one uppercase letter.")
            continue
        elif not re.search(r"[a-z]", password):
            print("⚠️ Password must contain at least one lowercase letter.")
            continue
        elif not re.search(r"[0-9]", password):
            print("⚠️ Password must contain at least one digit.")
            continue
        elif not re.search(r"[@#$%^&*-_!]", password):
            print("⚠️ Password must contain at least one special character .")
            continue
        else:
            confirm_pw = getpass.getpass('\nConfirm password : ')
            if password != confirm_pw:
                print('\n ⚠️ Passwords donot match. Please try again.')
                continue
            else:
                return password

#---------------------------------------- ROLE ID --------------------------------------------#

def get_role_id():
    while True:
        try:   
            role = int(input('\nEnter Role ID (0 for Employee  / 1 for Manager) : '))
            if role > 1:
                    raise roleError
        except roleError:
            print('\n ⚠️ Invalid Role ID !!!')
            continue
        except ValueError:
            print('\n ⚠️ Invalid Role ID!!! Should be a number')
            continue
        else:
            return role

#------------------------------------------ USER REGISTRATION  --------------------------------------------#

def register():
    conn = sqlite3.connect('emp.db')
    cursor = conn.cursor()
    
    print('\n\t\t\t\t-----------------------------------\n\t\t\t\tWelcome to user registration portal\n\t\t\t\t-----------------------------------')

    with open('instructions.txt','r') as file:
        for i in file.readlines():
            print(i)
            time.sleep(0.2)

    username = get_username().lower().strip()
            
    cursor.execute('''
                           
                    SELECT user_id FROM User WHERE username = ? 
                    ''',(username,))

    exist = cursor.fetchall()

    if exist:
        print('\nUsername Already Exists')
    else:
        password = get_password()
        role = get_role_id()

        cursor.execute('''
            INSERT INTO User(username,password,role_id)
                    VALUES (?,?,?) 
            ''',(username,password,role))
        
        cursor.execute('''
                       SELECT user_id FROM User WHERE username = ?
                       ''',(username,))
        
        user_id = cursor.fetchone()

        
        if role == 1:
            print('\n\t\t--------------------------------\n\t\t 👤 Manager Profile Details 👤 \n\t\t--------------------------------\n Please provide the required information below ⬇️ ⬇️ ⬇️')
            while True:
                try:
                    name = input('\nFull Name : ').upper()
                    if not re.fullmatch(r'[A-Za-z ]+', name):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid Name !!! Use letters and spaces only\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    dept = input('\nDepartment Name : ').upper()
                    cursor.execute('''
                                SELECT dept_id FROM Department WHERE dept_name = ?
                            ''',(dept,))
                    dept_id = cursor.fetchone()
                    if not dept_id:
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid Department Name !!! Use letters only\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    contact = input('\nContact Number : +91-')
                    if not re.fullmatch(r'\d{10}',contact):
                        raise numError
                except numError:
                    print('\n ⚠️ Invalid contact number !!! It should contain exactly 10 digits\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    email = input('\nMail id : ').lower()
                    if not re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid mail id !!!\n---------------------------------------------------------------------------------------------------')
                    continue
                else:
                    print('\n--------------------------------------------------------------')
                    print('\t\t 📋 REGISTRATION SUMMARY 📋 ')
                    print('--------------------------------------------------------------')
                    print(f'👤 Name           : {name}')
                    print(f'🏢 Department     : {dept}')
                    print(f'📞 Contact No.    : +91-{contact}')
                    print(f'📧 Email ID       : {email}')
                    break

            while True:
                print('\nPlease review your details carefully before submission.')
                print('  [1] ✅ Submit Registration')
                print('  [2] ✏️  Edit / Continue Registration')
                print('  [3] ❌ Cancel Registration')
                
                choice = input('\nSelect an option : ')
                if choice == '1':
                    cursor.execute('''
                                    INSERT INTO Manager(user_id,dept_id,name,contact,email)
                                        VALUES (?,?,?,?,?)
                                ''',(user_id[0],dept_id[0],name,contact,email))
                    
                    print(f'\n 🎉 {name} successfully registered as Manager✅')
                    break
                elif choice == '2':
                    print('\n🔄 Restarting registration process...')
                    return register()  
                
                elif choice == '3':
                    print('\n ❌ Registration cancelled ❌')
                    return

        else:
            try:
                man_id = int(input('\nEnter your manager_id : '))
            except ValueError:
                print('\n ⚠️ Invalid Manager ID !!!')
            cursor.execute('''
                           
                           SELECT manager_id FROM Manager WHERE manager_id = ?
                           ''',(man_id,))
            
            manager = cursor.fetchone()
            if not manager:
                print('\n ⚠️ Invalid Manager ID! You are not authorised to register.')
                return
           
            print('\n Manager ID verified ✅ . Proceed with registration. ')
            print('\n--------------------------------\n 👤 Employee Profile Details 👤 \n--------------------------------\n Please provide the required information below ⬇️ ⬇️ ⬇️')
            while True:
                try:
                    name = input('\nFull Name : ').upper()
                    if not re.fullmatch(r'[A-Za-z ]+', name):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid Name !!! Use letters and spaces only\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    dept = input('\nDepartment Name : ').upper()
                    cursor.execute('''
                                SELECT dept_id FROM Department WHERE dept_name = ?
                            ''',(dept,))
                    dept_id = cursor.fetchone()
                    if not dept_id:
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid Department Name !!! Use letters only\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    title = input('\nDesignation : ').upper()
                    if not re.fullmatch(r'[A-Za-z ]+',title):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid job title !!! Use letters and spaces only\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    join_date = input('\nDate of joining(YYYY-MM-DD) : ')
                    datetime.datetime.strptime(join_date, r"%Y-%m-%d")                   
                except ValueError:
                    print('\n ⚠️ Invalid date format !!!\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    salary = int(input('\nSalary : '))
                except ValueError:
                    print('\n ⚠️ Invalid entry !!! Salary should be a number\n--------------------------------------------------------------------------------------------------- ')
                    continue
                try:
                    contact = input('\nContact Number : +91-')
                    if not re.fullmatch(r'\d{10}',contact):
                        raise numError
                except numError:
                    print('\n ⚠️ Invalid contact number !!! It should contain exactly 10 digits\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    email = input('\nMail id : ').lower()
                    if not re.fullmatch( r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',email):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid mail id !!!\n---------------------------------------------------------------------------------------------------')
                    continue
                else:
                    print('\n--------------------------------------------------------------')
                    print('\t\t 📋 REGISTRATION SUMMARY 📋')
                    print('--------------------------------------------------------------')
                    print(f'👤 Name            : {name}')
                    print(f'🏢 Department      : {dept}')
                    print(f'🧑‍💼 Designation   : {title}')
                    print(f'📅 Date of Joining : {join_date}')
                    print(f'💰 Salary          : ₹{salary}')
                    print(f'📞 Contact No.     : +91-{contact}')
                    print(f'📧 Email ID        : {email}')
                    break    
            while True:
                print('\nPlease review your details carefully before submission.')
                print('Select an option:')
                print('  [1] ✅ Submit Registration')
                print('  [2] ✏️  Edit / Continue Registration')
                print('  [3] ❌ Cancel Registration')
                
                choice = input('\nEnter your choice : ')
                if choice == '1':    
                    cursor.execute('''
                                    INSERT INTO Employee(user_id,dept_id,manager_id,name,job_title,date_of_joining,salary,contact,email)
                                        VALUES (?,?,?,?,?,?,?,?,?)
                                    ''',(user_id[0],dept_id[0],manager[0],name,title,join_date,salary,contact,email))
                    cursor.execute('''
                                    SELECT emp_id FROM Employee WHERE user_id = ?
                                    ''',(user_id[0],))
                    emp_id = cursor.fetchone()[0]
                
                    cursor.execute('''
                                INSERT INTO Payroll(emp_id,basic_pay,allowance,deduction,overtime_pay,net_pay)
                                    VALUES (?,?,0,0,0,?)
                                    ''',(emp_id,salary,salary))
                    cursor.execute('''
                                INSERT INTO Leave_Balance(emp_id,total_leave)
                                    VALUES (?,42)
                                ''', (emp_id, ))
                    break

                elif choice == '2':
                    print('\n🔄 Restarting registration process...')
                    return register()  
                
                elif choice == '3':
                    print('\n ❌ Registration cancelled ❌')
                    return
                else:
                    return '\n ⚠️ Invalid choice '
                
    conn.commit()
    conn.close()

#----------------------------------------- USER LOGIN ----------------------------------------------#

def login():
    conn = sqlite3.connect('emp.db')
    cursor = conn.cursor()
                
    print('\n\t\t----------------------------------------\n\t\t\t Welcome to Login Portal\n\t\t----------------------------------------')
    cursor.execute('''
                    SELECT * FROM User
                   ''')

    user = cursor.fetchall()

    if not user:
        print('\n ⚠️ No registered users available. Kindly complete registration before logging in.')
    else:
        username = get_username().lower().strip()

        cursor.execute('''
                        SELECT * FROM User WHERE username = ?
                    ''',(username,))

        user = cursor.fetchone()

        if not user:
            print('\n ⚠️ Incorrect username !!!')
        else:
            attempts = 0
            while attempts < 3:
                password = getpass.getpass('\nPassword : ')       
                if password == user[2]:
                    if user[3] == 1:
                        cursor.execute('''
                                       SELECT name FROM Manager WHERE user_id = ?
                                       ''',(user[0],))
                        name = cursor.fetchone()[0]
                        print(f'\n 👤 {name} 👤 Logged in successfully✅')
                    else:
                        cursor.execute('''
                                       SELECT name FROM Employee WHERE user_id = ?
                                       ''',(user[0],))
                        name = cursor.fetchone()[0]
                        print(f'\n 👤 {name} 👤 Logged in successfully✅')
                    return user
                else:
                    print('\n ⚠️ Oops! Password is incorrect. Please try again.')
                    attempts += 1
                
            if attempts == 3:
                print('\n ❌ ❌ ❌ Too many failed attempts !! Please try again later ')

    conn.close()

#-----------------------------------------------------  MANAGER CLASS   ---------------------------------------------------------------------------#

class Manager:
    def __init__(self,id):
        self.id = id
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            SELECT manager_id FROM Manager WHERE user_id = ?
                            ''',(self.id,))
        manager_id = self.cursor.fetchone()
        self.manager_id = manager_id[0]

    def view_employees(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()

        print('\n\t\t\t\t\t------------------------\n\t\t\t\t\t👥 EMPLOYEE DIRECTORY\n\t\t\t\t\t-----------------------')
        self.cursor.execute('''
                        SELECT emp_id,name,dept_id,job_title,date_of_joining,salary,contact,email FROM Employee 
                            ''')
        self.employees = self.cursor.fetchall()

        if not self.employees:
            print('\n No Employees to display ❌ Please register employees to view them here.')
        else:
            print(tabulate(self.employees,headers = ['Emp_ID','Name','Dept_ID','Designation','Joined Date','Salary','Contact','Mail-ID'],tablefmt = 'fancy_grid'))

    def add_emp(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()

        print('\n\t------------------------------------------\n\t 📋 Employee Enrollment Section \n\t------------------------------------------')
        
        username = get_username().lower()
        self.cursor.execute('''
                            SELECT * FROM User WHERE username = ?
                            ''',(username,))
        user = self.cursor.fetchone()
        if user:
            print('\n Username already Exists !!!')
            return
        else:
            password = get_password()
            role = 0
            while True:
                try:
                    name = input('\nFull Name : ').upper()
                    if not re.fullmatch(r'[A-Za-z ]+', name):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid Name !!! Use letters and spaces only\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    dept = input('\nDepartment Name : ').upper()
                    self.cursor.execute('''
                                SELECT dept_id FROM Department WHERE dept_name = ?
                            ''',(dept,))
                    dept_id = self.cursor.fetchone()
                    if not dept_id:
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid Department Name !!! Use letters only\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    title = input('\nDesignation : ').upper()
                    if not re.fullmatch(r'[A-Za-z ]+',title):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid job title !!! Use letters and spaces only\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    join_date = input('\nDate of joining(YYYY-MM-DD) : ')
                    datetime.datetime.strptime(join_date, r"%Y-%m-%d")                   
                except ValueError:
                    print('\n ⚠️ Invalid date format !!!\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    salary = int(input('\nSalary : '))
                except ValueError:
                    print('\n ⚠️ Invalid entry !!! Salary should be a number\n--------------------------------------------------------------------------------------------------- ')
                    continue
                try:
                    contact = input('\nContact Number : +91-')
                    if not re.fullmatch(r'\d{10}',contact):
                        raise numError
                except numError:
                    print('\n ⚠️ Invalid contact number !!! It should contain exactly 10 digits\n---------------------------------------------------------------------------------------------------')
                    continue
                try:
                    email = input('\nMail id : ').lower()
                    if not re.fullmatch( r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',email):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid mail id !!!\n---------------------------------------------------------------------------------------------------')
                    continue
                self.cursor.execute('''
                                    INSERT INTO User(username,password,role_id)
                                        VALUES (?,?,?)
                                    ''',(username,password,role))
                
                self.cursor.execute('''
                                    SELECT user_id FROM User WHERE username = ?
                                    ''',(username,))
                user_id = self.cursor.fetchone()
                self.cursor.execute('''
                                    INSERT INTO Employee(user_id,dept_id,manager_id,name,job_title,date_of_joining,salary,contact,email)
                                        VALUES (?,?,?,?,?,?,?,?,?)
                                    ''',(user_id[0],dept_id[0],self.manager_id,name,title,join_date,salary,contact,email))
                
                self.cursor.execute('''
                                    SELECT emp_id FROM Employee WHERE user_id = ?
                                    ''',(user_id[0],))
                emp_id = self.cursor.fetchone()[0]
                
                self.cursor.execute('''
                                    INSERT INTO Payroll(emp_id,basic_pay,allowance,deduction,overtime_pay,net_pay)
                                    VALUES (?,?,0,0,0,?)
                                    ''',(emp_id,salary,salary))
                self.cursor.execute('''
                                INSERT INTO Leave_Balance(emp_id,total_leave)
                                    VALUES (?,42)
                                ''', (emp_id, ))
                print('\n Employee Added successfully ✅ ')
                break
            self.conn.commit()
            self.conn.close()

    def update_emp(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()

        updating = True

        print('\n\t--------------------------------\n\t🔧 EMPLOYEE RECORD UPDATE \n\t--------------------------------')
        try:
            self.emp = int(input('\nEnter Employee ID: '))
        except ValueError:
            print('\n ⚠️ Invalid Entry !!!')
            return
        self.cursor.execute('''
                            SELECT * FROM Employee WHERE emp_id = ?
                            ''',(self.emp,))
        employee = self.cursor.fetchone()
        if not employee:
            print('\n 🚫 No such employee found. Please check the details and try again. ')
            return
       
        while updating:
            print('\n🔧 What would you like to update? 🔧')
            print('\n[1] 👤 Name\n[2] 🏢 Department\n[3] 💼 Designation\n[4] 📅 Date of Joining\n[5] 💰 Salary\n[6] 📞 Contact Number\n[7] 📧 Mail ID\n[8] 💾 Save and Exit\n[9] ❌ Discard and Exit')
            self.choice = input('\nPlease specify the field you would like to update : ')
            self.cursor.execute('''
                                SELECT name,dept_id,job_title,date_of_joining,salary,contact,email FROM Employee WHERE emp_id = ?
                                ''',(self.emp,))
            profile = self.cursor.fetchone()
            if not profile:
                print('\nProfile not found')
            if self.choice == '1':
                print(f'\nExisting name on profile : {profile[0]}')
                while True:
                    try:
                        name = input('\nEnter the updated Name : ').upper()
                        if not re.fullmatch(r'[A-Za-z ]+', name):
                            raise charError
                    except charError:
                        print('\n ⚠️ Invalid Name !!! Use letters and spaces only')
                        return
                    if name == profile[0]:
                        print('\n 🚫 No changes detected !!! Same name entered')
                        continue
                    self.cursor.execute('''
                                        UPDATE Employee SET name = ? WHERE emp_id = ? 
                                        ''',(name,self.emp))
                    print('\n ✅ Name updated successfully!')
                    break
            elif self.choice == '2':
                self.cursor.execute('''
                                SELECT dept_name FROM Department WHERE dept_id = ?
                            ''',(profile[1],))
                dept_name = self.cursor.fetchone()[0]
                print(f'\nExisting Department Name on Profile : {dept_name}')
                while True:
                    try:
                        dept = input('\nEnter the new department : ').upper()
                        self.cursor.execute('''
                                    SELECT dept_id FROM Department WHERE dept_name = ?
                                ''',(dept,))
                        dept_id = self.cursor.fetchone()
                        if not dept_id:
                            raise charError
                    except charError:
                        print('\n ⚠️ Invalid Department Name !!! ')
                        return
                    if dept == dept_name:
                        print('\n 🚫 No changes Detected !!! Same department entered.')
                        continue
                    self.cursor.execute('''
                                        SELECT dept_id FROM Department WHERE dept_name = ?        
                                        ''',(dept,))
                    dept_id = self.cursor.fetchone()
                    self.cursor.execute('''
                                        UPDATE Employee SET dept_id = ? WHERE emp_id = ? 
                                        ''',(dept_id[0],self.emp))
                    print('\n ✅ Department updated successfully!')
                    break
            elif self.choice == '3':
                print(f'\nExisting Designation on profile : {profile[2]}')
                while True:
                    try:
                        title = input('\nEnter the new designation : ').upper()
                        if not re.fullmatch(r'[A-Za-z ]+',title):
                            raise charError
                    except charError:
                        print('\n ⚠️ Invalid job title !!! ')
                        return
                    if title == profile[2]:
                        print('\n 🚫 No changes Detected !!! Same designation entered.')
                        continue
                    self.cursor.execute('''
                                        UPDATE Employee SET job_title = ? WHERE emp_id = ? 
                                        ''',(title,self.emp))
                    print('\n ✅ Designation updated successfully!')
                    break
            elif self.choice == '4':
                print(f'\nExisting Joined Date on profile : {profile[3]}')
                while True:
                    try:
                        join_date = input('\nDate of joining(YYYY-MM-DD) : ')
                        datetime.datetime.strptime(join_date, r"%Y-%m-%d")                   
                    except ValueError:
                        print('\n ⚠️ Invalid date format !!!')
                        return
                    if join_date == profile[3]:
                        print('\n 🚫 No changes Detected !!! Same date entered.')
                        continue
                    self.cursor.execute('''                                    
                                UPDATE Employee SET date_of_joining = ? WHERE emp_id = ? 
                                        ''',(join_date,self.emp))
                    print('\n ✅ Join date updated successfully!')
                    break
            elif self.choice == '5':
                print(f'\nExisting salary on profile : {profile[4]}')
                while True:
                    try:
                        salary = int(input('\nEnter the updated Salary : '))
                    except ValueError:
                        print('\n ⚠️ Invalid entry !!! Salary should be a number')
                        return
                    if salary == profile[0]:
                        print('\n 🚫 No changes Detected !!! Same salary entered.')
                        continue
                    self.cursor.execute('''
                                        
                                        UPDATE Employee SET salary = ? WHERE emp_id = ? 
                                        ''',(salary,self.emp))
                    print('\n ✅ Salary updated successfully!')
                    break
            elif self.choice == '6':
                print(f'\nExisting Contact number on profile : {profile[5]}')
                while True:
                    try:
                        contact = input('\nContact Number : +91-')
                        if not re.fullmatch(r'\d{10}',contact):
                            raise numError
                    except numError:
                        print('\n ⚠️ Invalid contact number !!! It should contain exactly 10 digits')
                        return
                    if profile[5] == int(contact):
                        print('\n 🚫 No changes Detected !!! Same contact number entered.')
                        continue
                    self.cursor.execute('''
                                        
                                        UPDATE Employee SET contact = ? WHERE emp_id = ? 
                                        ''',(contact,self.emp))
                    print('\n ✅ Contact number updated successfully!')
                    break
            elif self.choice == '7':
                print(f'\nExisting mail id on profile : {profile[6]}')
                while True:
                    try:
                        email = input('\nEnter the updated mail id : ').lower()
                        if not re.fullmatch( r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',email):
                            raise charError
                    except charError:
                        print('\n ⚠️ Invalid mail id !!!')
                        return
                    if email == profile[6]:
                        print('\n 🚫 No changes Detected !!! Same mail id entered.')
                        continue
                    self.cursor.execute('''
                                        
                                        UPDATE Employee SET email = ? WHERE emp_id = ? 
                                        ''',(email,self.emp))
                    print('\n ✅ Email updated successfully!')
                    break
            elif self.choice == '8':
                print('\n 💾 Changes saved successfully!')
                self.conn.commit()
                self.conn.close()
                break
            elif self.choice == '9':
                print('\n ❌ Updation cancelled. No changes made.')
                self.conn.close()
                break
            else:
                print('\n ⚠️ Invalid choice !!!')

    def delete_emp(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()

        print('\n\t-------------------------\n\t 🗑️ DELETE EMPLOYEE RECORD\n\t-------------------------')
        try:
            self.emp = int(input('\nEnter Employee ID : '))
        except ValueError:
            print('\n ⚠️ Invalid entry !!!')
            return
        self.cursor.execute('''
                            SELECT * FROM Employee WHERE emp_id = ?
                            ''',(self.emp,))
        employee = self.cursor.fetchone()
        if employee:
            print('\n⚠️  You are about to permanently delete this employee record.')
            confirm = input('Are you sure you want to proceed? (Y/N): ')
            if confirm == 'y' or confirm == 'Y':
                self.cursor.execute('''
                                    SELECT user_id FROM Employee WHERE emp_id = ?
                                    '''(self.emp))
                user_id = self.cursor.fetchone()[0]
                self.cursor.execute('''
                            DELETE FROM Employee WHERE emp_id = ?
                            ''',(self.emp,))
                self.cursor.execute('''
                            DELETE FROM User WHERE user_id = ?
                                    ''',(user_id,))
                self.conn.commit()
            else:
                print('\n ❌ Deletion cancelled. No changes made.')
                    
        else:
            print(' 🚫 No such employee found. Please check the details and try again.')

    def search_emp(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()

        while True:
            print('\n\t---------------------------------\n\t🔍 SEARCH EMPLOYEE RECORD\n\t---------------------------------')
            print('\n[1] 🆔 Search by ID\n[2] 👤 Search by Name\n[3] 🏛️ Search by Department\n[4] 🪪 Search by Designation\n[5] 📅 Search by Join Date\n[6] 📞 Search by Phone number\n[7] 🚪 Exit ')
            self.choice = input('Enter your option : ')
            
            if self.choice == '1':
                try:
                    self.emp = int(input('Enter employee id : '))
                except ValueError:
                    print('\n ⚠️ Invalid entry !!!')
                    return
                self.cursor.execute('''
                                    SELECT emp_id,name,dept_id,job_title,date_of_joining,salary,contact,email FROM Employee WHERE emp_id = ?                         
                                    ''',(self.emp,))
                self.employee = self.cursor.fetchone()
                if not self.employee:
                    print('\n ❌ No such employee found. Please check the details and try again.')
                else:
                    print('\n Search successful ✅')
                    print(tabulate([self.employee],headers = ['Emp_ID','Name','Dept_ID','Designation','Joined Date','Salary','Contact','Mail-ID'],tablefmt = 'grid'))
            elif self.choice == '2':
                try:
                    self.name = input('Enter the name of Employee : ').upper()
                except charError:
                    if not re.fullmatch(r'[A-Za-z ]+', self.name):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid Name !!! Use letters and spaces only')
                    return
                self.cursor.execute('''
                                    SELECT emp_id,name,dept_id,job_title,date_of_joining,salary,contact,email FROM Employee                         
                                    ''')
                self.employee = self.cursor.fetchall()
                result  = []
                for i in self.employee:
                    if self.name in i[1]:
                        result.append(i)
                if not result:
                    print('\n ❌ No such employee found. Please check the details and try again.')   
                else: 
                    print('\n Search successful ✅')
                    print(tabulate(result,headers = ['Emp_ID','Name','Dept_ID','Designation','Joined Date','Salary','Contact','Mail-ID'],tablefmt = 'grid'))
                
            elif self.choice == '3':
                try:
                    dept = input('\nDepartment Name : ').upper()
                    self.cursor.execute('''
                                SELECT dept_id FROM Department WHERE dept_name = ?
                            ''',(dept,))
                    dept_id = self.cursor.fetchone()
                    if not dept_id:
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid Department Name !!!') 
                    return
                self.cursor.execute('''
                                SELECT emp_id,name,dept_id,job_title,date_of_joining,salary,contact,email FROM Employee 
                                    ''')
                self.employee = self.cursor.fetchall()
                result  = []
                for i in self.employee:
                    if dept_id[0] == i[2]:
                        result.append(i)
                if not result:
                    print('\n ❌ No such employee found. Please check the details and try again.')   
                else: 
                    print('\n Search successful ✅')
                    print(tabulate(result,headers = ['Emp_ID','Name','Dept_ID','Designation','Joined Date','Salary','Contact','Mail-ID'],tablefmt = 'grid'))
            elif self.choice == '4':
                try:
                    title = input('\nDesignation : ').upper()
                    if not re.fullmatch(r'[A-Za-z ]+',title):
                        raise charError
                except charError:
                    print('\n ⚠️ Invalid job title !!! Use letters and spaces only\n---------------------------------------------------------------------------------------------------')
                    continue
                self.cursor.execute('''
                                SELECT emp_id,name,dept_id,job_title,date_of_joining,salary,contact,email FROM Employee 
                                    ''')
                self.employee = self.cursor.fetchall()
                result  = []
                for i in self.employee:
                    if title in i[3]:
                        result.append(i)
                if not result:
                    print('\n ❌ No such employee found. Please check the details and try again.')   
                else: 
                    print('\n Search successful ✅')
                    print(tabulate(result,headers = ['Emp_ID','Name','Dept_ID','Designation','Joined Date','Salary','Contact','Mail-ID'],tablefmt = 'grid'))
            elif self.choice == '5':
                try:
                    join_date = input('\nDate of joining(YYYY-MM-DD) : ')
                    datetime.datetime.strptime(join_date, r"%Y-%m-%d")                   
                except ValueError:
                    print('\n ⚠️ Invalid date format !!!')
                    continue
                self.cursor.execute('''
                                SELECT emp_id,name,dept_id,job_title,date_of_joining,salary,contact,email FROM Employee
                                    ''')
                self.employee = self.cursor.fetchall()
                result  = []
                for i in self.employee:
                    if join_date in i[4]:
                        result.append(i)
                if not result:
                    print('\n ❌ No such employee found. Please check the details and try again.')   
                else: 
                    print('\n Search successful ✅')
                    print(tabulate(result,headers = ['Emp_ID','Name','Dept_ID','Designation','Joined Date','Salary','Contact','Mail-ID'],tablefmt = 'grid'))
            elif self.choice == '6':
                try:
                    self.contact = input('\nEnter the phone number : +91')
                    
                    if not re.fullmatch(r'\d{10}',self.contact):
                        raise numError
                except numError:
                    print('\n ⚠️ Invalid contact number !!! It should contain exactly 10 digits')
                    return
                
                self.cursor.execute('''
                                    SELECT emp_id,name,dept_id,job_title,date_of_joining,salary,contact,email FROM Employee                        
                                    ''')
                self.employee = self.cursor.fetchall()
                result  = []
                for i in self.employee:
                    if int(self.contact) == i[6]:
                        result.append(i)
                if not result:
                    print('\n ❌ No such employee found. Please check the details and try again.')   
                else: 
                    print('\n Search successful ✅')
                    print(tabulate(result,headers = ['Emp_ID','Name','Dept_ID','Designation','Joined Date','Salary','Contact','Mail-ID'],tablefmt = 'grid'))
            elif self.choice =='7':
                print('\n Exiting Search Employee Portal')
                break
            else:
                print('\n ⚠️ Invalid choice!!!')

        self.conn.close()
    
    def view_attendance(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()
        while True:
            print('\n\t----------------------------------------\n\t📅 EMPLOYEE ATTENDANCE RECORDS 📅\n\t----------------------------------------')
            print('\n1. 📊 Today\'s Attendance Log\n2. 👥 Employee-wise Attendance Summary \n3. 🔙 Go Back ')
            choice = input('\n Enter your choice : ')
            if choice == '1':
                print('\n-------------------------------------------------------------')
                print('\n\t\t 📊 Today\'s Attendance Log ')
                print('\n-------------------------------------------------------------')
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                self.cursor.execute('''
                                    SELECT * FROM Attendance WHERE date = ?
                                    ''',(today,))
                data = self.cursor.fetchall()
                if not data:
                    print('\n ⛔ No attendance marked yet.')
                    continue
                print(tabulate(data,headers = ['Att_ID','Emp_ID','Date','Clock-in','Clock-out','Working_Hours','Overtime_Hours','Status'],tablefmt = 'grid'))
                continue

            elif choice == '2':
                print('\n-------------------------------------------------------------')
                print('\n\t\t 👥 EMPLOYEE WISE ATTENDANCE SUMMARY')
                print('\n-------------------------------------------------------------')
                try:
                    self.emp = int(input('Enter Employee ID to view attendance details : '))
                except ValueError:
                    print('\n ⚠️ Invalid entry !!!')
                    continue
                self.cursor.execute('''
                                    SELECT * FROM Employee WHERE emp_id = ?
                                    ''',(self.emp,))
                employee = self.cursor.fetchone()
                
                if not employee:
                    print('\n 🚫 No such user found. Please check the details and try again ')
                    return
                self.cursor.execute('''
                                    SELECT  date, clock_in, clock_out, working_hours, overtime_hours, status FROM Attendance WHERE emp_id = ?
                                    ''',(self.emp,))
                self.record = self.cursor.fetchall()
                
                print(tabulate(self.record,headers = ['Date','Clock_in','Clock_out','Work_Hours','Overtime_Hours','Status'],tablefmt = 'grid'))
                continue
            
            elif choice == '3':
                print('\n 🔚 Exiting....')
                break
            else:
                print('\n ⚠️ Invalid choice !!!')
                continue
            self.conn.close()
   
    def manage_leave(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()
        
        while True:
            print('\n\t----------------------------------------\n\t 🗂️ LEAVE MANAGEMENT PORTAL 🗂️\n\t----------------------------------------')
            print('\n[1] 📄 View leave records \n[2] 🗂️  Manage Leave Requests \n[3] 🚪 Exit ')
            self.choice = input('\nEnter your choice : ')
            
            if self.choice == '1':
                print('\n\t---------------------------------------------\n\t\t📄 EMPLOYEE LEAVE REQUESTS 📄\n\t---------------------------------------------')
                print('\n[1] 📋 View all requests\n[2] ⏳ View Pending requests\n[3] ✅ View Approved requests\n[4] ❌ View rejected requests\n[5] 🔙 Go back')
                self.ch = input('Select an action : ')
                
                if self.ch == '1':
                    self.cursor.execute('''
                                SELECT * FROM Leave_Record ''')
                    self.record = self.cursor.fetchall()
                    if not self.record:
                        print('\n ❌ No leave records found')
                    else:
                        print('\n-------------------------------------------------------------------------------------------------------')
                        print('\nLeave_id  Emp_id \t Leave_Type \t From \t\t To \t\t Duration \t Status ')
                        print('\n-------------------------------------------------------------------------------------------------------')
                        for i in self.record:
                            if i[2] is None:
                                continue
                            print(f'\n{i[0]}  \t {i[1]} \t\t {i[2]} \t {i[3]} \t {i[4]} \t  {i[5]} \t\t {i[7]}')
            
                elif self.ch =='2':
                    self.cursor.execute('''
                        SELECT * FROM Leave_Record WHERE status = 'PENDING'
                                ''')
                    self.record = self.cursor.fetchall()
                    if not self.record:
                        print('\n ❌ No active leave records found')
                    else:
                        print('\n-------------------------------------------------------------------------------------------------------')
                        print('\nLeave_id  Emp_id \t Leave_Type \t From \t\t To \t\t Duration \t Status ')
                        print('\n-------------------------------------------------------------------------------------------------------')
                        for i in self.record:
                            print(f'\n{i[0]}  \t {i[1]} \t\t {i[2]} \t {i[3]} \t {i[4]} \t  {i[5]} \t\t {i[7]}')
            
                elif self.ch =='3':    
                    self.cursor.execute('''
                        SELECT * FROM Leave_Record WHERE status = 'APPROVED'
                                ''')
                    self.record = self.cursor.fetchall()
                    if not self.record:
                        print('\n ❌ No active leave records found')
                    else:
                        print('\n-------------------------------------------------------------------------------------------------------\nLeave_id   Emp_id \t Leave_Type \t\t From \t\t To \t Duration \t Status \n-------------------------------------------------------------------------------------------------------')
                        for i in self.record:
                            print(f'\n{i[0]}  \t {i[1]} \t\t {i[2]} \t {i[3]} \t {i[4]} \t  {i[5]} \t\t {i[7]}')
            
                elif self.ch =='4':    
                    self.cursor.execute('''
                        SELECT * FROM Leave_Record WHERE status = 'REJECTED'
                                ''')
                    self.record = self.cursor.fetchall()
                    if not self.record:
                        print('\n ❌ No active leave records found')
                    else:
                        print('\n-------------------------------------------------------------------------------------------------------\nLeave_id   Emp_id \t Leave_Type \t\t From \t\t To \t Duration \t Status \n-------------------------------------------------------------------------------------------------------')
                        for i in self.record:
                            print(f'\n{i[0]}  \t {i[1]} \t\t {i[2]} \t {i[3]} \t {i[4]} \t  {i[5]} \t\t {i[7]}')
                elif self.ch == '5':
                    print('\n Going back to Leave management Portal ....')
                else:
                    print('\n ⚠️ Invalid choice !!!')
            elif self.choice == '2':
                print('\n\t----------------------------------------\n\t\t 🗂️  MANAGE LEAVE REQUESTS 🗂️ \n\t----------------------------------------')
                self.cursor.execute('''
                        SELECT * FROM Leave_Record WHERE status = 'PENDING'
                                ''')
                self.record = self.cursor.fetchall()
                if not self.record:
                    print('\n ❌ No active leave records found')
                else:
                    for i in self.record:
                        print('\n-------------------------------------------------------------------------------------------------------\nLeave_id   Emp_id \t Leave_Type \t\t From \t\t To \t Duration \t Status \n-------------------------------------------------------------------------------------------------------')
                        print(f'\n{i[0]}  \t {i[1]} \t\t {i[2]} \t {i[3]} \t {i[4]} \t  {i[5]} \t\t {i[7]}')
                        print('\n1. ✅ Approve Leave\n2. ❌ Reject Leave\n3. ↩️ Go Back')
                        self.action = input('\n Select an action : ')
                        if self.action == '1':
                            self.cursor.execute('''
                                                UPDATE Leave_Record SET status = 'APPROVED' WHERE leave_id = ?
                                                ''',(i[0],))
                            print('\n 📝 Leave request Approved ✅')
                            self.conn.commit()
                        elif self.action == '2':
                            self.cursor.execute('''
                                                UPDATE Leave_Record SET status = 'REJECTED' WHERE leave_id = ?
                                                ''',(i[0],))
                            print('\n 📝 Leave request Rejected ✅')
                            self.conn.commit()
                        elif self.action == '3':
                            print('\n Going back to Leave management Portal ....')
                            break
            elif self.choice == '3':
                print('\n Exiting Leave management portal...')
                break
            else:
                print('\n ⚠️ Invalid choice!!!') 

    def manage_salary(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()        
        try:
            self.emp = int(input('Enter Employee ID to view salary details : '))
        except ValueError:
            print('\n ⚠️ Invalid entry !!!')
            return
        self.cursor.execute('''
                            SELECT * FROM Employee WHERE emp_id = ?
                            ''',(self.emp,))
        employee = self.cursor.fetchone()
        if not employee:
            print('\n 🚫 No such user found. Please check the details and try again ')
            return
        while True:
            print('\n\t--------------------------------------------------\n\t\t 💰 MANAGE EMPLOYEE SALARY \n\t--------------------------------------------------')
           
            print('\n[1] 💼 View Employee salary\n[2] 📈 Apply Allowance \n[3] 📉 Apply deduction \n[4] 🕒 Overtime pay Entry \n[5] 🗂️ View Salary History\n[6] 🔙 Back')
            ch = input('\nSelect an option : ')
            if ch == '1':
           
                self.cursor.execute('''
                                SELECT * FROM Payroll WHERE emp_id = ?
                                    ''',(self.emp,))
                salary_record = self.cursor.fetchone()
                self.cursor.execute('''
                                SELECT dept_id,name,job_title FROM Employee WHERE emp_id = ?
                                    ''',(self.emp,))
                emp = self.cursor.fetchone()
                self.cursor.execute('''
                                SELECT dept_name FROM Department WHERE dept_id = ?
                                    ''',(emp[0],))
                dept = self.cursor.fetchone()

                net_salary = salary_record[2] + salary_record[3] - salary_record[4] + salary_record[5]

                self.cursor.execute('''
                                    UPDATE Payroll SET net_pay = ? WHERE emp_id = ? 
                                    ''',(net_salary,self.emp))
                self.conn.commit()
               
                print('\n-------------------------------------------------------')
                print('\n\t\t💼 VIEW EMPLOYEE SALARY')
                print('\n-------------------------------------------------------')
                
                print(f'\nPayroll ID       : {salary_record[0]}')
                print(f'\nEmployee ID      : {salary_record[1]}')
                print(f'\nEmployee Name    : {emp[1]}')
                print(f'\nDepartment       : {dept[0]}')
                print(f'\nDesignation      : {emp[2]}')
                print('\n-------------------------------------------------------')
                print(f'\nBasic Salary     : ₹ {salary_record[2]}')               
                print(f'\nAllowances       : ₹ {salary_record[3]}')
                print(f'\nDeduction        : ₹ {salary_record[4]}')
                print(f'\nOvertime Pay     : ₹ {salary_record[5]}')
                print('\n-------------------------------------------------------')
                print(f'\nNet Salary (Payable) : ₹ {net_salary}')
                print('\n-------------------------------------------------------')
                continue
            elif ch == '2':
                print('\n\t-----------------------\n\t💰 APPLY ALLOWANCE  \n\t-----------------------')
             
                self.cursor.execute('''
                                SELECT basic_pay FROM Payroll WHERE emp_id = ? 
                                    ''',(self.emp,))
                salary = self.cursor.fetchone()[0]
                allowance = salary * 0.1
                self.cursor.execute('''
                                    UPDATE Payroll SET allowance = ? WHERE emp_id = ? 
                                    ''',(allowance,self.emp))
                self.conn.commit()
                print(f'\n 🎉 Allowance ₹ {allowance} applied Successfully')
                continue
            elif ch == '3':
                
                print('\n\t----------------------------\n\t📉 APPLY DEDUCTION\n\t----------------------------')
  
                self.cursor.execute('''
                                SELECT deduction FROM Payroll WHERE emp_id = ?
                                    ''',(self.emp,))
                deduction = self.cursor.fetchone()[0]
                if deduction == 0:
                    print('\n🟢 Salary processed without deductions.')
                else:
                    print(f'\n 📉 Salary deduction ₹ {deduction} applied. ')
                continue
            elif ch == '4':
                print('\n----------------------------\n🕒 OVERTIME PAY ENTRY \n----------------------------')
                
                self.cursor.execute('''
                                SELECT overtime_hours FROM Attendance WHERE emp_id = ? 
                                    ''',(self.emp,))
                overtime = self.cursor.fetchone()
                if not overtime:
                    print('\n ❌ Salary processed without overtime pay. No overtime hours were recorded for this employee.')
                    return
                self.cursor.execute('''
                                    SELECT basic_pay,overtime_pay FROM Payroll WHERE emp_id = ?
                                    ''',(self.emp,))
                result = self.cursor.fetchone()
                salary = result[0]
                overtime_rate = salary / 25 / 8
                overtime_pay = result[1] + overtime[0] * overtime_rate
                self.cursor.execute('''
                                    UPDATE Payroll SET overtime_pay = ? WHERE emp_id = ? 
                                    ''',(overtime_pay,self.emp))
                self.conn.commit()
                if overtime_pay > 0:
                    print('\n 🎉 Overtime Pay Applied')
                    print(f'🕒 Overtime Hours : {overtime[0]}')
                    print(f'💰 Overtime Rate  : {overtime_rate:.2f}')
                    print(f'💵 New OT Amount  : {overtime_pay:.2f}')
                else:
                    print('\n ⚠️ Overtime hours recorded are zero. No overtime pay added.')
                continue
            elif ch == '5':
                print('\n\t-----------------------------------\n\t\t 🗂️ View Salary History \n\t-----------------------------------')
                self.cursor.execute('''
                                SELECT * FROM Payroll WHERE emp_id = ? 
                                    ''',(self.emp,))
                salary_record = self.cursor.fetchall()
                
                print('\n-------------------------------------------------------------------------------------------------')
                print('\n Payroll_ID  Emp_ID  Basic_pay  Allowance  Deduction  Overtime_pay  Net_Salary ')
                print('\n-------------------------------------------------------------------------------------------------')
                for i in salary_record:
                        print(f'\n   {i[0]}\t\t{i[1]} \t {i[2]} \t {i[3]} \t\t {i[4]}\t\t{i[5]} \t {i[6]} ')
                continue
            elif ch == '6':
                print('\n Exiting 👋🏻👋🏻👋🏻')
                break
            else:
                print('\n ⚠️ Invalid choice !!!')


#--------------------------------------------------   EMPLOYEE CLASS   -------------------------------------------------#

class Employee:
    def __init__(self,id):
        self.id = id
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            SELECT emp_id FROM Employee WHERE user_id = ?
                            ''',(self.id,))
        emp_id = self.cursor.fetchone()
        self.emp_id = emp_id[0]
        self.conn.close()

    def change_password(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()
        print('\n\t--------------------------------------------------\n\t 🔐 CHANGE PASSWORD 🔐\n\t--------------------------------------------------')
        old_pw = getpass.getpass('\nEnter old password : ')
        self.cursor.execute('''
                            SELECT password from User WHERE user_id = ?
                            ''',(self.id,))
        pw = self.cursor.fetchone()
        if pw[0] != old_pw:
            print('\n ⚠️ Incorrect old password !!! Please try again Later...')
            return
        while True:
            new_pw = getpass.getpass('\nEnter new password : ')
            if new_pw == old_pw:
                print('\n 🚫 New password cannot be same as the old password ')
                continue
            elif len(new_pw) < 6:
                print("⚠️ Password too short! Must be at least 6 characters.")
                continue
            elif not re.search(r"[A-Z]", new_pw):
                print("⚠️ Password must contain at least one uppercase letter.")
                continue
            elif not re.search(r"[a-z]", new_pw):
                print("⚠️ Password must contain at least one lowercase letter.")
                continue
            elif not re.search(r"[0-9]", new_pw):
                print("⚠️ Password must contain at least one digit.")
                continue
            elif not re.search(r"[@#$%^&*-_!]", new_pw):
                print("⚠️ Password must contain at least one special character .")
                continue
            else:
                confirm_pw = getpass.getpass('\nConfirm password : ')
                if new_pw != confirm_pw:
                    print('\n ⚠️ Passwords donot match. Please try again.')
                    continue
                else:
                    self.conn.execute('''
                                    UPDATE User SET password = ? WHERE user_id = ?
                                      ''',(new_pw,self.id))
                    self.conn.commit()
                    self.conn.close()
                    print('\n ✔️ Password Updated Successfully. Please log in again to continue.')
                    break
        login()

    def view_profile(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            SELECT name,dept_id,job_title,date_of_joining,salary,contact,email FROM Employee WHERE emp_id = ?
                            ''',(self.emp_id,))
        profile = self.cursor.fetchone()
        self.cursor.execute('''
                            SELECT dept_name FROM Department WHERE dept_id = ?
                            ''',(profile[1],))
        dept = self.cursor.fetchone()
        print('\n\t-------------------------\n\t 👤 EMPLOYEE PROFILE 👤\n\t-------------------------')   
        print(f'👤 Name            : {profile[0]}')
        print(f'🏢 Department      : {dept[0]}')
        print(f'🧑‍💼 Designation   : {profile[2]}')
        print(f'📅 Date of Joining : {profile[3]}')
        print(f'💰 Salary          : ₹{profile[4]}')
        print(f'📞 Contact No.     : +91-{profile[5]}')
        print(f'📧 Email ID        : {profile[6]}')
        self.conn.close()

    def edit_profile(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()
        updating = True
        
        while updating:
            print('\n\t------------------------\n\t 🧾 Edit Your Details\n\t------------------------')
            print('\n[1] 👤 Name\n[2] 🏢 Department\n[3] 💼 Designation\n[4] 📅 Date of Joining\n[5] 📞 Contact Number\n[6] 📧 Mail ID\n[7] 💾 Save and Exit\n[8] ❌ Discard and Exit')
            choice = input('\nPlease specify the field you would like to update : ')
            self.cursor.execute('''
                                SELECT name,dept_id,job_title,date_of_joining,contact,email FROM Employee WHERE user_id = ?
                                ''',(self.id,))
            profile = self.cursor.fetchone()
            
            if choice == '1':
                print(f'\nExisting name on profile : {profile[0]}')
                while True:                    
                    try:
                        name = input('\nEnter new Name : ').upper()
                        if not re.fullmatch(r'[A-Za-z ]+', name):
                            raise charError
                    except charError:
                        print('\n ⚠️ Invalid Name !!! Use letters and spaces only')
                        continue
                    if name == profile[0]:
                        print('\n 🚫 No changes detected !!! You entered the same name.')
                        continue
                    self.cursor.execute('''
                                        UPDATE Employee SET name = ? WHERE emp_id = ? 
                                        ''',(name,self.emp_id))
                    print('\n ✅ Name updated successfully!')
                    break
            elif choice == '2':
                self.cursor.execute('''
                                    SELECT dept_name FROM Department WHERE dept_id = ?
                                ''',(profile[1],))
                dept_name = self.cursor.fetchone()[0]
                print(f'\nExisting Department Name on Profile : {dept_name}')
                while True:
                    try:
                        dept = input('\nEnter the new department : ').upper()
                        self.cursor.execute('''
                                    SELECT dept_id FROM Department WHERE dept_name = ?
                                ''',(dept,))
                        dept_id = self.cursor.fetchone()
                        if not dept_id:
                            raise charError
                    except charError:
                        print('\n ⚠️ Invalid Department Name !!! ')
                        continue
                    if dept == dept_name:
                        print('\n 🚫 No changes detected !!! You entered the same department')
                        continue
                    self.cursor.execute('''
                                        SELECT dept_id FROM Department WHERE dept_name = ?        
                                        ''',(dept,))
                    dept_id = self.cursor.fetchone()
                    self.cursor.execute('''
                                        UPDATE Employee SET dept_id = ? WHERE emp_id = ? 
                                        ''',(dept_id[0],self.emp_id))
                    print('\n ✅ Department updated successfully!')
                    break
            elif choice == '3':
                print(f'\nExisting Designation on profile : {profile[2]}')
                while True:
                    try:
                        title = input('\nEnter the new designation : ').upper()
                        if not re.fullmatch(r'[A-Za-z ]+',title):
                            raise charError
                    except charError:
                        print('\n ⚠️ Invalid job title !!! ')
                        continue
                    if title == profile[2]:
                        print('\n 🚫 No changes detected !!! You entered the same job title')
                        continue
                    self.cursor.execute('''
                                        UPDATE Employee SET job_title = ? WHERE emp_id = ? 
                                        ''',(title,self.emp_id))
                    print('\n ✅ Designation updated successfully!')
                    break
            elif choice == '4':
                print(f'\nExisting Joined Date on profile : {profile[3]}')
                while True:
                    try:
                        join_date = input('\nDate of joining(YYYY-MM-DD) : ')
                        datetime.datetime.strptime(join_date, r"%Y-%m-%d")                   
                    except ValueError:
                        print('\n ⚠️ Invalid date format !!!')
                        continue
                    if join_date == profile[3]:
                        print('\n 🚫 No changes detected !!! You entered the same date')
                        continue
                    self.cursor.execute('''                                    
                                UPDATE Employee SET date_of_joining = ? WHERE emp_id = ? 
                                        ''',(join_date,self.emp_id))
                    print('\n ✅ Join date updated successfully!')
                    break
            elif choice == '5':
                print(f'\nExisting Contact number on profile : +91-{profile[4]}')
                while True:
                    try:
                        contact = input('\nNew Contact Number : +91-')
                        if not re.fullmatch(r'\d{10}',contact):
                            raise numError
                    except numError:
                        print('\n ⚠️ Invalid contact number !!! It should contain exactly 10 digits')
                        continue
                   
                    if profile[5] == int(contact):
                        print('\n 🚫 No changes detected !!! You entered the same contact number')
                        continue
                    self.cursor.execute('''
                                        UPDATE Employee SET contact = ? WHERE emp_id = ? 
                                        ''',(contact,self.emp_id))
                    print('\n ✅ Contact number updated successfully!')
                    break
            elif choice == '6':
                print(f'\nExisting mail id on profile : {profile[5]}')
                while True:
                    try:
                        email = input('\nEnter the new mail id : ').lower()
                        if not re.fullmatch( r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',email):
                            raise charError
                    except charError:
                        print('\n ⚠️ Invalid mail id !!!')
                        continue
                    if email == profile[5]:
                        print('\n 🚫 No changes detected !!! You entered the same mail-id')
                        continue
                    self.cursor.execute('''
                                        
                                        UPDATE Employee SET email = ? WHERE emp_id = ? 
                                        ''',(email,self.emp_id))
                    print('\n ✅ Email updated successfully!')
                    break
            elif choice == '7':
                print('\n 💾 Changes saved successfully!')
                self.conn.commit()
                updating = False
                break
            elif choice == '8':
                print('\n ❌ Changes discarded. No updates applied.')
                updating = False
                break
            else:
                print('\n ⚠️ Invalid choice !!!')
                break
       
        self.conn.close()
               
    
    def clock_in(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()

        print('\n\t    ⏰ PUNCH IN  ')
        
        date = datetime.datetime.now().strftime(r'%Y-%m-%d')
        time_in = datetime.datetime.now().strftime(r'%H:%M')
        
        status = 'PRESENT'
        self.cursor.execute('''
                            SELECT clock_in FROM Attendance WHERE emp_id = ? and date = ?
                            ''',(self.emp_id,date))
        marked = self.cursor.fetchone()
        if marked:
            print('\n ⚠️  You have already punched in today.')
            self.conn.close()
            return
        self.cursor.execute('''
                            INSERT INTO Attendance(emp_id,date,clock_in,status)
                                VALUES (?,?,?,?)
                            ''',(self.emp_id,date,time_in,status))
        print(f'\n---------------------------------------------\n\tDATE : {date} \n ✔️ PUNCH-IN SUCCESSFUL !!!\n\tTIME : {time_in}\n---------------------------------------------')
        self.conn.commit()
        self.conn.close()

    def clock_out(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()
        print('\n\t-----------------------')
        print('\n\t   🕣 PUNCH - OUT ')
        print('\n\t-----------------------')
        date = datetime.datetime.now().strftime(r'%Y-%m-%d')
        time_out = datetime.datetime.now().strftime(r'%H:%M')

        self.cursor.execute('''
                            SELECT clock_in FROM Attendance WHERE emp_id = ? AND date = ?
                            ''',(self.emp_id,date))
        punched_in = self.cursor.fetchone()

        if not punched_in:
            print('\n ⚠️  You haven\'t punched in yet !!! Please punch in first.' )
            return
        
        time_in = punched_in[0]
        t_in = datetime.datetime.strptime(time_in, "%H:%M")
        t_out = datetime.datetime.strptime(time_out, "%H:%M")
        work_hours = 0
        overtime = 0
        self.cursor.execute('''
                           SELECT clock_out FROM Attendance WHERE emp_id = ? AND date = ? 
                            ''',(self.emp_id,date))
        punched_out = self.cursor.fetchone()
    
        if punched_out and punched_out[0] is not None:
            print('\n ⚠️  You have already punch out for today .')
            return
        
        work_hours += (t_out - t_in).seconds / 3600 
        if work_hours > 8 :
            status = 'OVERTIME'
            overtime += work_hours - 8
     
        elif work_hours > 6 and work_hours <= 8:
            status = 'PRESENT'
        elif work_hours >= 4 :
            status = 'HALF DAY'
        else :
            status = 'ABSENT'
        self.cursor.execute('''
                            SELECT total_leave
                                FROM Leave_Balance WHERE emp_id = ?     
                            ''',(self.emp_id,))
        balance = self.cursor.fetchone()
    
        leave_balance = balance[0]
        self.cursor.execute('''
                            SELECT basic_pay,deduction FROM Payroll WHERE emp_id = ?
                            ''',(self.emp_id,))
        salary,deduction = self.cursor.fetchone()
        if status == 'ABSENT':
            print('\n ⚠️  Working hours are insufficient. You will be marked as Absent.')
            confirm = input('Are you sure you want to punch out? (Y/N): ').upper()
            if confirm != 'Y':
                print('\n 🚫 Punch out Aborted ')
                return
            else:
                if leave_balance != 0:
                    leave_balance -= 1
                else: 
                    deduction += (salary / 25) 
 
        elif status == 'HALF DAY':
            print('\n ⚠️  You have not completed full-day hours. Punching out now will mark you as Half Day.')
            confirm = input('Do you still want to continue? (Y/N): ').upper()
            if confirm != 'Y':
                print('\n 🚫 Punch out Aborted ')
                return
            else:
                if leave_balance != 0:
                    leave_balance -= 0.5
                else:
                    deduction += (salary / 25) * 0.5

        self.cursor.execute('''
                            INSERT INTO Payroll(emp_id,deduction,basic_pay)
                                VALUES (?,?,?)
                         ''',(self.emp_id,deduction,salary))
        self.cursor.execute('''
                            UPDATE Leave_Balance SET total_leave = ? WHERE emp_id = ?
                           ''', (leave_balance,self.emp_id))
        self.cursor.execute('''
                            UPDATE Attendance SET clock_out = ?,working_hours = ?, overtime_hours = ?,status = ? WHERE emp_id = ? AND date = ?
                            ''',(time_out,work_hours,overtime,status,self.emp_id,date))
        
        print('\n----------------------------------------------------------------')
        print(f'\n\tDATE : {date} \n ✔️ PUNCH-OUT SUCCESSFUL !!!\n\tTIME : {time_out}')
        print('\n----------------------------------------------------------------')
        self.conn.commit()
        self.conn.close()

    def apply_leave(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
                            SELECT  total_leave FROM Leave_Balance WHERE emp_id = ?
                            ''', (self.emp_id,))
        balance = self.cursor.fetchone()
   
        if balance:
            leave_balance = balance[0]
            print(leave_balance)
            paid_leave = 0  

            print('\n\t---------------------------------')
            print('\t  📝 LEAVE APPLICATION PORTAL')
            print('\t---------------------------------')
            print('\nPlease fill out the leave application form below by providing all the required details accurately.')
            print('\n----------------------------------------------------------------------------------------------------')
            print('\n\t 📝 LEAVE APPLICATION FORM \n\t-----------------------------')
            print('\n[1] Casual Leave \n[2] Sick Leave \n[3] Earned Leave \n[4] Paid Leave')

            ch = input('\nPlease Select Leave type : ')
            leave_types = {'1': 'CASUAL LEAVE', '2': 'SICK LEAVE', '3': 'EARNED LEAVE', '4': 'PAID LEAVE'}
            if ch not in leave_types:
                print('\n ⚠️ Invalid Leave Type !!!')
                self.conn.close()
                return
            leave_type = leave_types[ch]
            status = 'PENDING'

            try:
                today = str(datetime.date.today())
                today = datetime.datetime.strptime(today, "%Y-%m-%d")
                start_date = input('\nLeave Start Date (YYYY-MM-DD): ')
                start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                if start_dt < today:
                    print('\n ⚠️ Leave application failed: The selected date cannot be earlier than the current date.')
                    self.conn.close()
                    return
                end_date = input('Leave End Date (YYYY-MM-DD): ')
                end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                if end_dt < start_dt:
                    print("\n ⚠️ Leave application failed: End date cannot be earlier than the start date")
                    self.conn.close()
                    return
            except ValueError:
                print('\n ⚠️ Invalid Date format !!! Use YYYY-MM-DD')
                self.conn.close()
                return

            leave_days = (end_dt - start_dt).days + 1
            print(f'Leave Duration: {leave_days} day(s)')

            if leave_days > leave_balance:
                print('\n ⚠️ Insufficient leave balance! Additional days will be processed as paid leave.')
                confirm = input('Do you wish to proceed? (Y/N): ')
                if confirm.upper() != 'Y':
                    print('\n ❌ Leave request cancelled')
                    self.conn.close()
                    return
                
                paid_leave = leave_days - leave_balance
                leave_type = 'PAID LEAVE'
                new_balance = 0
            new_balance = max(0, leave_balance - leave_days)
            self.cursor.execute('''
                            UPDATE Leave_Balance SET total_leave = ? WHERE emp_id = ?
                                ''', (new_balance, self.emp_id))
        else:
            print("\n ⚠️ Leave balance not found for this employee!\nIf you continue, the requested leave may be treated as paid leave and could lead to salary deductions.")
            confirm = input('\nWould you like to proceed? (Y/N): ')
            if confirm.upper() != 'Y':
                print('\n ❌ Leave request cancelled')
                self.conn.close()
                return
            else:
                print('\n\t---------------------------------')
            print('\t  📝 LEAVE APPLICATION PORTAL')
            print('\t---------------------------------')
            print('\nPlease fill out the leave application form below by providing all the required details accurately.')
            print('\n----------------------------------------------------------------------------------------------------')
            print('\n\t 📝 LEAVE APPLICATION FORM \n\t-----------------------------')
            print('\n[1] Casual Leave \n[2] Sick Leave \n[3] Earned Leave \n[4] Paid Leave')

            print('\nLeave type : PAID LEAVE')
            leave_type = 'PAID LEAVE'
            status = 'PENDING'
            try:
                today = str(datetime.date.today())
                today = datetime.datetime.strptime(today, "%Y-%m-%d")
                start_date = input('\nLeave Start Date (YYYY-MM-DD): ')
                start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                if start_dt < today:
                    print('\n ⚠️ Leave application failed: The selected date cannot be earlier than the current date.')
                    self.conn.close()
                    return
                end_date = input('Leave End Date (YYYY-MM-DD): ')
                end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                if end_dt < start_dt:
                    print("\n ⚠️ Leave application failed: End date cannot be earlier than the start date")
                    self.conn.close()
                    return
            except ValueError:
                print('\n ⚠️ Invalid Date format !!! Use YYYY-MM-DD')
                self.conn.close()
                return

            leave_days = (end_dt - start_dt).days + 1
            print(f'Leave Duration: {leave_days} day(s)')
            paid_leave = leave_days
        self.cursor.execute('''
            INSERT INTO Leave_Record(emp_id,leave_type,start_date,end_date,leave_duration, status)
                VALUES (?,?,?,?,?,?)
        ''', (self.emp_id,leave_type, start_date, end_date, leave_days, status))

        if paid_leave > 0:
            self.cursor.execute('''
                                SELECT basic_pay, deduction FROM Payroll WHERE emp_id = ?
                                ''', (self.emp_id,))
            result = self.cursor.fetchone()
            if result:
                salary, deduction = result
                deduction += (salary / 25) * paid_leave  
                self.cursor.execute('''
                    UPDATE Payroll SET deduction = ? WHERE emp_id = ?
                ''', (deduction, self.emp_id))
            new_balance = 0
        self.conn.commit()
        self.conn.close()
        print('\n Leave request send 📩')
        if paid_leave > 0:
            print(f'⚠️ {paid_leave} day(s) will be deducted from salary as paid leave.')

    def view_leave_status(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()

        total = 42
       
        self.cursor.execute('''
                            SELECT leave_id,start_date,end_date,leave_type,status FROM Leave_Record WHERE emp_id = ?
                            ''',(self.emp_id,))
        applied = self.cursor.fetchall()
        self.cursor.execute('''
                            SELECT * FROM Leave_Record WHERE emp_id = ? AND status = 'PENDING'
                            ''',(self.emp_id,))
        pending = self.cursor.fetchall()
        self.cursor.execute('''
                            SELECT * FROM Leave_Record WHERE emp_id = ? AND status = 'APPROVED'
                            ''',(self.emp_id,))
        approved = self.cursor.fetchall()
        leave_taken = 0
        for i in approved:
            leave_taken += i[5]
        self.cursor.execute('''
                            SELECT * FROM Leave_Record WHERE emp_id = ? AND status = 'REJECTED'
                            ''',(self.emp_id,))
        rejected = self.cursor.fetchall()
        date = datetime.datetime.now().strftime(r'%Y-%m-%d')
        
        remaining = total - leave_taken
        print('\n\t---------------------------------------------')
        print('\n\t\t📝🌟 LEAVE STATUS DASHBOARD')
        print('\n\t---------------------------------------------')
        print(f'\n\t 👤 Employee ID   : {self.emp_id}')
        print(f'\n\t 📅 As of Date    : {date}')
        print('\n\t---------------------------------------------')
        print(f'\n\t 🌴 Total Leave       : {total}')
        print(f'\n\t 🟢 Leave Taken       : {leave_taken}')
        print(f'\n\t ⚪ Remaining Leave   : {remaining}')
        print(f'\n\t ⏳ Pending Leave     : {len(pending)}')
        print(f'\n\t ✅ Approved Leave    : {len(approved)}')
        print(f'\n\t ❌ Rejected Leave    : {len(rejected)}')
        print('\n\t---------------------------------------------')
        if applied:
            print(f'\n\t 🗓️  Applied Leave Records:')
            print('\n\t---------------------------------------------------------------------------------------')
            print('\n\t LEAVE ID \t FROM \t\t TO \t\t TYPE \t\t STATUS ')
            print('\n\t---------------------------------------------------------------------------------------')
            for i in applied:
                if i[1] is None:
                    continue
                print(f'\n\t {i[0]} \t\t {i[1]} \t {i[2]} \t {i[3]} \t {i[4]}')
            print('\n\t---------------------------------------------------------------------------------------')

        self.conn.close()

    def view_salary_details(self):
        self.conn = sqlite3.connect('emp.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
                                SELECT * FROM Payroll WHERE emp_id = ?
                                    ''',(self.emp_id,))
        salary_record = self.cursor.fetchone()
        self.cursor.execute('''
                        SELECT dept_id,name,job_title FROM Employee WHERE emp_id = ?
                            ''',(self.emp_id,))
        emp = self.cursor.fetchone()
        self.cursor.execute('''
                        SELECT dept_name FROM Department WHERE dept_id = ?
                          ''',(emp[0],))
        dept = self.cursor.fetchone()

        net_salary = salary_record[2] + salary_record[3] - salary_record[4] + salary_record[5]

        self.cursor.execute('''
                      UPDATE Payroll SET net_pay = ? WHERE emp_id = ? 
                         ''',(net_salary,self.emp_id))
        self.conn.commit()
        self.conn.close()      
        print('\n-------------------------------------------------------')
        print('\n\t\t💰💰💰 SALARY SLIP 💰💰💰')
        print('\n-------------------------------------------------------')
                
        print(f'\nPayroll ID       : {salary_record[0]}')
        print(f'\nEmployee ID      : {salary_record[1]}')
        print(f'\nEmployee Name    : {emp[1]}')
        print(f'\nDepartment       : {dept[0]}')
        print(f'\nDesignation      : {emp[2]}')
        print('\n-------------------------------------------------------')
        print(f'\nBasic Salary     : ₹ {salary_record[2]}')               
        print(f'\nAllowances       : ₹ {salary_record[3]}')
        print(f'\nDeduction        : ₹ {salary_record[4]}')
        print(f'\nOvertime Pay     : ₹ {salary_record[5]}')
        print('\n-------------------------------------------------------')
        print(f'\nNet Salary (Payable) : ₹ {net_salary}')
        print('\n-------------------------------------------------------')


#------------------------------------------------------ MAIN MENU ----------------------------------------------------------------#

def main():
    setup_db()

    while True:
        print('\n=========================================================================================')
        print('\n\t\t 💼 WELCOME TO EMPLOYEE MANAGEMENT SYSTEM 💼')
        print('\n=========================================================================================')
        print('\n[1] 🆕 Register 📝\n[2] 🔐 Login 🔓 \n[3] 🔚 Exit 👋🏻 ')
    
        try:
            choice = input('\nEnter your choice (1/2/3) : ')
        except ValueError:
            print('\n ⚠️ Invalid choice !!!')
            continue
        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                id = user[0]
                role = user[3]
                if role == 1:
                    manager_portal(id)
                else:
                    employee_portal(id)
        elif choice == '3':
            print('\n 🌟 Thank you for visiting Employee Management System 🌟 Have a nice day 🌟\n')
            break
        else:
            print('\n ⚠️ Invalid choice !!! ')

#---------------------------------------------------------- MANAGER PORTAL ----------------------------------------------------------#

def manager_portal(id):
    conn = sqlite3.connect('emp.db')
    cursor = conn.cursor()

    manager = Manager(id)
    print('\n\t_______________________\n\t| 🔐 MANAGER LOGIN 🔑 |\n\t|_____________________|')
    
    cursor.execute('''
                   SELECT name FROM Manager WHERE user_id = ?
                   ''',(id,))
    name = cursor.fetchone()[0]

    print(f'\n************* 👤 Welcome {name} 👤 *************')
    while True:
        print('\n==============================================================\n\t 👨‍💼  MANAGER  DASHBOARD \n==============================================================')
        print('\n[1] 👥 View all employees \n[2] ➕ Add employee\n[3] ✏️ Edit Employee Details \n[4] 🗑️ Delete Employee \n[5] 🔍 Search Employee \n[6] 🕓 View attendance details\n[7] 📅 Manage Leave Applications\n[8] 💰 Manage Employee Salary \n[9] 🚪 Logout')
        ch = input('Enter your choice : ')
        if ch == '1':
            manager.view_employees()
        elif ch == '2':
            manager.add_emp()           
        elif ch == '3':
            manager.update_emp()
        elif ch == '4':
            manager.delete_emp()
        elif ch =='5':
            manager.search_emp()
        elif ch == '6':
            manager.view_attendance()
        elif ch == '7':
            manager.manage_leave()
        elif ch == '8':
            manager.manage_salary()
        elif ch == '9':
            print(f'\n 👤 {name} 👤 Logging out...✅')
            break
        else:
            print('⚠️ Invalid choice!!!')
    conn.close()

#------------------------------------------------------- EMPLOYEE PORTAL  ------------------------------------------------------------#

def employee_portal(id):
    conn = sqlite3.connect('emp.db')
    cursor = conn.cursor()
    
    employee = Employee(id)
    print('\n\t________________________\n\t| 🔐 Employee Login 🔑 |\n\t|______________________|')
    cursor.execute('''
                   SELECT name FROM Employee WHERE user_id = ?
                   ''',(id,))
    name = cursor.fetchone()[0]
    conn.close()

    print(f'\n************* 👤 Welcome {name} 👤 *************')
    while True:
        print('\n========================================================\n\t 👨‍🔧 EMPLOYEE DASHBOARD \n========================================================')
        print('\n[1] 🔐 Reset Password\n[2] 👤 View Profile \n[3] ✏️ Edit Profile\n[4] 🕒 Punch in\n[5] 🕔 Punch out\n[6] 📝 Apply for Leave\n[7] 📝🌟 View leave Status \n[8] 💰 View Salary Details \n[9] 🚪 Logout')
        try:
            ch = input('Enter your choice : ')
        except ValueError:
            print('⚠️ Invalid choice!!!')
            continue
        if ch == '1':
            employee.change_password()
        elif ch == '2':
            employee.view_profile()
        elif ch == '3':
            employee.edit_profile()   
        elif ch == '4':
            employee.clock_in()    
        elif ch == '5':
            employee.clock_out()
        elif ch == '6':
            employee.apply_leave()
        elif ch == '7':
            employee.view_leave_status()
        elif ch == '8':
            employee.view_salary_details()
        elif ch == '9':
            print(f'\n👤 {name} 👤 Logging out...✅')
            break
        else:
            print('\n ⚠️ Invalid choice!!!')
    

main()

       
                    