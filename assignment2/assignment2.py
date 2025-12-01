# Task 2: Employee Reader
import csv
import sys

def read_employees():
    try:
        employee_dict = {}
        rows = []
        
        with open('../csv/employees.csv', 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    employee_dict["fields"] = row
                else:
                    rows.append(row)
        
        employee_dict["rows"] = rows
        return employee_dict
    
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()

employees = read_employees()
print(employees)

#Task 3: Find the Column Index
def column_index(column_name):
    return employees["fields"].index(column_name)

employee_id_column = column_index("employee_id")

#Task 4: Find the Employee First Name
def first_name(row_number):
    return employees["rows"][row_number][column_index("first_name")]

#Task 5: Find the Employee: a Function in a Function
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    
    matches = list(filter(employee_match, employees["rows"]))
    return matches

#Task 6: Find the Employee with a Lambda
def employee_find_2(employee_id):
    matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
    return matches

#Task 7: Sort the Rows by last_name Using a Lambda
def sort_by_last_name():
    employees["rows"].sort(key=lambda row : row[column_index("last_name")])
    return employees["rows"]

sort_by_last_name()
print(employees)

#Task 8: Create a dict for an Employee
def employee_dict(row):
    result = {}
    for i, field in enumerate(employees["fields"]):
        if field != "employee_id":
            result[field] = row[i]
    return result

print(employee_dict(employees["rows"][0]))

#Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    result = {}
    for row in employees["rows"]:
        employee_id = row[employee_id_column]
        result[employee_id] = employee_dict(row)
    return result

print(all_employees_dict())

#Task 10: Use the os Module
import csv
import sys
import os

def get_this_value():
    return os.getenv("THISVALUE")

#Task 11: Creating Your Own Module
import csv
import sys
import os
import custom_module
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret("My Secret Password")
print(custom_module.secret)

#Task 12: Read minutes1.csv and minutes2.csv
def read_minutes():
    def read_minutes_file(file_path):
        minutes_dict = {}
        rows = []
        
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    minutes_dict["fields"] = row
                else:
                    rows.append(tuple(row))  # Convert row to tuple
        
        minutes_dict["rows"] = rows
        return minutes_dict

    minutes1 = read_minutes_file('../csv/minutes1.csv')
    minutes2 = read_minutes_file('../csv/minutes2.csv')
    
    return minutes1, minutes2
# Call the function and store the results in global variables
minutes1, minutes2 = read_minutes()
print(minutes1)
print(minutes2)

#Task 13: Create minutes_set
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    combined_set = set1.union(set2)
    return combined_set
# Call the function and store the result in a global variable
minutes_set = create_minutes_set()
print(minutes_set)

#Task 14: Convert to datetime
from datetime import datetime  # Importing datetime module

def create_minutes_list():
    # Create a list from the minutes_set
    minutes_list = list(minutes_set)
    # Use map to convert each element into a tuple
    converted_list = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list))
    return converted_list

# Call the function and store the result in a global variable
minutes_list = create_minutes_list()
print(minutes_list)  # Print the resulting list

#Task 15: Write Out Sorted List
import csv
from datetime import datetime  # Ensure datetime is imported

def write_sorted_list():
    # Sort minutes_list by datetime
    sorted_minutes = sorted(minutes_list, key=lambda x: x[1])
    
    # Convert each tuple back to the required format
    converted_sorted_list = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), sorted_minutes))
    
    # Write to minutes.csv
    with open('./minutes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(minutes1["fields"])  # Write the header
        writer.writerows(converted_sorted_list)  # Write the data rows
    
    return converted_sorted_list

# Call the function
sorted_minutes_list = write_sorted_list()
print(sorted_minutes_list)  # Print the resulting sorted list