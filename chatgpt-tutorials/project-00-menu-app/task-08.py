#def menu():
#    while True:
#        print("\nMenu")
#        print("1. Check age category")
#        print("2. Exit")
#        choice = input("Enter your choice: ")
#        if choice == "1":
#            try:
#                age = int(input("Enter your age: "))
#                if age < 0:
#                    print("Age cannot be negative")
#                    continue
#                if age < 13:
#                    print("You are a child")
#                elif 13 <= age < 18:
#                    print("You are a teenager")
#                else:
#                    print("You are an adult")
            

#            except ValueError:
#                print("Please enter a valid integer for age")
#        elif choice == "2":
#            print("Exiting the program")
#            break
#        else:
#            print("Invalid choice, please try again")

#menu()

def check_age():

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


def menu():
    while True:
        print("\nMenu")
        print("1. Check age category")
        print("2. Exit")
        choice = input("\nEnter your choice: ")
        if choice == "1":
             check_age()
        elif choice == "2":
            print("Exiting the program")
            break
        else:
            print("\nInvalid choice, please try again")
menu()