import csv

# Reading the contents of ../csv/employees.csv into a list of lists using the csv module
with open('../csv/employees.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Using a list comprehension, create a list of the employee names, first_name + space + last_name
# Skip the header
names = [row[1] + ' ' + row[2] for row in data[1:]]

# Printing the resulting list
print(names)

# Using a list comprehension, create another list from the previous list of names
# Including only those names that contain the letter "e"
names_with_e = [name for name in names if 'e' in name]

# Print list
print(names_with_e)
