def chatbot():
    name = input("What is your name? ")
    age = input("How old are you? ")
    print(f"\nNice to meet you, {name}! You are {age} years old.")
    print("\nHow can I help you today?")
    print("Please choose an option from the menu below:")
    while True:
        print("\n--- Menu ---")
        print("1. Tell me a joke")
        print("2. Give me a fun fact")
        print("3. Say goodbye")
        
        choice = input("Enter the number of your choice: ")
        
        if choice == "1":
            print("Why don’t scientists trust atoms? Because they make up everything!")
        elif choice == "2":
            print("Fun fact: Honey never spoils. Archaeologists have found 3000-year-old honey still safe to eat!")
        elif choice == "3":
            print(f"Goodbye, {name}! Thanks for chatting.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    chatbot()
