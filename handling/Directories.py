import os

while True:
    print("\nDirectory handling")
    print("1. Create Directory")
    print("2. List Directory")
    print("3. Change Directory")
    print("4. Show Current Directory")
    print("5. Rename Directory")
    print("6. Delete Directory")
    print("7. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        dirname = input("Enter directory name: ")
        os.mkdir(dirname)
        print("Directory created successfully.")

    elif choice == 2:
        print("Directories and files:")
        print(os.listdir())

    elif choice == 3:
        dirname = input("Enter directory path: ")
        os.chdir(dirname)
        print("Directory changed successfully.")

    elif choice == 4:
        print("Current directory:")
        print(os.getcwd())

    elif choice == 5:
        oldname = input("Enter old directory name: ")
        newname = input("Enter new directory name: ")
        os.rename(oldname, newname)
        print("Directory renamed successfully.")

    elif choice == 6:
        dirname = input("Enter directory name: ")
        os.rmdir(dirname)
        print("Directory deleted successfully.")

    elif choice == 7:
        print("Program ended.")
        break

    else:
        print("Invalid choice!")
