while True:
    print("\nMenu")
    print("1. Check age category")
    print("2. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        try:
            age = int(input("Enter your age: "))

            if age < 0:
                print("Age cannot be negative")
                continue
            if age < 13:
                print("You are a child")
            elif 13 <= age < 18:
                print("You are a teenager")
            else:
                print("You are an adult")
        

        except ValueError:
            print("Please enter a valid integer for age")
    elif choice == "2":
        print("Exiting the program")
        break
    else:
        print("Invalid choice, please try again")