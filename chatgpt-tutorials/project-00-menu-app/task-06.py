try:
    age = int(input("Enter your age: "))
    
    if age < 13:
        print("You are a child")
    elif 13 <= age < 18:
        print("You are a teenager")
    else:
        print("You are an adult")

except ValueError:
    print("Please enter a valid number")