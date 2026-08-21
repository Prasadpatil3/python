from array import array
numbers = array('i')

n = int(input("Enter number of elements: "))

for i in range(n):
  num = int(input("Enter number: "))
  numbers.append(num)

print("Array elements are:")

for num in numbers:
  print(num)
