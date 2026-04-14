import random
import string

def check_age():
    # This function checks the age category of the user based on their input
    try:
        age = int(input("\nEnter your age: "))

        if age < 0:
            print("\nAge cannot be negative")
            return
        
        if age < 13:
            print("\nYou are a child")
        elif 13 <= age < 18:
            print("\nYou are a teenager")
        else:
            print("\nYou are an adult")
    except ValueError:
        print("Please enter a valid integer for age")

# The following functions perform basic arithmetic operations and a simple calculator function that uses them. Additionally, there is a function to generate a random password based on user-specified length. Finally, a menu function allows the user to choose which functionality they want to use.
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y     

def calculator():
    # The calculator function performs basic arithmetic operations based on user input.
    while True:
        # 
        try:
            first_num = float(input("\nEnter the first number: "))
            oper_signs = input("Enter the operator sign (+, -, *, /): ")
            second_num = float(input("Enter the second number: "))

            # Perform the calculation based on the operator sign and handle division by zero
            if oper_signs == "+":
                result = add(first_num, second_num)
            elif oper_signs == "-":
                result = subtract(first_num, second_num)
            elif oper_signs ==  "*":
                result = multiply(first_num, second_num)
            elif oper_signs ==  "/":
                if second_num == 0:
                    print("Error: Cannot divide by zero")
                    continue
                result = divide(first_num, second_num)
            else:
                print("Invalid operator! Please try again.")
                continue

            print(f"Result: {result}")
            if input("Continue? (y/n): ").lower() != 'y':
                break
        except ValueError:
            print("Please enter valid numbers!")        



def generate_password():
    # This function generates a random password based on the desired length provided by the user. It includes a mix of uppercase letters, lowercase letters, digits, and punctuation characters. The function also handles invalid input for the password length.
    try:
        length = int(input("\nEnter the desired password length: "))
        if length <= 0:
            print("Password lenght must be greater than 0")
            return
        
        # Generate a random password using a combination of letters, digits, and punctuation characters
        characters = string.ascii_letters + string.digits + string.punctuation

        # 
        password = ''.join(random.choice(characters) for _ in range(length))
        
        print(f"\nGenerated password: {password}")
    except ValueError:
        print("Please enter a valid number for password lenght!")

def menu():

    # This function displays a menu to the user and allows them to choose between checking their age category, using a calculator, generating a password, or exiting the program. It handles invalid menu choices and continues to prompt the user until they choose to exit.
    while True:
        print("\nMenu")
        print("1. Check age category")
        print("2. Calculator")
        print("3. Generate password")
        print("4. Exit")

        choice = input("\nEnter your choice: ")
        
        if choice == "1":
             check_age()
        elif choice == "2":
            calculator()
        elif choice == "3":
            generate_password()
        elif choice == "4":
            print("Exiting the program")
            break
        else:
          print("\nInvalid choice, please try again")

# Call the menu function to start the program
menu() 