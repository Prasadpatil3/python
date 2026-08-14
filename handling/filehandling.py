import os

while True:
    print("\nFile handling")
    print("1. Create and Write (w)")
    print("2. Read File (r)")
    print("3. Append Data (a)")
    print("4. Read One Line (readline)")
    print("5. Read All Lines (readlines)")
    print("6. Current Position (tell)")
    print("7. Move Position (seek)")
    print("8. Read + Write (r+)")
    print("9. Write + Read (w+)")
    print("10. Append + Read (a+)")
    print("11. Rename File")
    print("12. Delete File")
    print("13. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
     with open("example.txt", "w") as file:
      file.write("Python is easy.\n")
      file.write("File handling is important.\n")
      file.write("Python is powerful.\n")
     print("File created and written successfully.")

    elif choice == 2:
        with open("example.txt", "r") as file:
            print("\nFile Content:")
            print(file.read())

    elif choice == 3:
        with open("example.txt", "a") as file:
            file.write("This is appended data.\n")
        print("Data appended successfully.")

    elif choice == 4:
        with open("example.txt", "r") as file:
            print("\nFirst line:")
            print(file.readline())

    elif choice == 5:
        with open("example.txt", "r") as file:
            print("\nAll lines:")
            print(file.readlines())

    elif choice == 6:
        with open("example.txt", "r") as file:
            file.read(5)
            print("Current file position:", file.tell())

    elif choice == 7:
        with open("example.txt", "r") as file:
            position = int(input("Enter position: "))
            file.seek(position)
            print("Current position:", file.tell())
            print("Data from this position:")
            print(file.read())

    elif choice == 8:
        
        with open("example.txt", "r+") as file:
            print("\nOriginal content:")
            print(file.read())

            file.write("\nData added using r+.")

        print("Data written using r+ successfully.")

    elif choice == 9:
    
        with open("example.txt", "w+") as file:
            file.write("Data written using w+.")

            file.seek(0)

            print("\nContent using w+:")
            print(file.read())

        print("w+ operation completed.")

    elif choice == 10:
        
        with open("example.txt", "a+") as file:
            file.write("\nData added using a+.")

            file.seek(0)

            print("\nContent using a+:")
            print(file.read())

        print("a+ operation completed.")

    elif choice == 11:
        oldname = input("Enter current file name: ")
        newname = input("Enter new file name: ")

        if os.path.exists(oldname):
            os.rename(oldname, newname)
            print("File renamed successfully.")
        else:
            print("File does not exist.")

    elif choice == 12:
        filename = input("Enter file name to delete: ")

        if os.path.exists(filename):
            os.remove(filename)
            print("File deleted successfully.")
        else:
            print("File does not exist.")

    elif choice == 13:
        print("Program ended.")
        break

    else:
        print("Invalid choice!")
