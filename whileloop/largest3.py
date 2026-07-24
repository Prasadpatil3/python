a = int(input("Enter first no: "))
b = int(input("Enter second no: "))
c = int(input("Enter third no: "))

if a > b and a > c:
    print("Largest no is:", a)
elif b > c:
    print("Largest no is:", b)
else:
    print("Largest no is:", c)