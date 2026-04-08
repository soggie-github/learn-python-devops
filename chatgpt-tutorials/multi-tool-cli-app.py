def check_age():
    pass

# Calculator def
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y     

def calculator():
    while True:

        try:
            first_num = float(input("\nEnter the first number: "))
            oper_signs = input("Enter the operator sign (+, -, *, /): ")
            second_num = float(input("Enter the second number: "))

            if oper_signs == "+":
                result = add(first_num, second_num)
            elif oper_signs == "-":
                result = subtract(first_num, second_num)
            elif oper_signs ==  "*":
                result = multiply(first_num, second_num)
            elif oper_signs ==  "/":
                if second_num == 0:
                    return "Error: Cannot divide by zero"
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
    pass

def menu():
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

menu() 