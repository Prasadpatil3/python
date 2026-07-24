nterms = 10  

a, b = 0, 1
count = 0

print("Fibonacci series:")
while count < nterms:
    print(a, end=" ")
    
   
    a, b = b, a + b
    
    count += 1