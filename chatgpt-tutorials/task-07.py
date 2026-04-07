while True:
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
            
        break
    except ValueError:
        print("Please enter a valid number")

