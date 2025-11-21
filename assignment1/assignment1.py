# Write your code here.

# Task 1
def hello():
    return "Hello!"

# Task 2
def greet(name):
    return f"Hello, {name}!"

#Task 3
def calc(a, b, operation="multiply"):
    try:
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            return a / b
        elif operation == "modulo":
            return a % b
        elif operation == "int_divide":
            return a // b
        elif operation == "power":
            return a ** b
        else:
            return "Invalid operation"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"

#Task 4
def data_type_conversion(value, data_type):
    try:
        if data_type == "float":
            return float(value)
        elif data_type == "int":
            return int(value)
        elif data_type == "str":
            return str(value)
        else:
            return f"Unsupported type: {data_type}"
    except Exception:
        return f"You can't convert {value} into a {data_type}."

# Task 5
def grade(*args):
    try:
        average = sum(args) / len(args)
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except Exception:
        return "Invalid data was provided."

# Task 6
def repeat(string, count):
    result = ""
    for i in range(count):
        result += string
    return result

# Task 7
def student_scores(option, **kwargs):
    try:
        if option == "best":
            # Find the student with the highest score
            best_student = max(kwargs, key=kwargs.get)
            return best_student
        elif option == "mean":
            # Compute the average score
            average = sum(kwargs.values()) / len(kwargs)
            return average
        else:
            return "Invalid option"
    except Exception:
        return "Invalid data was provided."

# Task 8
def titleize(text):
    little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}
    words = text.split()
    result = []

    for i, word in enumerate(words):
        # Always capitalize first and last word
        if i == 0 or i == len(words) - 1:
            result.append(word.capitalize())
        # Capitalize if not a little word
        elif word.lower() not in little_words:
            result.append(word.capitalize())
        # Keep little words lowercase
        else:
            result.append(word.lower())

    return " ".join(result)

# Task 9
def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"
    return result

# Task 10
def pig_latin(text):
    vowels = "aeiou"
    words = text.split()
    result = []

    for word in words:
        if word[0] in vowels:
            result.append(word + "ay")
        elif word.startswith("qu"):
            # Word begins with 'qu'
            result.append(word[2:] + "quay")
        else:
            # Find split point: first vowel, but treat 'qu' as a unit after consonants
            split = None
            for i, ch in enumerate(word):
                if ch in vowels:
                    # If this vowel is 'u' and preceded by 'q' within the leading consonants, include 'qu'
                    if ch == "u" and i > 0 and word[i-1] == "q":
                        split = i + 1  # include 'qu' in the leading cluster
                    else:
                        split = i
                    break
            if split is None:
                # No vowels: just append 'ay'
                result.append(word + "ay")
            else:
                result.append(word[split:] + word[:split] + "ay")

    return " ".join(result)