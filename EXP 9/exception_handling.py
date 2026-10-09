try:
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))

    result = a / b
    print("Division =", result)

except ZeroDivisionError:
    print("Error: Cannot divide by zero.")

except ValueError:
    print("Error: Please enter valid integers.")

finally:
    print("Program execution completed.")
