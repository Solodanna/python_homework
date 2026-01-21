import pandas as pd

# TASK 1: Create a DataFrame from a dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)
print(task1_data_frame)

# adding new column
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print(task1_with_salary)

# Modify existing column
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1
print(task1_older)

# Saving the DataFrame as CSV file
task1_older.to_csv('employees.csv', index=False)

# TASK 2: Loading Data from CSV and JSON
# Read data from CSV file
task2_employees = pd.read_csv('employees.csv')
print(task2_employees)

# Read data from JSON file
json_employees = pd.read_json('additional_employees.json')
print(json_employees)

# Combine DataFrames
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print(more_employees)

# TASK 3: Data Inspection - Using Head, Tail, and Info Methods
# Use head() method
first_three = more_employees.head(3)
print(first_three)

# Use tail() method
last_two = more_employees.tail(2)
print(last_two)

# Get shape of DataFrame
employee_shape = more_employees.shape
print(employee_shape)

# Use info() method
print(more_employees.info())

# TASK 4: Data Cleaning
# Create a DataFrame from dirty_data.csv file
dirty_data = pd.read_csv('dirty_data.csv')
print(dirty_data)

# Create a copy of the dirty data
clean_data = dirty_data.copy()

# Remove any duplicate rows from the DataFrame
clean_data.drop_duplicates(inplace=True)
print(clean_data)

# Convert Age to numeric and handle missing values
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print(clean_data)

# Convert Salary to numeric and replace known placeholders (unknown, n/a) with NaN
clean_data['Salary'] = clean_data['Salary'].replace(['unknown', 'n/a'], pd.NA)
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')
print(clean_data)

# Fill missing numeric values (use fillna). Fill Age with the mean and Salary with the median
clean_data['Age'].fillna(clean_data['Age'].mean(), inplace=True)
clean_data['Salary'].fillna(clean_data['Salary'].median(), inplace=True)
print(clean_data)

# Convert Hire Date to datetime
clean_data['Hire Date'] = clean_data['Hire Date'].str.strip()
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], format='mixed', errors='coerce')
print(clean_data)

# Strip extra whitespace and standardize Name and Department as uppercase
clean_data['Name'] = clean_data['Name'].str.strip()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print(clean_data)

